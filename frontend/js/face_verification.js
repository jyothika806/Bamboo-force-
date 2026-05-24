// =========================================================
// GLOBAL VARIABLES
// =========================================================

let driverCapturedBlob = null;

let verifyCapturedBlob = null;

let recordedVideoBlob = null;

let mediaRecorder = null;

let recordedChunks = [];

// =========================================================
// CLEANUP FUNCTIONS
// =========================================================

function cleanupDriverCamera() {
    if (window.driverStream) {
        window.driverStream.getTracks().forEach(track => track.stop());
        window.driverStream = null;
    }
}

function cleanupVerifyCamera() {
    if (window.verifyStream) {
        window.verifyStream.getTracks().forEach(track => track.stop());
        window.verifyStream = null;
    }
}

function cleanupMediaRecorder() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    mediaRecorder = null;
    recordedChunks = [];
}

// =========================================================
// LOADING INDICATORS
// =========================================================

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.disabled = true;
        element.textContent = "Processing...";
    }
}

function hideLoading(elementId, originalText) {
    const element = document.getElementById(elementId);
    if (element) {
        element.disabled = false;
        element.textContent = originalText;
    }
}

function showError(message) {
    alert(message);
}

// =========================================================
// START DRIVER CAMERA
// =========================================================

async function startDriverCamera() {
    try {
        const video = document.getElementById(
            "driverVideo"
        );

        const stream =
            await navigator.mediaDevices.getUserMedia({

                video: true,

                audio: false
            });

        video.srcObject = stream;

        window.driverStream = stream;
    } catch (error) {
        console.error("Failed to start driver camera:", error);
        showError("Failed to access camera. Please ensure camera permissions are granted.");
    }
}

// =========================================================
// RECORD DRIVER VIDEO
// =========================================================

