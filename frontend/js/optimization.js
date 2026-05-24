// ======================================================
// BAMBOO FORCE AI — RIDE OPTIMIZATION UI
// Uses api.js wrappers; no duplicate fetch logic.
// ======================================================

const LOCATION_COORDINATES = {
    madhapur: [17.4483, 78.3915],
    "hitech city": [17.4435, 78.3772],
    gachibowli: [17.4401, 78.3489],
    kukatpally: [17.4948, 78.3996],
    ameerpet: [17.4375, 78.4482],
    "banjara hills": [17.4126, 78.4482],
    secunderabad: [17.4399, 78.4983],
};

// ======================================================
// UI HELPERS — loading / toast (uses existing CSS)
// ======================================================

function showRideToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    let icon = "fa-circle-check";
    if (type === "error") {
        icon = "fa-circle-xmark";
    } else if (type === "info") {
        icon = "fa-circle-info";
    }

    toast.innerHTML =
        '<motionless-div class="toast-content">' +
        '<i class="fa-solid ' + icon + '"></i>' +
        '<span>' + message + '</span>' +
        '</motionless-div>'.replace(/motionless-div/g, 'div');

    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add("show");
    });

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, 3200);
}

function setSectionLoading(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) {
        return;
    }

    const cardClass =
        containerId === "recommendationContainer"
            ? "recommendation-card"
            : "dashboard-card";

    container.innerHTML = `
        <div class="${cardClass}">
            <h3>${message}</h3>
        </div>
    `;
}

function setSubmitLoading(isLoading) {
    const btn = document.querySelector("#rideForm .submit-btn");
    if (!btn) {
        return;
    }

    btn.disabled = isLoading;

    if (isLoading) {
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Optimizing...';
    } else if (btn.dataset.originalText) {
        btn.innerHTML = btn.dataset.originalText;
    }
}

// ======================================================
// LOAD ACTIVE RIDES
// ======================================================

async function loadActiveRides() {
    const countEl = document.getElementById("activeRideCount");
    if (countEl) {
        countEl.innerText = "...";
    }

    try {
        const result = await getActiveRides();

        if (!result || !result.success) {
            if (countEl) {
                countEl.innerText = "—";
            }
            showRideToast(
                result?.error || "Failed to load active rides",
                "error"
            );
            return;
        }

        const rides = result.data || {};
        if (countEl) {
            countEl.innerText = String(Object.keys(rides).length);
        }
    } catch (error) {
        console.error(error);
        if (countEl) {
            countEl.innerText = "—";
        }
        showRideToast("Failed to load active rides", "error");
    }
}

// ======================================================
// LOAD GROUPS
// ======================================================

async function loadGroups() {
    setSectionLoading("groupsContainer", "Loading groups...");

    try {
        const result = await getActiveGroups();

        if (!result || !result.success) {
            renderGroups(null, result?.error);
            return;
        }

        renderGroups(result.data);
    } catch (error) {
        console.error(error);
        renderGroups(null, error.message);
    }
}

// ======================================================
// LOAD RECOMMENDATIONS
// ======================================================

async function loadRecommendations() {
    setSectionLoading(
        "recommendationContainer",
        "Loading recommendations..."
    );

    try {
        const result = await getRecommendations();

        if (!result || !result.success) {
            renderRecommendations(null, result?.error);
            return;
        }

        renderRecommendations(result.data);
    } catch (error) {
        console.error(error);
        renderRecommendations(null, error.message);
    }
}

// ======================================================
// REFRESH DASHBOARD
// ======================================================

async function refreshDashboard() {
    await Promise.all([
        loadActiveRides(),
        loadGroups(),
        loadRecommendations(),
    ]);
}

// ======================================================
// FORM SUBMIT
// ======================================================

