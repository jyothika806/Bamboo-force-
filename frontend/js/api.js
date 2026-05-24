// =========================================================
// BAMBOO FORCE AI — API SERVICE LAYER
// =========================================================

const API_BASE =
    (window.APP_CONFIG && window.APP_CONFIG.baseUrl) ||
    "http://127.0.0.1:8000";

const REQUEST_TIMEOUT_MS =
    (window.APP_CONFIG && window.APP_CONFIG.requestTimeoutMs) ||
    30000;

const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 1000;

// =========================================================
// GENERIC API REQUEST WITH RETRY
// =========================================================

async function apiRequest(endpoint, options = {}, retryCount = 0) {
    try {
        console.log("[API REQUEST]", endpoint, retryCount > 0 ? `(Retry ${retryCount})` : "");

        const controller = new AbortController();
        const timeoutId = setTimeout(
            () => controller.abort(),
            REQUEST_TIMEOUT_MS
        );

        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            signal: controller.signal,
        });

        clearTimeout(timeoutId);

        let data;
        const contentType = response.headers.get("content-type") || "";

        if (contentType.includes("application/json")) {
            data = await response.json();
        } else {
            const text = await response.text();
            data = {
                success: response.ok,
                message: text,
            };
        }

        if (!response.ok) {
            console.error("[API HTTP ERROR]", endpoint, response.status, data);
            
            // Retry on 5xx errors or network issues
            if (retryCount < MAX_RETRIES && (response.status >= 500 || response.status === 0)) {
                console.log(`[API RETRY] Waiting ${RETRY_DELAY_MS}ms before retry...`);
                await new Promise(resolve => setTimeout(resolve, RETRY_DELAY_MS));
                return apiRequest(endpoint, options, retryCount + 1);
            }
            
            return {
                success: false,
                status: response.status,
                error:
                    data.detail ||
                    data.message ||
                    data.error ||
                    `Request failed (${response.status})`,
                data: data,
            };
        }

        console.log("[API RESPONSE]", endpoint, data);
        return data;
    } catch (error) {
        console.error("[API ERROR]", endpoint, error);
        
        // Retry on network errors
        if (retryCount < MAX_RETRIES && (error.name === "AbortError" || error.message.includes("fetch"))) {
            console.log(`[API RETRY] Waiting ${RETRY_DELAY_MS}ms before retry...`);
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY_MS));
            return apiRequest(endpoint, options, retryCount + 1);
        }
        
        return {
            success: false,
            error: error.message || "Network error",
        };
    }
}

// =========================================================
// HEALTH CHECK
// =========================================================

async function getBackendHealth() {
    return apiRequest("/api/ride/health", { method: "GET" });
}

async function getAppHealth() {
    return apiRequest("/health", { method: "GET" });
}

// =========================================================
// FACE VERIFICATION
// =========================================================

async function verifyFace(formData) {
    return apiRequest("/api/verify/verify", {
        method: "POST",
        body: formData,
    });
}

async function registerDriver(formData) {
    return apiRequest("/api/verify/register", {
        method: "POST",
        body: formData,
    });
}

// =========================================================
// LIVENESS CHECK
// =========================================================

async function checkLiveness(formData) {
    return apiRequest("/api/liveness/check", {
        method: "POST",
        body: formData,
    });
}

// =========================================================
// RIDE OPTIMIZATION
// =========================================================

async function createRide(rideData) {
    return apiRequest("/api/ride/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(rideData),
    });
}

async function getActiveRides() {
    return apiRequest("/api/ride/active", { method: "GET" });
}

async function getActiveGroups() {
    return apiRequest("/api/ride/groups", { method: "GET" });
}

async function getRecommendations() {
    return apiRequest("/api/ride/recommendations", { method: "GET" });
}

async function startRide(rideId) {
    return apiRequest(`/api/ride/start/${rideId}`, { method: "POST" });
}

async function completeRide(rideId) {
    return apiRequest(`/api/ride/complete/${rideId}`, { method: "POST" });
}

async function cancelRide(rideId) {
    return apiRequest(`/api/ride/cancel/${rideId}`, { method: "POST" });
}

async function getRideHistory() {
    return apiRequest("/api/ride/history", { method: "GET" });
}

// =========================================================
// RISK PREDICTION
// =========================================================

async function predictRideRisk(riskData) {
    return apiRequest("/api/risk/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(riskData),
    });
}