async function recordDriverVideo() {

    recordedChunks = [];

    const stream = window.driverStream;

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {

        if (event.data.size > 0) {

            recordedChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {

        recordedVideoBlob = new Blob(

            recordedChunks,

            {
                type: "video/webm"
            }
        );

        alert(
            "Driver liveness video recorded"
        );
    };

    mediaRecorder.start();

    alert(
        "Recording started for 3 seconds"
    );

    setTimeout(() => {

        mediaRecorder.stop();

    }, 3000);
}

// =========================================================
// CAPTURE DRIVER FACE FRAME
// =========================================================

function captureDriverFace() {

    const video = document.getElementById(
        "driverVideo"
    );

    const canvas = document.getElementById(
        "driverCanvas"
    );

    const context =
        canvas.getContext("2d");

    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;

    context.drawImage(

        video,

        0,

        0,

        canvas.width,

        canvas.height
    );

    canvas.toBlob(blob => {

        driverCapturedBlob = blob;

        alert(
            "Driver face frame captured"
        );

    }, "image/jpeg");
}

// =========================================================
// DRIVER REGISTRATION
// =========================================================

async function handleDriverRegistration() {
    console.log("[DEBUG] handleDriverRegistration() called");
    try {
        // =====================================================
        // VALIDATION
        // =====================================================
        const finalVideo =
            recordedVideoBlob;

        console.log("[DEBUG] finalVideo:", finalVideo ? "present" : "missing");

        if (!finalVideo) {
            console.error("[DEBUG] Validation failed: No final video");
            showError("Record or upload liveness video");
            return;
        }

        if (!driverCapturedBlob) {
            console.error("[DEBUG] Validation failed: No driver face captured");
            showError("Capture driver face first");
            return;
        }

        console.log("[DEBUG] driverCapturedBlob:", driverCapturedBlob ? "present" : "missing");

        const idProof =
            document.getElementById(
                "driverIdProof"
            ).files[0];

        console.log("[DEBUG] idProof:", idProof ? "present" : "missing");

        if (!idProof) {
            console.error("[DEBUG] Validation failed: No ID proof");
            showError("Upload ID proof");
            return;
        }

        const driverId =
            document.getElementById(
                "driverId"
            ).value;

        const driverName =
            document.getElementById(
                "driverName"
            ).value;

        console.log("[DEBUG] driverId:", driverId, "driverName:", driverName);

        if (!driverId || !driverName) {
            console.error("[DEBUG] Validation failed: Missing driver ID or name");
            showError("Please enter Driver ID and Name");
            return;
        }

        // Check backend availability
        const backendAvailable = window.isBackendAvailable();
        console.log("[DEBUG] Backend available:", backendAvailable);
        
        if (!backendAvailable) {
            console.error("[DEBUG] Backend unavailable");
            showError("Backend is currently unavailable. Please try again later.");
            return;
        }

        showLoading("registerButton");
        console.log("[DEBUG] Loading indicator shown");

        // =====================================================
        // LIVENESS FORM
        // =====================================================

        const liveFormData =
            new FormData();

        liveFormData.append(

            "file",

            finalVideo,

            "driver_video.webm"
        );

        console.log("[DEBUG] Liveness FormData created");

        // =====================================================
        // LIVENESS CHECK
        // =====================================================

        console.log("[DEBUG] Calling checkLiveness()...");
        const liveResult =
            await checkLiveness(
                liveFormData
            );

        console.log(
            "[DEBUG] Liveness Result:",
            liveResult
        );

        // =====================================================
        // SPOOF DETECTED
        // =====================================================

        if (

            !liveResult.success ||

            !liveResult.data.is_live
        ) {
            console.error("[DEBUG] Liveness check failed:", liveResult);
            hideLoading("registerButton", "Register Driver");
            showError("Spoof detected");
            return;
        }

        console.log("[DEBUG] Liveness check passed");

        // =====================================================
        // FACE VERIFICATION FORM
        // =====================================================

        const verifyFormData =
            new FormData();

        verifyFormData.append(

            "driver_id",

            driverId
        );

        verifyFormData.append(

            "driver_name",

            driverName
        );

        verifyFormData.append(

            "id_image",

            idProof
        );

        verifyFormData.append(

            "live_image",

            driverCapturedBlob,

            "driver_face.jpg"
        );

        console.log("[DEBUG] Registration FormData created with:", {
            driver_id: driverId,
            driver_name: driverName,
            id_image: idProof ? "present" : "missing",
            live_image: driverCapturedBlob ? "present" : "missing"
        });

        // =====================================================
        // REGISTER DRIVER
        // =====================================================

        console.log("[DEBUG] Calling registerDriver()...");
        const result =
            await registerDriver(
                verifyFormData
            );

        console.log(
            "[DEBUG] Driver Registration result:",
            result
        );

        // =====================================================
        // RESULT UI
        // =====================================================

        const resultBox =
            document.getElementById(
                "driverResult"
            );

        if (

            result.success
        ) {

            resultBox.innerHTML = `

                <h2 class="success">

                    Driver Registered

                </h2>

                <pre>

${JSON.stringify(result, null, 2)}

                </pre>
            `;

        } else {

            resultBox.innerHTML = `

                <h2 class="error">

                    Registration Failed

                </h2>

                <pre>

${JSON.stringify(result, null, 2)}

                </pre>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Registration error:", error);
        console.error("[DEBUG] Error stack:", error.stack);
        showError("Registration failed: " + (error.message || "Unknown error"));
    } finally {
        console.log("[DEBUG] Cleaning up loading indicator");
        hideLoading("registerButton", "Register Driver");
    }
}

// =========================================================
// START VERIFY CAMERA
// =========================================================

async function startVerifyCamera() {
    try {
        const video = document.getElementById(
            "verifyVideo"
        );

        const stream =
            await navigator.mediaDevices.getUserMedia({

                video: true,

                audio: false
            });

        video.srcObject = stream;

        window.verifyStream = stream;
    } catch (error) {
        console.error("Failed to start verify camera:", error);
        showError("Failed to access camera. Please ensure camera permissions are granted.");
    }
}

// =========================================================
// RECORD VERIFY VIDEO
// =========================================================

async function recordVerifyVideo() {

    recordedChunks = [];

    const stream = window.verifyStream;

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {

        if (event.data.size > 0) {

            recordedChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {

        recordedVideoBlob = new Blob(

            recordedChunks,

            {
                type: "video/webm"
            }
        );

        alert(
            "Verification video recorded"
        );
    };

    mediaRecorder.start();

    alert(
        "Recording verification video..."
    );

    setTimeout(() => {

        mediaRecorder.stop();

    }, 3000);
}

// =========================================================
// CAPTURE VERIFY FRAME
// =========================================================

function captureVerifyFace() {

    const video = document.getElementById(
        "verifyVideo"
    );

    const canvas = document.getElementById(
        "verifyCanvas"
    );

    const context =
        canvas.getContext("2d");

    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;

    context.drawImage(

        video,

        0,

        0,

        canvas.width,

        canvas.height
    );

    canvas.toBlob(blob => {

        verifyCapturedBlob = blob;

        alert(
            "Verification frame captured"
        );

    }, "image/jpeg");
}

// =========================================================
// VERIFY DRIVER
// =========================================================

async function handleVerify() {
    console.log("[DEBUG] handleVerify() called");
    try {
        const finalVideo =
            recordedVideoBlob;
        console.log("[DEBUG] finalVideo:", finalVideo ? "present" : "missing");
        
        if (!finalVideo) {
            console.error("[DEBUG] Validation failed: No final video");
            showError("Record or upload liveness video");
            return;
        }
        if (!verifyCapturedBlob) {
            console.error("[DEBUG] Validation failed: No verify frame captured");
            showError("Capture verification frame");
            return;
        }

        console.log("[DEBUG] verifyCapturedBlob:", verifyCapturedBlob ? "present" : "missing");

        const driverId =
            document.getElementById(
                "verifyDriverId"
            ).value;

        console.log("[DEBUG] driverId:", driverId);

        if (!driverId) {
            console.error("[DEBUG] Validation failed: Missing driver ID");
            showError("Please enter Driver ID to verify");
            return;
        }

        // Check backend availability
        const backendAvailable = window.isBackendAvailable();
        console.log("[DEBUG] Backend available:", backendAvailable);
        
        if (!backendAvailable) {
            console.error("[DEBUG] Backend unavailable");
            showError("Backend is currently unavailable. Please try again later.");
            return;
        }

        showLoading("verifyButton");
        console.log("[DEBUG] Loading indicator shown");

        // =====================================================
        // LIVENESS CHECK
        // =====================================================

        const liveFormData =
            new FormData();

        liveFormData.append(

            "file",

            finalVideo,

    

            "verify_video.webm"
        );

        console.log("[DEBUG] Verify liveness FormData created");
        console.log("[DEBUG] Calling checkLiveness()...");
        const liveResult =
            await checkLiveness(
                liveFormData
            );

        console.log(
            "[DEBUG] Verify Liveness Result:",
            liveResult
        );

        if (

            !liveResult.success ||

            !liveResult.data.is_live
        ) {
            console.error("[DEBUG] Verify liveness check failed:", liveResult);
            hideLoading("verifyButton", "Verify Driver");
            showError("Spoof detected");
            return;
        }

        console.log("[DEBUG] Verify liveness check passed");

        // =====================================================
        // FACE VERIFY
        // =====================================================

        const verifyFormData =
            new FormData();

        verifyFormData.append(

            "driver_id",

            driverId
        );

        verifyFormData.append(

            "live_image",

            verifyCapturedBlob,

            "verify_driver.jpg"
        );

        console.log("[DEBUG] Verify FormData created with:", {
            driver_id: driverId,
            live_image: verifyCapturedBlob ? "present" : "missing"
        });

        console.log("[DEBUG] Calling verifyFace()...");
        const result =
            await verifyFace(
                verifyFormData
            );

        console.log(
            "[DEBUG] Driver Verification result:",
            result
        );

        // =====================================================
        // RESULT UI
        // =====================================================

        const resultBox =
            document.getElementById(
                "result"
            );

        if (

            result.success &&

            result.data?.verified
        ) {

            resultBox.innerHTML = `

                <h2 class="success">

                    Driver Verified

                </h2>

                <pre>

${JSON.stringify(result, null, 2)}

                </pre>
            `;

        } else {

            resultBox.innerHTML = `

                <h2 class="error">

                    Verification Failed

                </h2>

                <pre>

${JSON.stringify(result, null, 2)}

                </pre>
            `;
        }
    } catch (error) {
        console.error("Verification error:", error);
        showError("Verification failed: " + (error.message || "Unknown error"));
    } finally {
        hideLoading("verifyButton", "Verify Driver");
    }
}