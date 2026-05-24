// =====================================================
// RISK PREDICTION UI
// =====================================================

async function runRiskPrediction() {
    console.log("[DEBUG] runRiskPrediction() called");
    const input = document.getElementById("risk_passenger_count");
    const riskBox = document.getElementById("riskResult");
    const button = document.querySelector(
        ".risk-section button"
    );

    console.log("[DEBUG] Elements:", { input: !!input, riskBox: !!riskBox, button: !!button });

    if (!input || !riskBox) {
        console.error("[DEBUG] Required elements not found");
        return;
    }

    const passengerCount = parseInt(input.value, 10);
    console.log("[DEBUG] Passenger count:", passengerCount);

    if (Number.isNaN(passengerCount) || passengerCount < 1) {
        console.error("[DEBUG] Invalid passenger count");
        riskBox.innerHTML = "<h3>Enter a valid passenger count</h3>";
        return;
    }

    if (button) {
        button.disabled = true;
        button.textContent = "Predicting...";
    }

    riskBox.innerHTML = "<p>Loading prediction...</p>";

    try {
        console.log("[DEBUG] Calling predictRideRisk API...");
        const result = await predictRideRisk({
            passenger_count: passengerCount,
        });

        console.log("[DEBUG] Risk prediction result:", result);

        if (result && result.success) {
            riskBox.innerHTML = `
                <h3>Risk Level: ${result.risk_level || "Unknown"}</h3>
                ${
                    result.note
                        ? `<p>${result.note}</p>`
                        : ""
                }
            `;
        } else {
            console.error("[DEBUG] Prediction failed:", result);
            riskBox.innerHTML = `
                <h3>Prediction Failed</h3>
                <p>${result?.error || result?.detail || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Risk prediction error:", error);
        riskBox.innerHTML = `
            <h3>Prediction Failed</h3>
            <p>${error.message || "Network error"}</p>
        `;
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Predict Risk";
        }
    }
}

window.runRiskPrediction = runRiskPrediction;

// =====================================================
// DRIVER RISK ANALYSIS
// =====================================================

async function analyzeDriverRisk() {
    console.log("[DEBUG] analyzeDriverRisk() called");
    const driverId = document.getElementById("driverId").value;
    const resultBox = document.getElementById("driverRiskResult");
    const button = document.querySelector(".risk-section button");

    console.log("[DEBUG] driverId:", driverId);

    if (!driverId) {
        console.error("[DEBUG] No driver ID provided");
        resultBox.innerHTML = "<h3>Enter a Driver ID</h3>";
        return;
    }

    if (button) {
        button.disabled = true;
        button.textContent = "Analyzing...";
    }

    resultBox.innerHTML = "<p>Running driver risk analysis...</p>";

    try {
        console.log("[DEBUG] Calling analyzeDriverRisk API...");
        const result = await window.analyzeDriverRisk({ driver_id: driverId });

        console.log("[DEBUG] Driver risk analysis result:", result);

        if (result && result.success) {
            const riskLevel = result.risk_level || "Unknown";
            const riskClass = riskLevel.toLowerCase();
            resultBox.innerHTML = `
                <h3>Driver Risk Analysis</h3>
                <span class="risk-badge ${riskClass}">${riskLevel}</span>
                ${result.note ? `<p>${result.note}</p>` : ""}
            `;
        } else {
            console.error("[DEBUG] Analysis failed:", result);
            resultBox.innerHTML = `
                <h3>Analysis Failed</h3>
                <p>${result?.error || result?.detail || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Driver risk analysis error:", error);
        resultBox.innerHTML = `
            <h3>Analysis Failed</h3>
            <p>${error.message || "Network error"}</p>
        `;
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Analyze Driver Risk";
        }
    }
}

window.analyzeDriverRisk = analyzeDriverRisk;

// =====================================================
// ROUTE RISK ANALYSIS
// =====================================================

async function analyzeRouteRisk() {
    console.log("[DEBUG] analyzeRouteRisk() called");
    const routeId = document.getElementById("routeId").value;
    const resultBox = document.getElementById("routeRiskResult");
    const button = document.querySelectorAll(".risk-section button")[1];

    console.log("[DEBUG] routeId:", routeId);

    if (!routeId) {
        console.error("[DEBUG] No route ID provided");
        resultBox.innerHTML = "<h3>Enter a Route ID</h3>";
        return;
    }

    if (button) {
        button.disabled = true;
        button.textContent = "Analyzing...";
    }

    resultBox.innerHTML = "<p>Running route risk analysis...</p>";

    try {
        console.log("[DEBUG] Calling analyzeRouteRisk API...");
        const result = await window.analyzeRouteRisk({ route_id: routeId });

        console.log("[DEBUG] Route risk analysis result:", result);

        if (result && result.success) {
            const riskLevel = result.risk_level || "Unknown";
            const riskClass = riskLevel.toLowerCase();
            resultBox.innerHTML = `
                <h3>Route Risk Analysis</h3>
                <span class="risk-badge ${riskClass}">${riskLevel}</span>
                ${result.note ? `<p>${result.note}</p>` : ""}
            `;
        } else {
            console.error("[DEBUG] Analysis failed:", result);
            resultBox.innerHTML = `
                <h3>Analysis Failed</h3>
                <p>${result?.error || result?.detail || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Route risk analysis error:", error);
        resultBox.innerHTML = `
            <h3>Analysis Failed</h3>
            <p>${error.message || "Network error"}</p>
        `;
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Analyze Route Risk";
        }
    }
}

window.analyzeRouteRisk = analyzeRouteRisk;

// =====================================================
// LIVE RISK STATUS
// =====================================================

async function getLiveRisk() {
    console.log("[DEBUG] getLiveRisk() called");
    const resultBox = document.getElementById("liveRiskResult");
    const button = document.querySelectorAll(".risk-section button")[2];

    if (button) {
        button.disabled = true;
        button.textContent = "Loading...";
    }

    resultBox.innerHTML = "<p>Loading live risk status...</p>";

    try {
        console.log("[DEBUG] Calling getLiveRiskStatus API...");
        const result = await window.getLiveRiskStatus();

        console.log("[DEBUG] Live risk status result:", result);

        if (result && result.success) {
            const status = result.status || "Unknown";
            const riskLevel = result.risk_level || "N/A";
            const riskClass = riskLevel.toLowerCase() !== "na" ? riskLevel.toLowerCase() : "medium";
            resultBox.innerHTML = `
                <h3>Live Risk Status</h3>
                <p>Status: <span class="status-badge active">${status}</span></p>
                <p>Risk Level: <span class="risk-badge ${riskClass}">${riskLevel}</span></p>
            `;
        } else {
            console.error("[DEBUG] Failed to get live risk:", result);
            resultBox.innerHTML = `
                <h3>Failed</h3>
                <p>${result?.error || result?.detail || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Live risk status error:", error);
        resultBox.innerHTML = `
            <h3>Failed</h3>
            <p>${error.message || "Network error"}</p>
        `;
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Get Live Risk Status";
        }
    }
}

window.getLiveRisk = getLiveRisk;

// =====================================================
// RISK HISTORY
// =====================================================

async function getRiskHistory() {
    console.log("[DEBUG] getRiskHistory() called");
    const resultBox = document.getElementById("riskHistoryResult");
    const button = document.querySelectorAll(".risk-section button")[3];

    if (button) {
        button.disabled = true;
        button.textContent = "Loading...";
    }

    resultBox.innerHTML = "<p>Loading risk history...</p>";

    try {
        console.log("[DEBUG] Calling getRiskHistory API...");
        const result = await window.getRiskHistory();

        console.log("[DEBUG] Risk history result:", result);

        if (result && result.success) {
            const history = result.data || result;
            const historyHtml = Object.entries(history).map(([key, value]) => {
                const riskLevel = value.risk_level || "Unknown";
                const riskClass = riskLevel.toLowerCase();
                return `
                    <div class="history-item">
                        <strong>${key}</strong>
                        <span class="risk-badge ${riskClass}">${riskLevel}</span>
                    </div>
                `;
            }).join("");
            resultBox.innerHTML = `<div class="history-list"><h3>Risk History</h3>${historyHtml}</div>`;
        } else {
            console.error("[DEBUG] Failed to get risk history:", result);
            resultBox.innerHTML = `
                <h3>Failed</h3>
                <p>${result?.error || result?.detail || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        console.error("[DEBUG] Risk history error:", error);
        resultBox.innerHTML = `
            <h3>Failed</h3>
            <p>${error.message || "Network error"}</p>
        `;
    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Get Risk History";
        }
    }
}

window.getRiskHistory = getRiskHistory;
