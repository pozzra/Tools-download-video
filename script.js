document.getElementById("downloadBtn").addEventListener("click", async () => {
  const platform = document.getElementById("platform").value;
  const url = document.getElementById("url").value;
  const progressBar = document.getElementById("progressBar");
  const statusDiv = document.getElementById("status");
  const downloadResultDiv = document.getElementById("downloadResult");
  const downloadTitle = document.getElementById("downloadTitle");
  const downloadLink = document.getElementById("downloadLink");

  // Validate URL and platform
  if (!url) {
    statusDiv.textContent = "Please enter a video URL.";
    return;
  }

  // Show progress bar
  progressBar.value = 0;
  statusDiv.textContent = "Downloading...";

  try {
    const response = await fetch("http://127.0.0.1:5000/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        platform: platform,
        url: url,
      }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }

    const result = await response.json();
    
    if (result.status === "success") {
      downloadTitle.textContent = `Download Complete: ${result.title}`;
      downloadLink.href = `http://127.0.0.1:5000/downloads/${result.title}`;
      downloadResultDiv.classList.remove("hidden");
      statusDiv.textContent = "Download successful!";
    } else {
      statusDiv.textContent = result.error || "An unknown error occurred.";
    }
  } catch (error) {
    statusDiv.textContent = `Error: ${error.message}`;
  } finally {
    progressBar.value = 100;
  }
});

document.getElementById("clearBtn").addEventListener("click", () => {
  document.getElementById("url").value = "";
  document.getElementById("status").textContent = "";
  document.getElementById("downloadResult").classList.add("hidden");
});

document.getElementById("chooseFolderBtn").addEventListener("click", () => {
  // Implement the folder selection feature here
  alert("Folder selection is not implemented yet.");
});
