const API_URL = "http://localhost:8000";
const input = document.getElementById("file-input");
const statusBox = document.getElementById("upload-status");
const title = document.getElementById("document-title");
const statusPill = document.getElementById("document-status");
const summary = document.getElementById("document-summary");
const chunkList = document.getElementById("chunk-list");

input.addEventListener("change", async () => {
  const file = input.files[0];
  if (!file) return;

  setStatus("Uploading and extracting evidence...", "success");

  const form = new FormData();
  form.append("file", file);

  try {
    const response = await fetch(API_URL + "/api/documents/ingest", {
      method: "POST",
      body: form,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Upload failed.");
    }

    renderDocument(data);
    setStatus("Ready — " + data.chunk_count + " evidence chunk(s) created.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
});

function renderDocument(document) {
  title.textContent = document.filename;
  statusPill.textContent = document.status;
  summary.textContent =
    formatBytes(document.size_bytes) +
    " · " +
    document.character_count.toLocaleString() +
    " characters · " +
    document.chunk_count +
    " chunk(s)";

  chunkList.innerHTML = document.chunks
    .slice(0, 6)
    .map(function (chunk) {
      return (
        '<article class="chunk">' +
        '<div class="chunk-header">' +
        "<span>CHUNK " +
        String(chunk.chunk_index + 1).padStart(2, "0") +
        "</span>" +
        "<span>" +
        escapeHtml(chunk.source) +
        "</span>" +
        "</div>" +
        "<p>" +
        escapeHtml(chunk.text) +
        "</p>" +
        "</article>"
      );
    })
    .join("");
}

function setStatus(message, type) {
  statusBox.textContent = message;
  statusBox.className = "status " + type;
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
