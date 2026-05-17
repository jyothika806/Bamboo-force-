// ======================================================
// API BASE URL
// ======================================================

const API_BASE =
    "http://127.0.0.1:8000/api/ride";

// ======================================================
// DEMO LOCATION DATABASE
// ======================================================


const LOCATION_COORDINATES = {

    "madhapur": [17.4483, 78.3915],

    "hitech city": [17.4435, 78.3772],

    "gachibowli": [17.4401, 78.3489],

    "kukatpally": [17.4948, 78.3996],

    "ameerpet": [17.4375, 78.4482],

    "banjara hills": [17.4126, 78.4482],

    "secunderabad": [17.4399, 78.4983]
};
// ======================================================
// CREATE RIDE
// ======================================================

async function createRide(data) {

    try {

        const response = await fetch(

            `${API_BASE}/create`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        return await response.json();

    } catch (error) {

        console.error(
            "Create Ride Error:",
            error
        );
    }
}

// ======================================================
// LOAD ACTIVE RIDES
// ======================================================

async function loadActiveRides() {

    try {

        const response = await fetch(
            `${API_BASE}/active`
        );

        const result =
            await response.json();

        if (result.success) {

            document.getElementById(
                "activeRideCount"
            ).innerText =

                Object.keys(
                    result.data
                ).length;
        }

    } catch (error) {

        console.error(error);
    }
}

// ======================================================
// LOAD GROUPS
// ======================================================

async function loadGroups() {

    try {

        const response = await fetch(
            `${API_BASE}/groups`
        );

        const result =
            await response.json();

        renderGroups(
            result.data
        );

    } catch (error) {

        console.error(error);
    }
}

// ======================================================
// LOAD RECOMMENDATIONS
// ======================================================

async function loadRecommendations() {

    try {

        const response = await fetch(
            `${API_BASE}/recommendations`
        );

        const result =
            await response.json();

        renderRecommendations(
            result.data
        );

    } catch (error) {

        console.error(error);
    }
}

// ======================================================
// FORM SUBMIT
// ======================================================

document.getElementById(
    "rideForm"
).addEventListener(

    "submit",

    async function(event) {

        event.preventDefault();
        const vehicleType =
            document.getElementById(
                "vehicle_type"
            ).value;

        let passengerCount = 1;

        if (vehicleType === "AUTO") {

            passengerCount = 3;
        }

        else if (vehicleType === "CAB") {

            passengerCount = 4;
        }

        else if (vehicleType === "VAN") {

            passengerCount = 6;
        }
        const pickupLocation =
            document.getElementById(
                "pickup_location"
            ).value.toLowerCase();

        const destinationLocation =
            document.getElementById(
                "destination_location"
            ).value.toLowerCase();

        const source =
            LOCATION_COORDINATES[
                pickupLocation.trim()
            ];

        const destination =
            LOCATION_COORDINATES[
                destinationLocation.trim()
            ];

        if (!source || !destination) {

            alert(
                "Demo location not supported"
            );

            return;
        }

        const rideData = {

            ride_id:
                document.getElementById(
                    "ride_id"
                ).value,

            source: source,

            destination: destination,

            start_time:
                Date.now(),

            share_allowed:
                document.getElementById(
                    "share_allowed"
                ).checked,

            passenger_count:
                passengerCount,
        };

        const result =
            await createRide(
                rideData
            );
        console.log(
            "CREATE RESPONSE:",
            result
        );
        alert(
            JSON.stringify(result)
        );
        console.log(result);
        if (result.success) {
            alert(
                "AI Ride Optimization Complete"
            );
            document
                .getElementById("rideForm")
                .reset();
            loadActiveRides();

            loadGroups();

            loadRecommendations();
        }
        else {

            alert(
                "Backend Error"
            );

            console.log(result);
        }

// ======================================================
// RENDER GROUPS
// ======================================================

function renderGroups(groups) {

    const container =

        document.getElementById(
            "groupsContainer"
        );

    container.innerHTML = "";

    if (

        !groups ||

        Object.keys(groups).length === 0
    ) {

        container.innerHTML = `

        <div class="dashboard-card">

            <h3>
                No Groups Yet
            </h3>

        </div>
        `;

        return;
    }

    Object.entries(groups).forEach(

        ([groupId, group]) => {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "dashboard-card";

            card.innerHTML = `

                <h3>
                    ${groupId}
                </h3>

                <p>
                    Vehicle:
                    ${group.recommended_vehicle}
                </p>

                <p>
                    Passengers:
                    ${group.passenger_count}
                </p>

                <p>
                    Efficiency:
                    ${group.cluster_efficiency}
                </p>

                <p>
                    Dynamic Chain:
                    ${group.dynamic_chain_ready}
                </p>
            `;

            container.appendChild(card);
        }
    );
}

// ======================================================
// RENDER RECOMMENDATIONS
// ======================================================

function renderRecommendations(data) {

    const container =
        document.getElementById(
            "recommendationContainer"
        );

    container.innerHTML = "";

    if (

        !data ||

        !data.passenger_recommendations
    ) {

        container.innerHTML = `

        <div class="recommendation-card">

            <h3>
                No Recommendations Yet
            </h3>

        </div>
        `;

        return;
    }

    data.passenger_recommendations.forEach(

        item => {

            container.innerHTML += `

            <div class="recommendation-card">

                <h3>

                    AI Ride Suggestion

                </h3>

                <p>

                    Recommended Vehicle:
                    <strong>
                        ${item.recommended_vehicle}
                    </strong>

                </p>

                <p>

                    Action:
                    <strong>
                        ${item.vehicle_action}
                    </strong>

                </p>

                <p>

                    Reason:
                    ${item.reason}

                </p>

                <p>

                    Traffic Reduction:
                    ${(
                        item.traffic_reduction_score
                        * 100
                    ).toFixed(0)}%

                </p>

                <p>

                    Cost Savings:
                    ₹${item.estimated_cost_savings}

                </p>

                <p>

                    Ride Chain Potential:
                    ${item.ride_chain_potential}

                </p>

            </div>
            `;
        }
    );
}

// ======================================================
// INITIAL LOAD
// ======================================================

loadActiveRides();

loadGroups();

loadRecommendations();