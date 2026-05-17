// =========================================================
// BAMBOO FORCE AI
// FINAL API SERVICE LAYER
// =========================================================

// =========================================================
// BASE URL
// =========================================================

const API_BASE =
    "http://127.0.0.1:8000";

// =========================================================
// GENERIC API REQUEST
// =========================================================

async function apiRequest(

    endpoint,
    options = {}

) {

    try {

        console.log(
            "[API REQUEST]",
            endpoint
        );

        const response =
            await fetch(

                `${API_BASE}${endpoint}`,

                options
            );

        const data =
            await response.json();

        console.log(
            "[API RESPONSE]",
            endpoint,
            data
        );

        return data;

    } catch (error) {

        console.error(
            "[API ERROR]",
            endpoint,
            error
        );

        return {

            success: false,

            error:
                error.message
        };
    }
}

// =========================================================
// HEALTH CHECK
// =========================================================

async function getBackendHealth() {

    return await apiRequest(

        "/api/ride/health",

        {
            method: "GET"
        }
    );
}

// =========================================================
// FACE VERIFICATION
// =========================================================

async function verifyFace(

    formData
) {

    return await apiRequest(

        "/api/verify/verify",

        {

            method: "POST",

            body: formData
        }
    );
}

// =========================================================
// REGISTER DRIVER
// =========================================================

async function registerDriver(

    formData
) {

    return await apiRequest(

        "/api/verify/register",

        {

            method: "POST",

            body: formData
        }
    );
}

// =========================================================
// LIVENESS CHECK
// =========================================================

async function checkLiveness(

    formData
) {

    return await apiRequest(

        "/api/liveness/check",

        {

            method: "POST",

            body: formData
        }
    );
}

// =========================================================
// CREATE RIDE
// =========================================================

async function createRide(

    rideData
) {

    return await apiRequest(

        "/api/ride/create",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                rideData
            )
        }
    );
}

// =========================================================
// GET ACTIVE RIDES
// =========================================================

async function getActiveRides() {

    return await apiRequest(

        "/api/ride/active",

        {
            method: "GET"
        }
    );
}

// =========================================================
// GET ACTIVE GROUPS
// =========================================================

async function getActiveGroups() {

    return await apiRequest(

        "/api/ride/groups",

        {
            method: "GET"
        }
    );
}

// =========================================================
// GET RECOMMENDATIONS
// =========================================================

async function getRecommendations() {

    return await apiRequest(

        "/api/ride/recommendations",

        {
            method: "GET"
        }
    );
}

// =========================================================
// START RIDE
// =========================================================

async function startRide(

    rideId
) {

    return await apiRequest(

        `/api/ride/start/${rideId}`,

        {
            method: "POST"
        }
    );
}

// =========================================================
// COMPLETE RIDE
// =========================================================

async function completeRide(

    rideId
) {

    return await apiRequest(

        `/api/ride/complete/${rideId}`,

        {
            method: "POST"
        }
    );
}

// =========================================================
// CANCEL RIDE
// =========================================================

async function cancelRide(

    rideId
) {

    return await apiRequest(

        `/api/ride/cancel/${rideId}`,

        {
            method: "POST"
        }
    );
}

// =========================================================
// RISK PREDICTION
// =========================================================

async function predictRideRisk(

    riskData
) {

    return await apiRequest(

        "/api/risk/predict",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                riskData
            )
        }
    );
}

// =========================================================
// DASHBOARD LOADER
// =========================================================

async function loadDashboardData() {

    try {

        const [

            rides,
            groups,
            recommendations

        ] = await Promise.all([

            getActiveRides(),

            getActiveGroups(),

            getRecommendations()
        ]);

        console.log(
            "Dashboard Loaded"
        );

        return {

            rides,
            groups,
            recommendations
        };

    } catch (error) {

        console.error(
            "Dashboard Error",
            error
        );

        return null;
    }
}

// =========================================================
// BACKEND STATUS
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
// INITIALIZE
// =========================================================

window.addEventListener(

    "load",

    async () => {

        console.log(
            "Bamboo Force Initialized"
        );

        await updateBackendStatus();
    }
);

// =========================================================
// AUTO HEALTH CHECK
// =========================================================

setInterval(

    updateBackendStatus,

    10000
);

// =========================================================
// GLOBAL EXPORTS
// =========================================================

window.verifyFace =
    verifyFace;

window.registerDriver =
    registerDriver;

window.checkLiveness =
    checkLiveness;

window.createRide =
    createRide;

window.getActiveRides =
    getActiveRides;

window.getActiveGroups =
    getActiveGroups;

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

window.loadDashboardData =
    loadDashboardData;
// =========================================================
// RISK PREDICTION
// =========================================================

async function predictRideRisk(

    riskData
) {

    return await apiRequest(

        "/api/risk/predict",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                riskData
            )
        }
    );
}

// =========================================================
// GET RISK HISTORY
// =========================================================

async function getRiskHistory() {

    return await apiRequest(

        "/api/risk/history",

        {
            method: "GET"
        }
    );
}

// =========================================================
// GET LIVE RISK STATUS
// =========================================================

async function getLiveRiskStatus() {

    return await apiRequest(

        "/api/risk/live",

        {
            method: "GET"
        }
    );
}

// =========================================================
// ANALYZE DRIVER RISK
// =========================================================

async function analyzeDriverRisk(

    driverData
) {

    return await apiRequest(

        "/api/risk/analyze_driver",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                driverData
            )
        }
    );
}

// =========================================================
// ANALYZE ROUTE RISK
// =========================================================

async function analyzeRouteRisk(

    routeData
) {

    return await apiRequest(

        "/api/risk/analyze_route",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                routeData
            )
        }
    );
}