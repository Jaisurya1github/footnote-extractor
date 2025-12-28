const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const statusText = document.getElementById("status");

uploadBtn.onclick = async () => {
    if (!fileInput.files.length) {
        statusText.innerText = "Please select an XML file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    statusText.innerText = "Processing...";

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        statusText.innerText = "Failed to process file.";
        return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "footnotes.xml";
    document.body.appendChild(a);
    a.click();
    a.remove();

    statusText.innerText = "Download complete.";
};