document.getElementById("rideForm").addEventListener(
    "submit",
    async function (event) {
        event.preventDefault();

        const vehicleType =
            document.getElementById("vehicle_type").value;

        let passengerCount = 1;
        if (vehicleType === "AUTO") {
            passengerCount = 3;
        } else if (vehicleType === "CAB") {
            passengerCount = 4;
        } else if (vehicleType === "VAN") {
            passengerCount = 6;
        }

        const pickupLocation = document
            .getElementById("pickup_location")
            .value.toLowerCase()
            .trim();

        const destinationLocation = document
            .getElementById("destination_location")
            .value.toLowerCase()
            .trim();

        const source = LOCATION_COORDINATES[pickupLocation];
        const destination = LOCATION_COORDINATES[destinationLocation];

        if (!source || !destination) {
            showRideToast("Demo location not supported", "error");
            return;
        }

        const rideData = {
            ride_id: document.getElementById("ride_id").value,
            source: source,
            destination: destination,
            start_time: String(Date.now()),
            share_allowed: document.getElementById("share_allowed").checked,
            passenger_count: passengerCount,
        };

        setSubmitLoading(true);

        try {
            const result = await createRide(rideData);
            console.log("CREATE RESPONSE:", result);

            if (result && result.success) {
                showRideToast("AI Ride Optimization Complete", "success");
                document.getElementById("rideForm").reset();
                await refreshDashboard();
            } else {
                const msg =
                    result?.error ||
                    result?.detail ||
                    result?.message ||
                    "Backend error while creating ride";
                showRideToast(
                    typeof msg === "string" ? msg : JSON.stringify(msg),
                    "error"
                );
            }
        } catch (error) {
            console.error(error);
            showRideToast("Network error while creating ride", "error");
        } finally {
            setSubmitLoading(false);
        }
    }
);

// ======================================================
// RENDER GROUPS
// ======================================================

function renderGroups(groups, errorMessage) {
    const container = document.getElementById("groupsContainer");
    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (errorMessage) {
        container.innerHTML = `
            <div class="dashboard-card">
                <h3>Could not load groups</h3>
                <p>${errorMessage}</p>
            </div>
        `;
        return;
    }

    if (!groups || Object.keys(groups).length === 0) {
        container.innerHTML = `
            <div class="dashboard-card">
                <h3>No Groups Yet</h3>
                <p>Create a shared ride to see AI groups.</p>
            </div>
        `;
        return;
    }

    Object.entries(groups).forEach(([groupId, group]) => {
        const card = document.createElement("div");
        card.className = "dashboard-card";

        const vehicle =
            group.recommended_vehicle || group.vehicle || "—";
        const passengers =
            group.passenger_count ?? group.passengers ?? "—";
        const efficiency =
            group.cluster_efficiency ?? group.efficiency ?? "—";
        const chainReady =
            group.dynamic_chain_ready === true ? "Yes" : "No";

        card.innerHTML = `
            <h3>${groupId}</h3>
            <p>Vehicle: ${vehicle}</p>
            <p>Passengers: ${passengers}</p>
            <p>Efficiency: ${efficiency}</p>
            <p>Dynamic Chain: ${chainReady}</p>
        `;

        container.appendChild(card);
    });
}

// ======================================================
// RENDER RECOMMENDATIONS
// ======================================================

function renderRecommendations(data, errorMessage) {
    const container = document.getElementById("recommendationContainer");
    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (errorMessage) {
        container.innerHTML = `
            <div class="recommendation-card">
                <h3>Could not load recommendations</h3>
                <p>${errorMessage}</p>
            </div>
        `;
        return;
    }

    if (!data || !data.passenger_recommendations) {
        container.innerHTML = `
            <div class="recommendation-card">
                <h3>No Recommendations Yet</h3>
                <p>Create rides to receive AI suggestions.</p>
            </div>
        `;
        return;
    }

    data.passenger_recommendations.forEach((item) => {
        container.innerHTML += `
            <div class="recommendation-card">
                <h3>AI Ride Suggestion</h3>
                <p>
                    Recommended Vehicle:
                    <strong>${item.recommended_vehicle || "—"}</strong>
                </p>
                <p>
                    Action:
                    <strong>${item.vehicle_action || "—"}</strong>
                </p>
                <p>Reason: ${item.reason || "—"}</p>
                <p>
                    Traffic Reduction:
                    ${(
                        (item.traffic_reduction_score || 0) * 100
                    ).toFixed(0)}%
                </p>
                <p>
                    Cost Savings:
                    ₹${item.estimated_cost_savings ?? 0}
                </p>
                <p>
                    Ride Chain Potential:
                    ${item.ride_chain_potential ?? "—"}
                </p>
            </div>
        `;
    });
}

