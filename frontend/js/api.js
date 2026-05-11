// =========================================================
// BAMBOO FORCE AI
// API SERVICE LAYER
// =========================================================

// =========================================================
// BASE URL
// =========================================================

const BASE_URL =
    "http://127.0.0.1:8000";

// =========================================================
// GENERIC GET
// =========================================================

async function getRequest(endpoint) {

    try {

        const response = await fetch(

            `${BASE_URL}${endpoint}`
        );

        return await response.json();

    } catch (error) {

        console.error(

            "GET request failed:",

            error
        );

        return {

            success: false,

            message: "Backend unavailable"
        };
    }
}

// =========================================================
// GENERIC POST JSON
// =========================================================

async function postJSON(

    endpoint,

    data
) {

    try {

        const response = await fetch(

            `${BASE_URL}${endpoint}`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    data
                )
            }
        );

        return await response.json();

    } catch (error) {

        console.error(

            "POST JSON failed:",

            error
        );

        return {

            success: false,

            message:
                "Backend unavailable"
        };
    }
}

// =========================================================
// GENERIC POST FORM DATA
// =========================================================

async function postFormData(

    endpoint,

    formData
) {

    try {

        const response = await fetch(

            `${BASE_URL}${endpoint}`,

            {

                method: "POST",

                body: formData
            }
        );

        return await response.json();

    } catch (error) {

        console.error(

            "POST FormData failed:",

            error
        );

        return {

            success: false,

            message:
                "Upload failed"
        };
    }
}

// =========================================================
// HEALTH CHECK
// =========================================================

async function getBackendHealth() {

    return await getRequest(
        "/health"
    );
}

// =========================================================
// CREATE RIDE
// =========================================================

async function createRide(

    rideData
) {

    return await postJSON(

        "/api/ride/create",

        rideData
    );
}

// =========================================================
// FACE VERIFICATION
// =========================================================

async function verifyFace(

    formData
) {

    return await postFormData(

        "/api/verify/verify",

        formData
    );
}

// =========================================================
// REGISTER DRIVER
// =========================================================

async function registerDriver(

    formData
) {

    return await postFormData(

        "/api/verify/register",

        formData
    );
}

// =========================================================
// GET ACTIVE RIDES
// =========================================================

async function getActiveRides() {

    return await getRequest(

        "/api/ride/active"
    );
}

// =========================================================
// GET RECOMMENDATIONS
// =========================================================

async function getRecommendations() {

    return await getRequest(

        "/api/ride/recommendations"
    );
}

// =========================================================
// START RIDE
// =========================================================

async function startRide(

    rideId
) {

    return await postJSON(

        `/api/ride/start/${rideId}`,

        {}
    );
}

// =========================================================
// COMPLETE RIDE
// =========================================================

async function completeRide(

    rideId
) {

    return await postJSON(

        `/api/ride/complete/${rideId}`,

        {}
    );
}

// =========================================================
// CANCEL RIDE
// =========================================================

async function cancelRide(

    rideId
) {

    return await postJSON(

        `/api/ride/cancel/${rideId}`,

        {}
    );
}

// =========================================================
// RISK PREDICTION
// =========================================================

async function predictRideRisk(

    riskData
) {

    return await postJSON(

        "/api/risk/predict",

        riskData
    );
}

// =========================================================
// UPDATE BACKEND STATUS
// =========================================================

async function updateBackendStatus() {

    const health =
        await getBackendHealth();

    console.log(

        "Backend Health:",

        health
    );
}

// =========================================================
// AUTO MONITOR
// =========================================================

setInterval(() => {

    updateBackendStatus();

}, 10000);

// =========================================================
// INITIAL CHECK
// =========================================================

window.addEventListener(

    "load",

    () => {

        updateBackendStatus();
    }
);

// =========================================================
// GLOBAL ACCESS
// =========================================================

window.createRide =
    createRide;

window.verifyFace =
    verifyFace;

window.registerDriver =
    registerDriver;

window.getActiveRides =
    getActiveRides;

window.getRecommendations =
    getRecommendations;

window.startRide =
    startRide;

window.completeRide =
    completeRide;

window.cancelRide =
    cancelRide;

window.predictRideRisk =
    predictRideRisk;