// =========================================================
// BAMBOO FORCE AI
// FINAL PRODUCTION-READY FRONTEND SCRIPT
// =========================================================

// =========================================================
// CONFIGURATION
// =========================================================

const API_BASE_URL =
    "http://127.0.0.1:5000/api/ride";

const AUTO_REFRESH_INTERVAL = 5000;

// =========================================================
// DOM ELEMENTS
// =========================================================

const rideForm = document.getElementById(
    "rideForm"
);

const groupsContainer = document.getElementById(
    "groupsContainer"
);

const recommendationContainer = document.getElementById(
    "recommendationContainer"
);

const activeRideCount = document.getElementById(
    "activeRideCount"
);

// =========================================================
// APP STATE
// =========================================================

let autoRefresh = null;

// =========================================================
// TOAST SYSTEM
// =========================================================

function showToast(

    message,
    type = "success"
) {

    const existingToast = document.querySelector(
        ".toast"
    );

    if (existingToast) {

        existingToast.remove();
    }

    const toast = document.createElement(
        "div"
    );

    toast.className = `toast ${type}`;

    toast.innerHTML = `

        <div class="toast-content">

            <span>
                ${message}
            </span>

        </div>
    `;

    document.body.appendChild(
        toast
    );

    requestAnimationFrame(() => {

        toast.classList.add(
            "show"
        );
    });

    setTimeout(() => {

        toast.classList.remove(
            "show"
        );

        setTimeout(() => {

            toast.remove();

        }, 400);

    }, 3500);
}

// =========================================================
// LOADING BUTTON
// =========================================================

function setButtonLoading(

    button,
    isLoading,
    loadingText = "Loading..."
) {

    if (isLoading) {

        button.dataset.originalText =
            button.innerHTML;

        button.innerHTML = `

            ${loadingText}
        `;

        button.disabled = true;

    } else {

        button.innerHTML =
            button.dataset.originalText;

        button.disabled = false;
    }
}

// =========================================================
// API REQUEST
// =========================================================

async function apiRequest(

    endpoint,
    method = "GET",
    body = null
) {

    try {

        const options = {

            method,

            headers: {

                "Content-Type":
                    "application/json"
            }
        };

        if (body) {

            options.body = JSON.stringify(
                body
            );
        }

        const response = await fetch(

            `${API_BASE_URL}${endpoint}`,

            options
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(

                data.message
                || "Request failed"
            );
        }

        return data;

    } catch (error) {

        console.error(
            "API ERROR:",
            error
        );

        showToast(

            error.message
            || "Backend connection failed",

            "error"
        );

        return null;
    }
}

// =========================================================
// VALIDATE FORM DATA
// =========================================================

function validateRideData(data) {

    if (!data.ride_id.trim()) {

        showToast(
            "Ride ID required",
            "error"
        );

        return false;
    }

    if (data.passenger_count <= 0) {

        showToast(
            "Passenger count invalid",
            "error"
        );

        return false;
    }

    const locations = [

        ...data.source,
        ...data.destination
    ];

    for (const value of locations) {

        if (isNaN(value)) {

            showToast(
                "Invalid location coordinates",
                "error"
            );

            return false;
        }
    }

    return true;
}

// =========================================================
// CREATE SMART RIDE
// =========================================================

async function createRide(event) {

    event.preventDefault();

    const submitButton = document.querySelector(
        ".submit-btn"
    );

    // =====================================================
    // BUILD PAYLOAD
    // =====================================================

    const rideData = {

        ride_id: document.getElementById(
            "ride_id"
        ).value.trim(),

        passenger_count: parseInt(

            document.getElementById(
                "passenger_count"
            ).value
        ),

        source: [

            parseFloat(

                document.getElementById(
                    "source_lat"
                ).value
            ),

            parseFloat(

                document.getElementById(
                    "source_lon"
                ).value
            )
        ],

        destination: [

            parseFloat(

                document.getElementById(
                    "dest_lat"
                ).value
            ),

            parseFloat(

                document.getElementById(
                    "dest_lon"
                ).value
            )
        ],

        start_time: Math.floor(
            Date.now() / 1000
        ),

        share_allowed: document.getElementById(
            "share_allowed"
        ).checked
    };

    // =====================================================
    // VALIDATION
    // =====================================================

    if (!validateRideData(rideData)) {

        return;
    }

    // =====================================================
    // LOADING STATE
    // =====================================================

    setButtonLoading(

        submitButton,

        true,

        "Optimizing Ride..."
    );

    // =====================================================
    // CREATE RIDE
    // =====================================================

    const result = await apiRequest(

        "/create_ride",

        "POST",

        rideData
    );

    // =====================================================
    // RESET BUTTON
    // =====================================================

    setButtonLoading(

        submitButton,

        false
    );

    // =====================================================
    // HANDLE RESPONSE
    // =====================================================

    if (result?.success) {

        showToast(

            "Smart Ride Created Successfully 🚀"
        );

        rideForm.reset();

        await loadDashboard();

    } else {

        showToast(

            result?.message
            || "Ride creation failed",

            "error"
        );
    }
}

// =========================================================
// LOAD ACTIVE RIDES
// =========================================================

async function loadActiveRides() {

    const result = await apiRequest(
        "/active_rides"
    );

    if (

        !result
        || !result.success
        || !result.data

    ) {

        activeRideCount.textContent = "0";

        return;
    }

    const rides = Object.values(
        result.data
    );

    activeRideCount.textContent =
        rides.length;
}

// =========================================================
// LOAD ACTIVE GROUPS
// =========================================================

