// =========================================================
// BAMBOO FORCE DASHBOARD INTERACTIVITY
// =========================================================

// =========================================================
// MODAL SYSTEM
// =========================================================

function openModal(title, content) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    modalOverlay.classList.add('active');
}

function closeModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.classList.remove('active');
}

// Close modal on overlay click
document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// =========================================================
// ACTIVE RIDES MODAL
// =========================================================

async function showActiveRidesModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-spinner fa-spin"></i><p>Loading active rides...</p></div>';
    openModal('Active Rides', '');
    
    try {
        const rides = await getActiveRides();
        if (rides && (rides.success || rides.data)) {
            const activeRides = rides.data || rides;
            const rideKeys = Object.keys(activeRides);
            
            if (rideKeys.length === 0) {
                modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-car"></i><p>No active rides at the moment</p></div>';
                return;
            }
            
            let content = '';
            rideKeys.forEach(rideId => {
                const ride = activeRides[rideId];
                content += `
                    <div class="modal-item">
                        <h4>Ride ${rideId}</h4>
                        <p>Status: <span class="modal-item-value status-badge active">${ride.status || 'Active'}</span></p>
                        <p>Pickup: <span class="modal-item-value">${ride.pickup || 'N/A'}</span></p>
                        <p>Destination: <span class="modal-item-value">${ride.destination || 'N/A'}</span></p>
                    </div>
                `;
            });
            
            modalBody.innerHTML = content;
        } else {
            modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Failed to load active rides</p></div>';
        }
    } catch (error) {
        console.error('Error loading active rides:', error);
        modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Error loading active rides</p></div>';
    }
}

// =========================================================
// VERIFIED DRIVERS MODAL
// =========================================================

async function showVerifiedDriversModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-spinner fa-spin"></i><p>Loading verified drivers...</p></div>';
    openModal('Verified Drivers', '');
    
    try {
        // Since we don't have a direct API for verified drivers list,
        // we'll show a placeholder with the current count
        const count = document.getElementById('verifiedDriversCount').textContent;
        
        let content = `
            <div class="modal-item">
                <h4>Verified Drivers Count</h4>
                <p>Total: <span class="modal-item-value">${count}</span></p>
                <p>Driver verification is managed through the Driver Portal and Verification modules.</p>
            </div>
            <div class="modal-item">
                <h4>Quick Actions</h4>
                <p><a href="pages/user_verification.html" style="color: #00d4ff;">Go to Verification Module</a></p>
                <p><a href="pages/driver_portal.html" style="color: #00d4ff;">Go to Driver Portal</a></p>
            </div>
        `;
        
        modalBody.innerHTML = content;
    } catch (error) {
        console.error('Error loading verified drivers:', error);
        modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Error loading verified drivers</p></div>';
    }
}

// =========================================================
// RISK ALERTS MODAL
// =========================================================

async function showRiskAlertsModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-spinner fa-spin"></i><p>Loading risk alerts...</p></div>';
    openModal('Risk Alerts', '');
    
    try {
        const riskHistory = await getRiskHistory();
        if (riskHistory && (riskHistory.success || riskHistory.data)) {
            const history = riskHistory.data || riskHistory;
            const historyKeys = Object.keys(history);
            
            if (historyKeys.length === 0) {
                modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-shield-halved"></i><p>No risk alerts at the moment</p></div>';
                return;
            }
            
            let content = '';
            historyKeys.slice(0, 10).forEach(key => {
                const risk = history[key];
                const riskLevel = risk.risk_level || risk.riskLevel || 'LOW';
                const badgeClass = riskLevel.toLowerCase() === 'high' ? 'high' : 
                                   riskLevel.toLowerCase() === 'medium' ? 'medium' : 'low';
                
                content += `
                    <div class="modal-item">
                        <h4>Risk Assessment #${key}</h4>
                        <p>Risk Level: <span class="modal-item-value risk-badge ${badgeClass}">${riskLevel}</span></p>
                        <p>Score: <span class="modal-item-value">${risk.score || risk.risk_score || 'N/A'}</span></p>
                        <p>Timestamp: <span class="modal-item-value">${risk.timestamp || 'N/A'}</span></p>
                    </div>
                `;
            });
            
            modalBody.innerHTML = content;
        } else {
            modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Failed to load risk alerts</p></div>';
        }
    } catch (error) {
        console.error('Error loading risk alerts:', error);
        modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Error loading risk alerts</p></div>';
    }
}

// =========================================================
// TRAFFIC REDUCTION MODAL
// =========================================================

