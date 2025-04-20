// Make sure DOM is fully loaded before adding event listeners
document.addEventListener("DOMContentLoaded", function() {
    // Choose Folder Button
    document.getElementById("chooseFolderBtn").addEventListener("click", function() {
        const folderInput = document.createElement("input");
        folderInput.type = "file";
        folderInput.webkitdirectory = true;
        folderInput.directory = true;

        folderInput.addEventListener("change", function() {
            const firstFile = folderInput.files[0];
            if (firstFile) {
                const folderPath = firstFile.webkitRelativePath.split("/")[0];
                document.getElementById("folder").value = folderPath || "";
            } else {
                document.getElementById("folder").value = "";
            }
        });

        folderInput.click();
    });

    // Download Button
    document.getElementById("downloadBtn").addEventListener("click", function() {
        const platform = document.getElementById("platform").value;
        const url = document.getElementById("url").value;
        const folder = document.getElementById("folder").value;

        if (!url || !folder) {
            alert("Please provide both a video URL and folder name.");
            return;
        }

        const data = { platform, url, folder };

        document.getElementById("status").innerText = "Starting download...";
        const progressBar = document.getElementById("progressBar");
        if (progressBar) progressBar.value = 0;

        fetch("http://127.0.0.1:5000/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                throw new Error(result.error);
            }
            document.getElementById("status").innerText = "Download Completed!";
            if (progressBar) progressBar.value = 100;
        })
        .catch(error => {
            document.getElementById("status").innerText = "Error: " + error.message;
        });
    });

    // Clear Button
    document.getElementById("clearBtn").addEventListener("click", function() {
        document.getElementById("url").value = "";
        document.getElementById("folder").value = "";
        document.getElementById("platform").value = "youtube";
        document.getElementById("status").innerText = "";
        const progressBar = document.getElementById("progressBar");
        if (progressBar) progressBar.value = 0;
    });
});
