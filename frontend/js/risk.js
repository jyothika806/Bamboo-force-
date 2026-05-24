// =====================================================
// RISK PREDICTION
// =====================================================

async function runRiskPrediction() {

    const passengerCount = parseInt(

        document.getElementById(
            "risk_passenger_count"
        ).value
    );

    const result =
        await predictRideRisk({

            passenger_count:
                passengerCount
        });

    console.log(
        "RISK RESULT:",
        result
    );

    const riskBox =
        document.getElementById(
            "riskResult"
        );

    if (result.success) {

        riskBox.innerHTML = `

            <h3>
                Risk Level:
                ${result.risk_level}
            </h3>

        `;

    } else {

        riskBox.innerHTML = `

            <h3>
                Prediction Failed
            </h3>

        `;
    }
}