async function showTrafficReductionModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-spinner fa-spin"></i><p>Loading traffic insights...</p></div>';
    openModal('Traffic Reduction Insights', '');
    
    try {
        const groups = await getActiveGroups();
        if (groups && (groups.success || groups.data)) {
            const activeGroups = groups.data || groups;
            const groupKeys = Object.keys(activeGroups);
            
            let content = `
                <div class="modal-item">
                    <h4>Optimization Impact</h4>
                    <p>Traffic Reduced: <span class="modal-item-value">${document.getElementById('trafficReducedCount').textContent}</span></p>
                    <p>Active Ride Groups: <span class="modal-item-value">${groupKeys.length}</span></p>
                </div>
            `;
            
            if (groupKeys.length > 0) {
                content += '<div class="modal-item"><h4>Active Ride Groups</h4>';
                groupKeys.slice(0, 5).forEach(groupId => {
                    const group = activeGroups[groupId];
                    content += `
                        <p>Group ${groupId}: <span class="modal-item-value">${group.rides ? group.rides.length : 0} rides</span></p>
                    `;
                });
                content += '</div>';
            }
            
            content += `
                <div class="modal-item">
                    <h4>Quick Actions</h4>
                    <p><a href="pages/ride_optimization.html" style="color: #00d4ff;">Go to Ride Optimization</a></p>
                </div>
            `;
            
            modalBody.innerHTML = content;
        } else {
            modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Failed to load traffic insights</p></div>';
        }
    } catch (error) {
        console.error('Error loading traffic insights:', error);
        modalBody.innerHTML = '<div class="modal-empty"><i class="fa-solid fa-exclamation-triangle"></i><p>Error loading traffic insights</p></div>';
    }
}

// =========================================================
// REALTIME DASHBOARD UPDATES
// =========================================================

let dashboardRefreshInterval = null;

async function updateDashboardMetrics() {
    try {
        // Update Active Rides
        const rides = await getActiveRides();
        if (rides && (rides.success || rides.data)) {
            const activeRides = rides.data || rides;
            const rideCount = Object.keys(activeRides).length;
            const activeRidesEl = document.getElementById('activeRidesCount');
            if (activeRidesEl) {
                activeRidesEl.classList.add('updating');
                setTimeout(() => {
                    activeRidesEl.textContent = rideCount;
                    activeRidesEl.classList.remove('updating');
                }, 250);
            }
        }
        
        // Update Risk Alerts
        const riskHistory = await getRiskHistory();
        if (riskHistory && (riskHistory.success || riskHistory.data)) {
            const history = riskHistory.data || riskHistory;
            const highRiskCount = Object.values(history).filter(r => 
                (r.risk_level || r.riskLevel || '').toLowerCase() === 'high'
            ).length;
            const riskAlertsEl = document.getElementById('riskAlertsCount');
            if (riskAlertsEl) {
                riskAlertsEl.classList.add('updating');
                setTimeout(() => {
                    riskAlertsEl.textContent = highRiskCount;
                    riskAlertsEl.classList.remove('updating');
                }, 250);
            }
        }
        
        // Update Traffic Reduction (simulated based on groups)
        const groups = await getActiveGroups();
        if (groups && (groups.success || groups.data)) {
            const activeGroups = groups.data || groups;
            const groupCount = Object.keys(activeGroups).length;
            const trafficReducedEl = document.getElementById('trafficReducedCount');
            if (trafficReducedEl) {
                trafficReducedEl.classList.add('updating');
                setTimeout(() => {
                    // Simulated calculation: more groups = more traffic reduction
                    const reduction = Math.min(50, 20 + (groupCount * 3));
                    trafficReducedEl.textContent = reduction + '%';
                    trafficReducedEl.classList.remove('updating');
                }, 250);
            }
        }
        
    } catch (error) {
        console.error('Error updating dashboard metrics:', error);
    }
}

function startDashboardRefresh() {
    // Clear existing interval if any
    if (dashboardRefreshInterval) {
        clearInterval(dashboardRefreshInterval);
    }
    
    // Update immediately
    updateDashboardMetrics();
    
    // Set up periodic refresh every 15 seconds
    dashboardRefreshInterval = setInterval(updateDashboardMetrics, 15000);
}

function stopDashboardRefresh() {
    if (dashboardRefreshInterval) {
        clearInterval(dashboardRefreshInterval);
        dashboardRefreshInterval = null;
    }
}

// =========================================================
// INITIALIZATION
// =========================================================

document.addEventListener('DOMContentLoaded', () => {
    // Start realtime dashboard updates
    startDashboardRefresh();
});

// =========================================================
// GLOBAL EXPORTS
// =========================================================

window.openModal = openModal;
window.closeModal = closeModal;
window.showActiveRidesModal = showActiveRidesModal;
window.showVerifiedDriversModal = showVerifiedDriversModal;
window.showRiskAlertsModal = showRiskAlertsModal;
window.showTrafficReductionModal = showTrafficReductionModal;
window.updateDashboardMetrics = updateDashboardMetrics;
window.startDashboardRefresh = startDashboardRefresh;
window.stopDashboardRefresh = stopDashboardRefresh;
