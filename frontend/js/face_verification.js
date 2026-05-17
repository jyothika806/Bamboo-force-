// =========================================================
// GLOBAL VARIABLES
// =========================================================

let driverCapturedBlob = null;

let verifyCapturedBlob = null;

let recordedVideoBlob = null;

let mediaRecorder = null;

let recordedChunks = [];

// =========================================================
// START DRIVER CAMERA
// =========================================================

async function startDriverCamera() {

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

    // =====================================================
    // VALIDATION
    // =====================================================
    const finalVideo =
        recordedVideoBlob;

    if (!finalVideo) {

        alert(
            "Record or upload liveness video"
        );

        return;
    }

    if (!driverCapturedBlob) {

        alert(
            "Capture driver face first"
        );

        return;
    }

    const idProof =
        document.getElementById(
            "driverIdProof"
        ).files[0];

    if (!idProof) {

        alert(
            "Upload ID proof"
        );

        return;
    }

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

    // =====================================================
    // LIVENESS CHECK
    // =====================================================

    const liveResult =
        await checkLiveness(
            liveFormData
        );

    console.log(
        "Liveness Result:",
        liveResult
    );

    // =====================================================
    // SPOOF DETECTED
    // =====================================================

    if (

        !liveResult.success ||

        !liveResult.data.is_live
    ) {

        alert(
            "Spoof detected"
        );

        return;
    }

    // =====================================================
    // FACE VERIFICATION FORM
    // =====================================================

    const verifyFormData =
        new FormData();

    verifyFormData.append(

        "file",

        driverCapturedBlob,

        "driver_face.jpg"
    );

    verifyFormData.append(

        "id_proof",

        idProof
    );

    // =====================================================
    // REGISTER DRIVER
    // =====================================================

    const result =
        await registerDriver(
            verifyFormData
        );

    console.log(
        "Driver Registration:",
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

        result.success &&

        result.data.success
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
}

// =========================================================
// START VERIFY CAMERA
// =========================================================

async function startVerifyCamera() {

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

    const finalVideo =
        recordedVideoBlob;
    if (!finalVideo) {

        alert(
            "Record or upload liveness video"
        );

        return;
    }
    if (!verifyCapturedBlob) {

        alert(
            "Capture verification frame"
        );

        return;
    }

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

    const liveResult =
        await checkLiveness(
            liveFormData
        );

    console.log(
        "Verify Liveness:",
        liveResult
    );

    if (

        !liveResult.success ||

        !liveResult.data.is_live
    ) {

        alert(
            "Spoof detected"
        );

        return;
    }

    // =====================================================
    // FACE VERIFY
    // =====================================================

    const verifyFormData =
        new FormData();

    verifyFormData.append(

        "file",

        verifyCapturedBlob,

        "verify_driver.jpg"
    );

    const result =
        await verifyFace(
            verifyFormData
        );

    console.log(
        "Driver Verification:",
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

        result.verified
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
}