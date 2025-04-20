document.getElementById("chooseFolderBtn").addEventListener("click", function() {
    const folderInput = document.createElement("input");
    folderInput.type = "file";
    folderInput.webkitdirectory = true;
    folderInput.directory = true;

    folderInput.addEventListener("change", function() {
        const folderPath = folderInput.files[0]?.webkitRelativePath.split("/")[0];
        document.getElementById("folder").value = folderPath || "";
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

    const data = { platform, url, folder };

    document.getElementById("status").innerText = "Starting download...";
    document.getElementById("progressBar").value = 0;

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
        document.getElementById("progressBar").value = 100;
    })
    .catch(error => {
        document.getElementById("status").innerText = "Error: " + error.message;
    });
});

document.getElementById("clearBtn").addEventListener("click", function() {
    document.getElementById("url").value = "";
    document.getElementById("folder").value = "";
    document.getElementById("platform").value = "youtube";
    document.getElementById("status").innerText = "";
    document.getElementById("progressBar").value = 0;
});
