document.addEventListener("DOMContentLoaded", function () {
    const validationForm = document.getElementById("validationForm");
    const statusText = document.getElementById("statusText");
    const statusList = document.getElementById("statusList");

    validationForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const environment = document.getElementById("environment").value;
        statusText.textContent = "Running...";
        statusList.innerHTML = "";

        fetch("/start_validation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ environment })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => console.error("Error starting validation:", error));
    });

    setInterval(function () {
        fetch("/status")
            .then(response => response.json())
            .then(data => {
                statusText.textContent = data.status;
                statusList.innerHTML = "";
                data.results.forEach(result => {
                    const li = document.createElement("li");
                    li.textContent = result[0];
                    statusList.appendChild(li);
                });
            });
    }, 2000);
});