async function loadGroups() {

    const result = await apiRequest(
        "/active_groups"
    );

    if (

        !result
        || !result.success
        || !result.data

    ) {

        groupsContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    No Smart Groups Yet
                </h3>

                <p>

                    Create rides to activate
                    AI ride orchestration.

                </p>

            </div>
        `;

        return;
    }

    const groups = Object.values(
        result.data
    );

    if (groups.length === 0) {

        groupsContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    Waiting For Optimization
                </h3>

                <p>

                    Smart ride groups
                    will appear here.

                </p>

            </div>
        `;

        return;
    }

    groupsContainer.innerHTML = "";

    groups.forEach(group => {

        const card = document.createElement(
            "div"
        );

        card.className = "dynamic-card";

        card.innerHTML = `

            <div class="card-header">

                <h3>
                    ${group.cluster_id || "Cluster"}
                </h3>

                <span class="live-badge">

                    LIVE

                </span>

            </div>

            <div class="group-details">

                <div class="detail-item">

                    <span>
                        Vehicle
                    </span>

                    <strong>
                        ${group.recommended_vehicle || "AUTO"}
                    </strong>

                </div>

                <div class="detail-item">

                    <span>
                        Passengers
                    </span>

                    <strong>
                        ${group.passenger_count || 0}
                    </strong>

                </div>

                <div class="detail-item">

                    <span>
                        Optimization
                    </span>

                    <strong>

                        ${(
                            (
                                group.optimization_score
                                || 0
                            ) * 100
                        ).toFixed(1)}%

                    </strong>

                </div>

            </div>
        `;

        groupsContainer.appendChild(
            card
        );
    });
}

// =========================================================
// LOAD RECOMMENDATIONS
// =========================================================

async function loadRecommendations() {

    const result = await apiRequest(
        "/recommendations"
    );

    if (

        !result
        || !result.success
        || !result.data

    ) {

        recommendationContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    AI Recommendations Pending
                </h3>

                <p>

                    Recommendations
                    will appear here.

                </p>

            </div>
        `;

        return;
    }

    const recommendations = (

        result.data
        ?.passenger_recommendations

        || []
    );

    if (!recommendations.length) {

        recommendationContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    No Recommendations Yet
                </h3>

            </div>
        `;

        return;
    }

    recommendationContainer.innerHTML = "";

    recommendations.forEach(item => {

        const card = document.createElement(
            "div"
        );

        card.className =
            "recommendation-card";

        card.innerHTML = `

            <div class="recommendation-top">

                <h3>
                    ${item.group_id || "Group"}
                </h3>

                <span class="confidence-score">

                    ${(
                        (
                            item.confidence_score
                            || 0
                        ) * 100
                    ).toFixed(0)}%
                    Match

                </span>

            </div>

            <div class="recommendation-body">

                <div class="recommend-item">

                    <span>
                        Vehicle
                    </span>

                    <strong>
                        ${item.recommended_vehicle || "AUTO"}
                    </strong>

                </div>

                <div class="recommend-item">

                    <span>
                        Savings
                    </span>

                    <strong>

                        ₹${item.estimated_cost_savings || 0}

                    </strong>

                </div>

                <div class="recommend-item">

                    <span>
                        Traffic Reduction
                    </span>

                    <strong>

                        ${(
                            (
                                item.traffic_reduction_score
                                || 0
                            ) * 100
                        ).toFixed(0)}%

                    </strong>

                </div>

            </div>
        `;

        recommendationContainer.appendChild(
            card
        );
    });
}

// =========================================================
// LOAD FULL DASHBOARD
// =========================================================

async function loadDashboard() {

    await Promise.all([

        loadActiveRides(),

        loadGroups(),

        loadRecommendations()
    ]);
}

// =========================================================
// AUTO REFRESH
// =========================================================

function startAutoRefresh() {

    if (autoRefresh) {

        clearInterval(autoRefresh);
    }

    autoRefresh = setInterval(() => {

        loadDashboard();

    }, AUTO_REFRESH_INTERVAL);
}

// =========================================================
// SMOOTH SCROLL
// =========================================================

function initializeSmoothScroll() {

    const links = document.querySelectorAll(
        'a[href^="#"]'
    );

    links.forEach(link => {

        link.addEventListener(

            "click",

            event => {

                event.preventDefault();

                const target = document.querySelector(

                    link.getAttribute(
                        "href"
                    )
                );

                if (target) {

                    target.scrollIntoView({

                        behavior: "smooth"
                    });
                }
            }
        );
    });
}

// =========================================================
// INITIALIZE APP
// =========================================================

function initializeApp() {

    // =====================================================
    // FORM EVENT
    // =====================================================

    if (rideForm) {

        rideForm.addEventListener(

            "submit",

            createRide
        );
    }

    // =====================================================
    // INITIAL DASHBOARD LOAD
    // =====================================================

    loadDashboard();

    // =====================================================
    // AUTO REFRESH
    // =====================================================

    startAutoRefresh();

    // =====================================================
    // TAB VISIBILITY OPTIMIZATION
    // =====================================================

    document.addEventListener(

        "visibilitychange",

        () => {

            if (document.hidden) {

                clearInterval(
                    autoRefresh
                );

            } else {

                startAutoRefresh();
            }
        }
    );

    // =====================================================
    // SMOOTH SCROLL
    // =====================================================

    initializeSmoothScroll();

    // =====================================================
    // WELCOME MESSAGE
    // =====================================================

    setTimeout(() => {

        showToast(

            "Welcome to Bamboo Force AI 🚀"
        );

    }, 1000);

    console.log(

        "Bamboo Force AI Initialized"
    );
}

// =========================================================
// START APPLICATION
// =========================================================

document.addEventListener(

    "DOMContentLoaded",

    initializeApp
);