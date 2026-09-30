const API_URL = (window.VERITY_CONFIG && window.VERITY_CONFIG.apiUrl) || "";

const input = document.getElementById("file-input");
const statusBox = document.getElementById("upload-status");
const title = document.getElementById("document-title");
const statusPill = document.getElementById("document-status");
const summary = document.getElementById("document-summary");
const chunkList = document.getElementById("chunk-list");
const connectionLabel = document.getElementById("connection-label");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const searchStatus = document.getElementById("search-status");
const searchResults = document.getElementById("search-results");
const searchCount = document.getElementById("search-count");

checkBackend();

input.addEventListener("change", async () => {
  const file = input.files[0];
  if (!file) return;

  setStatus("Uploading and extracting evidence...", "success");
  const form = new FormData();
  form.append("file", file);

  try {
    const response = await fetch(API_URL + "/api/documents/ingest", { method: "POST", body: form });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Upload failed.");

    renderDocument(data);
    setStatus("Ready — " + data.chunk_count + " evidence chunk(s) created.", "success");
    statusPill.textContent = "Ready";
    searchInput.focus();
  } catch {
    setStatus("Backend unavailable. The workspace is still available, but document processing is offline.", "error");
    statusPill.textContent = "Offline";
  }
});

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = searchInput.value.trim();
  if (!query) return;

  searchStatus.textContent = "Searching extracted evidence...";
  searchResults.innerHTML = "";
  searchCount.textContent = "Searching";

  try {
    const response = await fetch(API_URL + "/api/search?q=" + encodeURIComponent(query) + "&limit=8");
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Search failed.");
    renderSearchResults(data);
  } catch {
    searchStatus.textContent = "Search is offline. Connect the Render API to retrieve evidence.";
    searchCount.textContent = "Offline";
  }
});

async function checkBackend() {
  try {
    const response = await fetch(API_URL + "/health", {
      method: "GET",
      signal: AbortSignal.timeout(4000),
    });
    if (!response.ok) throw new Error("Backend health check failed.");
    connectionLabel.textContent = "API online";
    statusPill.textContent = "API online";
  } catch {
    connectionLabel.textContent = "API offline";
    statusPill.textContent = "API offline";
    setStatus("Workspace is online. Connect the backend to enable ingestion and evidence search.", "error");
  }
}

function renderDocument(document) {
  title.textContent = document.filename;
  statusPill.textContent = document.status;
  summary.textContent = formatBytes(document.size_bytes) + " · " +
    document.character_count.toLocaleString() + " characters · " + document.chunk_count + " chunk(s)";

  chunkList.innerHTML = document.chunks.slice(0, 6).map(function (chunk) {
    return '<article class="chunk"><div class="chunk-header"><span>CHUNK ' +
      String(chunk.chunk_index + 1).padStart(2, "0") + '</span><span>' +
      escapeHtml(chunk.source) + '</span></div><p>' + escapeHtml(chunk.text) + "</p></article>";
  }).join("");
  searchStatus.textContent = "Search is ready for " + document.filename + ".";
}

function renderSearchResults(data) {
  searchCount.textContent = data.count + (data.count === 1 ? " result" : " results");
  searchStatus.textContent = data.count
    ? 'Evidence matching "' + data.query + '"'
    : "No matching evidence found. Try different words.";

  searchResults.innerHTML = data.results.map(function (result, index) {
    const percent = Math.round(result.score * 100);
    return '<article class="result-card">' +
      '<div class="result-meta"><span class="result-number">0' + (index + 1) +
      '</span><span>' + escapeHtml(result.citation) + '</span><span>' + percent + '% match</span></div>' +
      '<p>' + escapeHtml(result.text) + '</p>' +
      '<div class="result-source">Source evidence · ' + escapeHtml(result.source) + '</div>' +
      '</article>';
  }).join("");
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
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
