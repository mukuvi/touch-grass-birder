const RECORD_MS = 6000;

const els = {
  recordBtn: document.getElementById("recordBtn"),
  recordLabel: document.getElementById("recordLabel"),
  status: document.getElementById("status"),
  results: document.getElementById("results"),
  detections: document.getElementById("detections"),
  fileInput: document.getElementById("fileInput"),
  fileBtn: document.getElementById("fileBtn"),
  photoInput: document.getElementById("photoInput"),
  photoBtn: document.getElementById("photoBtn"),
  netBadge: document.getElementById("netBadge"),
  modelTag: document.getElementById("modelTag"),
  sightingList: document.getElementById("sightingList"),
  sightingCount: document.getElementById("sightingCount"),
};

let recording = false;
let mediaRecorder = null;
let chunks = [];
let timer = null;
let visionBusy = false;

function setStatus(text) {
  els.status.textContent = text;
}

function setRecordingUI(on) {
  els.recordBtn.classList.toggle("active", on);
  els.recordLabel.textContent = on ? "Listening" : "Listen";
}

function audioBufferToWav(buffer) {
  const numCh = 1;
  const sampleRate = buffer.sampleRate;
  const channel = buffer.getChannelData(0);
  const len = channel.length;
  const bytesPerSample = 2;
  const blockAlign = numCh * bytesPerSample;
  const dataSize = len * blockAlign;
  const out = new ArrayBuffer(44 + dataSize);
  const view = new DataView(out);

  const writeStr = (offset, str) => {
    for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
  };

  writeStr(0, "RIFF");
  view.setUint32(4, 36 + dataSize, true);
  writeStr(8, "WAVE");
  writeStr(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numCh, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * blockAlign, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, 16, true);
  writeStr(36, "data");
  view.setUint32(40, dataSize, true);

  let offset = 44;
  for (let i = 0; i < len; i++) {
    const s = Math.max(-1, Math.min(1, channel[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    offset += 2;
  }
  return new Blob([view], { type: "audio/wav" });
}

async function toWavBlob(blob) {
  const arrayBuffer = await blob.arrayBuffer();
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  try {
    const audioBuffer = await ctx.decodeAudioData(arrayBuffer);
    return audioBufferToWav(audioBuffer);
  } finally {
    ctx.close();
  }
}

async function sendForId(blob) {
  setStatus("Identifying locally");
  els.results.hidden = true;
  const form = new FormData();
  form.append("audio", blob, "clip.wav");
  try {
    const res = await fetch("/api/identify", { method: "POST", body: form });
    if (!res.ok) throw new Error(await res.text());
    render(await res.json());
  } catch (err) {
    setStatus("Could not identify that clip. Try a clearer recording.");
    console.error(err);
  }
}

async function record() {
  if (!navigator.mediaDevices?.getUserMedia) {
    setStatus("Recording needs https or localhost.");
    return;
  }
  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch {
    setStatus("Microphone permission denied.");
    return;
  }
  chunks = [];
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = (e) => e.data.size && chunks.push(e.data);
  mediaRecorder.onstop = async () => {
    stream.getTracks().forEach((t) => t.stop());
    clearTimeout(timer);
    setRecordingUI(false);
    const raw = new Blob(chunks, { type: mediaRecorder.mimeType });
    const wav = await toWavBlob(raw);
    sendForId(wav);
  };
  mediaRecorder.start();
  setRecordingUI(true);
  setStatus(`Recording ${RECORD_MS / 1000}s. Stay quiet.`);
  timer = setTimeout(() => mediaRecorder.stop(), RECORD_MS);
}

function confidenceBar(value) {
  const pct = Math.round(value * 100);
  return `<div class="bar"><span style="width:${pct}%"></span></div><span class="pct">${pct}%</span>`;
}

function render(data) {
  setStatus(`${data.count} detection(s) via ${data.model}`);
  if (!data.detections.length) {
    els.detections.innerHTML = `<p class="empty">Nothing confident enough. Get closer and try again.</p>`;
    els.results.hidden = false;
    return;
  }
  els.detections.innerHTML = data.detections
    .map((d) => {
      const note = d.field_note ? `<p class="note">${escapeHtml(d.field_note)}</p>` : "";
      return `<article class="det">
        <div class="det-head">
          <strong>${escapeHtml(d.common_name)}</strong>
          <em>${escapeHtml(d.scientific_name)}</em>
        </div>
        ${confidenceBar(d.confidence)}
        ${note}
        <button class="save" data-name="${escapeAttr(d.common_name)}" data-sci="${escapeAttr(d.scientific_name)}" data-conf="${d.confidence}">Log sighting</button>
      </article>`;
    })
    .join("");
  els.results.hidden = false;
  els.detections.querySelectorAll(".save").forEach((btn) => {
    btn.addEventListener("click", () => saveSighting(btn));
  });
}

async function saveSighting(btn) {
  const form = new FormData();
  form.append("common_name", btn.dataset.name);
  form.append("scientific_name", btn.dataset.sci);
  form.append("confidence", btn.dataset.conf);
  const note = btn.closest(".det").querySelector(".note");
  form.append("note", note ? note.textContent : "");
  await fetch("/api/sightings", { method: "POST", body: form });
  btn.textContent = "Logged";
  btn.disabled = true;
  loadSightings();
}

async function loadSightings() {
  try {
    const res = await fetch("/api/sightings");
    const { sightings } = await res.json();
    els.sightingCount.textContent = sightings.length;
    els.sightingList.innerHTML = sightings
      .map(
        (s) =>
          `<li><span>${escapeHtml(s.common_name)}</span><time>${new Date(s.created_at).toLocaleString()}</time></li>`
      )
      .join("");
  } catch {
    return;
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
const escapeAttr = escapeHtml;

els.recordBtn.addEventListener("click", () => {
  if (recording) return;
  recording = true;
  record().finally(() => (recording = false));
});

els.fileBtn.addEventListener("click", () => els.fileInput.click());
els.fileInput.addEventListener("change", async () => {
  const file = els.fileInput.files[0];
  if (!file) return;
  const wav = file.type === "audio/wav" ? file : await toWavBlob(file);
  sendForId(wav);
});

async function sendForVision(file) {
  if (visionBusy) return;
  visionBusy = true;
  els.photoBtn.disabled = true;
  const preview = URL.createObjectURL(file);
  setStatus("Identifying by photo");
  els.results.hidden = true;
  const form = new FormData();
  form.append("image", file);
  try {
    const res = await fetch("/api/vision", { method: "POST", body: form });
    if (!res.ok) throw new Error(await res.text());
    renderVision(await res.json(), preview);
  } catch (err) {
    setStatus("Could not identify that photo.");
    console.error(err);
  } finally {
    visionBusy = false;
    els.photoBtn.disabled = false;
  }
}

function renderVision(data, previewUrl) {
  if (!data.configured) {
    setStatus("Photo ID is not configured on this instance.");
    return;
  }
  setStatus(`Photo ID via ${data.model}`);
  const species = data.species ? escapeHtml(data.species) : "Unsure";
  const img = previewUrl ? `<img class="photo-preview" src="${previewUrl}" alt="your photo" />` : "";
  els.detections.innerHTML = `<article class="det">
    ${img}
    <div class="det-head">
      <strong>${species}</strong>
    </div>
    ${data.note ? `<p class="note">${escapeHtml(data.note)}</p>` : ""}
    <button class="save" data-name="${escapeAttr(data.species || "Unknown bird")}" data-sci="" data-conf="0">Log sighting</button>
  </article>`;
  els.results.hidden = false;
  els.detections.querySelector(".save").addEventListener("click", (btn) => saveSighting(btn.currentTarget));
}

els.photoBtn.addEventListener("click", () => els.photoInput.click());
els.photoInput.addEventListener("change", async () => {
  const file = els.photoInput.files[0];
  if (!file) return;
  sendForVision(file);
});

function updateNet() {
  els.netBadge.textContent = navigator.onLine ? "online" : "offline, still works";
  els.netBadge.classList.toggle("off", !navigator.onLine);
}
window.addEventListener("online", updateNet);
window.addEventListener("offline", updateNet);

async function boot() {
  updateNet();
  loadSightings();
  try {
    const res = await fetch("/api/health");
    const h = await res.json();
    let tag = `BirdNET ready, Gemma ${h.gemma_available ? "ready" : "off"}`;
    if (h.gemma4_available) tag += `, Gemma 4 ready`;
    els.modelTag.textContent = tag;
  } catch {
    els.modelTag.textContent = "server not reachable";
  }
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  }
}

boot();
