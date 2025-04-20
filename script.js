document.getElementById("chooseFolderBtn").addEventListener("click", function() {
    const folderInput = document.createElement("input");
    folderInput.type = "file";
    folderInput.webkitdirectory = true;
    folderInput.directory = true;

    folderInput.addEventListener("change", function() {
        const folderPath = folderInput.files[0].webkitRelativePath.split("/")[0];
        document.getElementById("folder").value = folderPath;
    });

    folderInput.click();
});

document.getElementById("downloadBtn").addEventListener("click", function() {
    const platform = document.getElementById("platform").value;
    const url = document.getElementById("url").value;
    const folder = document.getElementById("folder").value;

    if (!url || !folder) {
        alert("Please provide both a video URL and folder name.");
        return;
    }

    const data = {
        platform: platform,
        url: url,
        folder: folder
    };

    document.getElementById("status").innerText = "Downloading...";
    document.getElementById("progressBar").value = 0;

    fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Download failed");
        }

        // Create a new EventSource to listen for the progress updates
        const eventSource = new EventSource("http://127.0.0.1:5000/download");
        
        eventSource.onmessage = function(event) {
            const progress = parseInt(event.data, 10);
            document.getElementById("progressBar").value = progress;
            document.getElementById("status").innerText = `Downloading... ${progress}%`;

            if (progress === 100) {
                eventSource.close();
                document.getElementById("status").innerText = "Download Completed!";
            }
        };

        eventSource.onerror = function() {
            document.getElementById("status").innerText = "Error during download.";
        };
    })
    .catch(error => {
        document.getElementById("status").innerText = "Error: " + error;
    });
});

document.getElementById("clearBtn").addEventListener("click", function() {
    document.getElementById("url").value = "";
    document.getElementById("folder").value = "";
    document.getElementById("platform").value = "youtube";
    document.getElementById("status").innerText = "";
    document.getElementById("progressBar").value = 0;
}
);
document.getElementById("folderName").value = selectedFolder;
