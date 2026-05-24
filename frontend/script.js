// =========================================================
// BAMBOO FORCE AI
// ULTIMATE INTERACTION SYSTEM
// =========================================================

document.addEventListener(

    "DOMContentLoaded",

    () => {

        initializeDashboard();
    }
);

// =========================================================
// INITIALIZE DASHBOARD
// =========================================================

function initializeDashboard() {

    animateMetrics();

    initializeQuickActions();

    initializeModuleButtons();

    rotateSystemStatus();

    showWelcomeToast();

    initializeHoverEffects();
}

// =========================================================
// SECTION NAVIGATION
// =========================================================

function showSection(

    sectionId,
    event = null
) {

    const sections = document.querySelectorAll(
        ".content-section"
    );

    sections.forEach(section => {

        section.classList.remove(
            "active-section"
        );
    });

    const selectedSection = document.getElementById(
        sectionId
    );

    if (selectedSection) {

        selectedSection.classList.add(
            "active-section"
        );
    }

    // =====================================================
    // UPDATE NAVIGATION
    // =====================================================

    const navItems = document.querySelectorAll(
        ".nav-item"
    );

    navItems.forEach(item => {

        item.classList.remove(
            "active"
        );
    });

    if (event) {

        event.currentTarget.classList.add(
            "active"
        );
    }

    // =====================================================
    // SCROLL TO TOP
    // =====================================================

    window.scrollTo({

        top: 0,

        behavior: "smooth"
    });

    // =====================================================
    // TOAST FEEDBACK
    // =====================================================

    const sectionNames = {

        dashboardSection:
            "Dashboard Loaded",

        safetySection:
            "AI Safety Systems Activated",

        riskSection:
            "Risk Intelligence Monitoring",

        optimizationSection:
            "Optimization Engine Ready",

        analyticsSection:
            "Analytics Dashboard Loaded"
    };

    showToast(

        sectionNames[sectionId] ||

        "Section Opened",

        "success"
    );
}

// =========================================================
// METRIC ANIMATION
// =========================================================

function animateMetrics() {

    const metricBoxes = document.querySelectorAll(
        ".metric-box p"
    );

    metricBoxes.forEach(metric => {

        const finalValue = metric.innerText;

        let numericValue =
            parseInt(
                finalValue.replace(/\D/g, "")
            );

        let current = 0;

        const increment =
            Math.ceil(numericValue / 40);

        metric.innerText = "0";

        const counter = setInterval(() => {

            current += increment;

            if (current >= numericValue) {

                current = numericValue;

                clearInterval(counter);
            }

            if (finalValue.includes("%")) {

                metric.innerText =
                    current + "%";
            }

            else {

                metric.innerText =
                    current;
            }

        }, 35);
    });
}

// =========================================================
// QUICK ACTIONS
// =========================================================

function initializeQuickActions() {

    const quickButtons = document.querySelectorAll(
        ".quick-btn"
    );

    quickButtons.forEach(button => {

        button.addEventListener(

            "click",

            () => {

                const text =
                    button.innerText;

                simulateAIProcess(text);
            }
        );
    });
}

// =========================================================
// MODULE BUTTONS
// =========================================================

function initializeModuleButtons() {

    const moduleButtons = document.querySelectorAll(
        ".module-btn"
    );

    moduleButtons.forEach(button => {

        button.addEventListener(

            "click",

            () => {

                simulateAIProcess(
                    button.innerText
                );
            }
        );
    });
}

// =========================================================
// AI PROCESS SIMULATION
// =========================================================