async function getRiskHistory() {
    return apiRequest("/api/risk/history", { method: "GET" });
}

async function getLiveRiskStatus() {
    return apiRequest("/api/risk/live", { method: "GET" });
}

async function analyzeDriverRisk(driverData) {
    return apiRequest("/api/risk/analyze_driver", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(driverData),
    });
}

async function analyzeRouteRisk(routeData) {
    return apiRequest("/api/risk/analyze_route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(routeData),
    });
}

// =========================================================
// DASHBOARD LOADER
// =========================================================

async function loadDashboardData() {
    try {
        const [rides, groups, recommendations] = await Promise.all([
            getActiveRides(),
            getActiveGroups(),
            getRecommendations(),
        ]);

        return { rides, groups, recommendations };
    } catch (error) {
        console.error("Dashboard Error", error);
        return null;
    }
}

// =========================================================
// BACKEND STATUS
// =========================================================

let backendAvailable = true;

async function updateBackendStatus() {
    try {
        const health = await getBackendHealth();
        backendAvailable = health && (health.status === "ok" || health.success);
        console.log("Backend Health:", health, "Available:", backendAvailable);
        updateHealthIndicator(backendAvailable);
        return health;
    } catch (error) {
        backendAvailable = false;
        console.error("Backend health check failed:", error);
        updateHealthIndicator(false);
        return null;
    }
}

function updateHealthIndicator(available) {
    const indicator = document.getElementById("backendHealthIndicator");
    if (indicator) {
        indicator.className = available ? "health-indicator healthy" : "health-indicator unhealthy";
        indicator.textContent = available ? "● Backend Online" : "● Backend Offline";
    }
}

function isBackendAvailable() {
    return backendAvailable;
}

// =========================================================
// INITIALIZE (index / shared pages)
// =========================================================

window.addEventListener("load", async () => {
    console.log("Bamboo Force API layer initialized");
    await updateBackendStatus();
});

setInterval(updateBackendStatus, 10000);

// =========================================================
// GLOBAL EXPORTS
// =========================================================

window.API_BASE = API_BASE;
window.apiRequest = apiRequest;
window.getBackendHealth = getBackendHealth;
window.getAppHealth = getAppHealth;
window.verifyFace = verifyFace;
window.registerDriver = registerDriver;
window.checkLiveness = checkLiveness;
window.createRide = createRide;
window.getActiveRides = getActiveRides;
window.getActiveGroups = getActiveGroups;
window.getRecommendations = getRecommendations;
window.startRide = startRide;
window.completeRide = completeRide;
window.cancelRide = cancelRide;
window.getRideHistory = getRideHistory;
window.predictRideRisk = predictRideRisk;
window.getRiskHistory = getRiskHistory;
window.getLiveRiskStatus = getLiveRiskStatus;
window.analyzeDriverRisk = analyzeDriverRisk;
window.analyzeRouteRisk = analyzeRouteRisk;
window.loadDashboardData = loadDashboardData;
window.updateBackendStatus = updateBackendStatus;
window.isBackendAvailable = isBackendAvailable;

// =========================================================
// TOAST NOTIFICATION SYSTEM
// =========================================================

function showToast(message, type = 'info', duration = 3000) {
    // Create toast container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    // Add to container
    container.appendChild(toast);
    
    // Remove after duration
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

window.showToast = showToast;

// =========================================================
// PERIODIC REFRESH SYSTEM
// =========================================================

let refreshIntervals = [];

function startPeriodicRefresh(callback, intervalMs = 10000) {
    // Clear any existing interval for this callback
    stopPeriodicRefresh(callback);
    
    // Set up new interval
    const intervalId = setInterval(callback, intervalMs);
    refreshIntervals.push({ callback, intervalId });
    
    // Execute immediately
    callback();
    
    return intervalId;
}

function stopPeriodicRefresh(callback) {
    const index = refreshIntervals.findIndex(item => item.callback === callback);
    if (index !== -1) {
        clearInterval(refreshIntervals[index].intervalId);
        refreshIntervals.splice(index, 1);
    }
}

function stopAllPeriodicRefreshes() {
    refreshIntervals.forEach(item => clearInterval(item.intervalId));
    refreshIntervals = [];
}

window.startPeriodicRefresh = startPeriodicRefresh;
window.stopPeriodicRefresh = stopPeriodicRefresh;
window.stopAllPeriodicRefreshes = stopAllPeriodicRefreshes;