// ======================================================
// RIDE ACTION HANDLERS
// ======================================================

async function handleStartRide() {
    const rideId = document.getElementById("actionRideId").value;
    const resultBox = document.getElementById("rideActionResult");
    
    if (!rideId) {
        resultBox.innerHTML = `<p class="error">Please enter a Ride ID</p>`;
        return;
    }
    
    resultBox.innerHTML = `<p>Starting ride...</p>`;
    
    try {
        const result = await startRide(rideId);
        console.log("Start Ride Result:", result);
        
        if (result && result.success) {
            resultBox.innerHTML = `<p class="success">Ride ${rideId} started successfully</p>`;
            await refreshDashboard();
        } else {
            resultBox.innerHTML = `<p class="error">Failed to start ride: ${result?.error || "Unknown error"}</p>`;
        }
    } catch (error) {
        console.error("Start ride error:", error);
        resultBox.innerHTML = `<p class="error">Network error: ${error.message}</p>`;
    }
}

async function handleCompleteRide() {
    const rideId = document.getElementById("actionRideId").value;
    const resultBox = document.getElementById("rideActionResult");
    
    if (!rideId) {
        resultBox.innerHTML = `<p class="error">Please enter a Ride ID</p>`;
        return;
    }
    
    resultBox.innerHTML = `<p>Completing ride...</p>`;
    
    try {
        const result = await completeRide(rideId);
        console.log("Complete Ride Result:", result);
        
        if (result && result.success) {
            resultBox.innerHTML = `<p class="success">Ride ${rideId} completed successfully</p>`;
            await refreshDashboard();
        } else {
            resultBox.innerHTML = `<p class="error">Failed to complete ride: ${result?.error || "Unknown error"}</p>`;
        }
    } catch (error) {
        console.error("Complete ride error:", error);
        resultBox.innerHTML = `<p class="error">Network error: ${error.message}</p>`;
    }
}

async function handleCancelRide() {
    const rideId = document.getElementById("actionRideId").value;
    const resultBox = document.getElementById("rideActionResult");
    
    if (!rideId) {
        resultBox.innerHTML = `<p class="error">Please enter a Ride ID</p>`;
        return;
    }
    
    resultBox.innerHTML = `<p>Cancelling ride...</p>`;
    
    try {
        const result = await cancelRide(rideId);
        console.log("Cancel Ride Result:", result);
        
        if (result && result.success) {
            resultBox.innerHTML = `<p class="success">Ride ${rideId} cancelled successfully</p>`;
            await refreshDashboard();
        } else {
            resultBox.innerHTML = `<p class="error">Failed to cancel ride: ${result?.error || "Unknown error"}</p>`;
        }
    } catch (error) {
        console.error("Cancel ride error:", error);
        resultBox.innerHTML = `<p class="error">Network error: ${error.message}</p>`;
    }
}

async function handleRideHistory() {
    const resultBox = document.getElementById("rideActionResult");
    
    resultBox.innerHTML = `<p>Loading ride history...</p>`;
    
    try {
        const result = await getRideHistory();
        console.log("Ride History Result:", result);
        
        if (result && result.success) {
            const history = result.data || result;
            const historyHtml = Object.entries(history).map(([rideId, ride]) => {
                const status = ride.status || "Unknown";
                const statusClass = status.toLowerCase();
                return `
                    <div class="ride-item">
                        <strong>${rideId}</strong>
                        <span class="status-badge ${statusClass}">${status}</span>
                    </div>
                `;
            }).join("");
            resultBox.innerHTML = `<div class="history-list"><h3>Ride History</h3>${historyHtml}</div>`;
        } else {
            resultBox.innerHTML = `<p class="error">Failed to load history: ${result?.error || "Unknown error"}</p>`;
        }
    } catch (error) {
        console.error("Ride history error:", error);
        resultBox.innerHTML = `<p class="error">Network error: ${error.message}</p>`;
    }
}

// ======================================================
// INITIAL LOAD
// ======================================================

document.addEventListener("DOMContentLoaded", () => {
    refreshDashboard();
});