function simulateAIProcess(actionName) {

    const launchButton =
        document.querySelector(
            ".launch-btn"
        );

    const originalText =
        launchButton.innerHTML;

    // =====================================================
    // LOADING STATE
    // =====================================================

    launchButton.innerHTML = `

        <i class="fa-solid fa-spinner fa-spin"></i>

        AI Processing...
    `;

    launchButton.disabled = true;

    showToast(

        `Running ${actionName}...`,

        "info"
    );

    // =====================================================
    // PROCESS COMPLETE
    // =====================================================

    setTimeout(() => {

        launchButton.innerHTML =
            originalText;

        launchButton.disabled = false;

        const successMessages = [

            "AI operation completed",

            "System analysis successful",

            "AI workflow executed",

            "Optimization completed",

            "Verification successful"
        ];

        const randomMessage =

            successMessages[
                Math.floor(
                    Math.random() *
                    successMessages.length
                )
            ];

        showToast(

            randomMessage,

            "success"
        );

    }, 2500);
}

// =========================================================
// TOAST SYSTEM
// =========================================================

function showToast(

    message,
    type = "success"
) {

    const toast = document.createElement(
        "div"
    );

    toast.className =
        `toast toast-${type}`;

    let icon = "fa-circle-check";

    if (type === "error") {

        icon =
            "fa-circle-xmark";
    }

    if (type === "info") {

        icon =
            "fa-circle-info";
    }

    toast.innerHTML = `

        <i class="fa-solid ${icon}"></i>

        <span>

            ${message}

        </span>
    `;

    document.body.appendChild(
        toast
    );

    setTimeout(() => {

        toast.classList.add(
            "show-toast"
        );

    }, 100);

    setTimeout(() => {

        toast.classList.remove(
            "show-toast"
        );

        setTimeout(() => {

            toast.remove();

        }, 400);

    }, 3200);
}

// =========================================================
// WELCOME TOAST
// =========================================================

function showWelcomeToast() {

    setTimeout(() => {

        showToast(

            "Bamboo Force AI Initialized",

            "success"
        );

    }, 900);
}

// =========================================================
// SYSTEM STATUS ROTATION
// =========================================================

function rotateSystemStatus() {

    const statusMessages = [

        "Optimization Engine Active",

        "Risk Monitoring Online",

        "Face Verification Ready",

        "Traffic Intelligence Running",

        "AI Mobility Systems Stable"
    ];

    const systemItems =
        document.querySelectorAll(
            ".system-item"
        );

    let currentIndex = 0;

    setInterval(() => {

        systemItems.forEach(

            (item, index) => {

                item.style.opacity =
                    "0";

                setTimeout(() => {

                    item.innerHTML = `

                        <span class="system-dot"></span>

                        ${statusMessages[
                            (currentIndex + index)
                            %
                            statusMessages.length
                        ]}
                    `;

                    item.style.opacity =
                        "1";

                }, 300);
            }
        );

        currentIndex++;

    }, 4000);
}

// =========================================================
// CARD HOVER INTERACTIONS
// =========================================================

function initializeHoverEffects() {

    const cards = document.querySelectorAll(
        ".module-card"
    );

    cards.forEach(card => {

        card.addEventListener(

            "mousemove",

            event => {

                const rect =
                    card.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                card.style.background = `

                    radial-gradient(
                        circle at ${x}px ${y}px,
                        rgba(255,255,255,0.08),
                        rgba(255,255,255,0.04)
                    )
                `;
            }
        );

        card.addEventListener(

            "mouseleave",

            () => {

                card.style.background =
                    "rgba(255,255,255,0.05)";
            }
        );
    });
}

// =========================================================
// FAKE API STATUS CHECK
// =========================================================

async function checkBackendStatus() {

    try {

        const health = await getBackendHealth();

        if (health && health.success) {

            updateStatusIndicator(
                "ONLINE"
            );
        } else {

            updateStatusIndicator(
                "OFFLINE"
            );
        }

    } catch (error) {

        updateStatusIndicator(
            "OFFLINE"
        );
    }
}

// =========================================================
// STATUS UPDATE
// =========================================================

function updateStatusIndicator(status) {

    const statusItems =
        document.querySelectorAll(
            ".status-item strong"
        );

    if (statusItems.length > 0) {

        statusItems[0].innerText =
            status;
    }
}

// =========================================================
// OPTIONAL AUTO STATUS CHECK
// =========================================================

setInterval(() => {

    checkBackendStatus();

}, 8000);
