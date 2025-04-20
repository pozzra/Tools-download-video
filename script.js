   document.getElementById("downloadBtn").addEventListener("click", function () {
            const platform = document.getElementById("platform").value;
            const url = document.getElementById("url").value;
            const progressBar = document.getElementById("progressBar");
            const statusDiv = document.getElementById("status");

            if (!url) {
                alert("Please provide a video URL.");
                return;
            }

            const data = { platform, url };

            statusDiv.innerText = "Starting download...";
            progressBar.value = 0; // Reset progress bar

            fetch("https://web-production-4bbff.up.railway.app/download", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok.");
                }
                return response.json();
            })
            .then((result) => {
                if (result.status === "success") {
                    statusDiv.innerText = `Download Completed: ${result.title}`;
                } else {
                    statusDiv.innerText = `Error: ${result.error}`;
                }
            })
            .catch((error) => {
                statusDiv.innerText = "Error: " + error.message;
                console.error("Error during fetch:", error);
            });

            // Simulate download progress (this would depend on your backend sending real-time progress)
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 100) {
                    progress += 5;
                    progressBar.value = progress;
                } else {
                    clearInterval(progressInterval);
                }
            }, 500); // Update every 500ms
        });

        document.getElementById("clearBtn").addEventListener("click", function () {
            document.getElementById("url").value = "";
            document.getElementById("platform").value = "youtube";
            document.getElementById("status").innerText = "";
            document.getElementById("progressBar").value = 0;
        });
