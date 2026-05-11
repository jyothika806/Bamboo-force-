async function handleVerify() {

    const fileInput =

        document.getElementById(
            "imageInput"
        );

    const file =
        fileInput.files[0];

    if (!file) {

        alert(
            "Please select image"
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(

        "file",

        file
    );

    const result =
        await verifyFace(
            formData
        );

    console.log(result);

    const resultBox =

        document.getElementById(
            "result"
        );

    if (result.success) {

        resultBox.innerHTML = `

            <h2>Verification Success</h2>

            <pre>

${JSON.stringify(result, null, 2)}

            </pre>
        `;

    } else {

        resultBox.innerHTML = `

            <h2>Verification Failed</h2>

            <pre>

${JSON.stringify(result, null, 2)}

            </pre>
        `;
    }
}