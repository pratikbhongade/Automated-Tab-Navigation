document.addEventListener("DOMContentLoaded", function () {
    const validationForm = document.getElementById("validationForm");
    const statusText = document.getElementById("statusText");
    const statusList = document.getElementById("statusList");

    validationForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const environment = document.getElementById("environment").value;
        statusText.className = "badge badge-warning";
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
                statusText.className = data.status === "Completed" ? "badge badge-success" : "badge badge-danger";
                statusList.innerHTML = "";
                data.results.forEach(result => {
                    const li = document.createElement("li");
                    li.className = "list-group-item";
                    li.textContent = result[0];
                    const statusIcon = document.createElement("i");
                    statusIcon.className = result[1] === "Success" ? "fas fa-check-circle text-success" : "fas fa-times-circle text-danger";
                    li.appendChild(statusIcon);
                    statusList.appendChild(li);
                });
            });
    }, 2000);
});
