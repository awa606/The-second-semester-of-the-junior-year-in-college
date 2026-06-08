const appState = {
  currentTaskId: null,
  currentAudioId: null,
  currentAsrResult: null,
  currentEvaluation: null,
  currentTask: null,
  currentSteps: [],
  currentRecordFields: null,
  currentDraft: "",
  currentSafetyCheck: null,
  currentInputText: "",
  selectedEngine: "funasr",
  audioMode: "transcribe",
  uploadedFilename: "",
  taskStatus: "CREATED",
  busy: false,
  eventSource: null,
};

const FIELD_DEFS = [
  ["chief_complaint", "主诉"],
  ["present_illness", "现病史"],
  ["previous_treatment", "既往处理"],
  ["accompanying_symptoms", "伴随症状"],
  ["past_history", "既往史"],
  ["allergy_history", "过敏史"],
  ["physical_exam", "查体"],
  ["treatment_plan", "处理建议"],
];

const WORKFLOW_STEPS = [
  { key: "CREATED", label: "1.输入/上传" },
  { key: "TRANSCRIBED", label: "2.对话转写" },
  { key: "GENERATING_DRAFT", label: "3.病历草稿" },
  { key: "WAITING_DOCTOR_REVIEW", label: "4.医生审核" },
  { key: "EXPORTED", label: "5.确认导出" },
];

const STATUS_TO_STEP = {
  CREATED: "CREATED",
  TRANSCRIBED: "TRANSCRIBED",
  EXTRACTING_FIELDS: "GENERATING_DRAFT",
  GENERATING_DRAFT: "GENERATING_DRAFT",
  SAFETY_CHECKING: "GENERATING_DRAFT",
  WAITING_DOCTOR_REVIEW: "WAITING_DOCTOR_REVIEW",
  FAILED: "WAITING_DOCTOR_REVIEW",
  reviewed: "WAITING_DOCTOR_REVIEW",
  approved: "WAITING_DOCTOR_REVIEW",
  EXPORTED: "EXPORTED",
  exported: "EXPORTED",
};

const STATUS_LABELS = {
  CREATED: "任务已创建",
  TRANSCRIBED: "转写完成",
  EXTRACTING_FIELDS: "字段抽取中",
  GENERATING_DRAFT: "草稿生成中",
  SAFETY_CHECKING: "安全校验中",
  WAITING_DOCTOR_REVIEW: "等待医生审核",
  FAILED: "任务失败",
  reviewed: "草稿已保存",
  approved: "字段已确认",
  EXPORTED: "已导出",
  exported: "已导出",
};

const ENGINE_LABELS = {
  funasr: "FunASR",
  mock: "Mock ASR",
  qwen3: "Qwen3-ASR 0.6B",
  online: "Online ASR",
  "funasr-local": "FunASR",
  "mock-asr-v0.2": "Mock ASR",
  "qwen3-asr-0.6b": "Qwen3-ASR 0.6B",
};

const $ = (id) => document.getElementById(id);

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    if (typeof detail === "string") throw new Error(detail);
    if (detail?.errors) throw new Error(detail.errors.join(" "));
    throw new Error(JSON.stringify(detail || data));
  }
  return data;
}

function renderJson(element, value) {
  if (!element) return;
  element.textContent = value ? JSON.stringify(value, null, 2) : "-";
}

function setBusy(nextBusy, message = "") {
  appState.busy = nextBusy;
  document.querySelectorAll("button").forEach((button) => {
    if (button.id !== "closeDrawerButton") button.disabled = nextBusy;
  });
  if (message) {
    $("currentTaskHint").textContent = message;
  }
}

function showToast(text) {
  const toast = $("toast");
  toast.textContent = text;
  toast.classList.add("active");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.remove("active"), 2200);
}

function openDrawer(panelId, title) {
  $("drawerTitle").textContent = title;
  $("drawerBackdrop").classList.add("active");
  $("drawer").classList.add("active");
  $("drawer").setAttribute("aria-hidden", "false");
  document.querySelectorAll(".drawer-panel").forEach((panel) => panel.classList.remove("active"));
  $(panelId).classList.add("active");
}

function closeDrawer() {
  $("drawerBackdrop").classList.remove("active");
  $("drawer").classList.remove("active");
  $("drawer").setAttribute("aria-hidden", "true");
}

function renderPatientBar() {
  $("patientName").textContent = "模拟患者";
  $("patientProfile").textContent = "女 / 32岁";
  $("sessionId").textContent = appState.currentTaskId
    ? `T-${appState.currentTaskId}`
    : appState.currentAudioId
      ? `A-${appState.currentAudioId}`
      : "未创建";
  $("recordingStatus").textContent = appState.uploadedFilename || "未上传";
  $("asrEngine").textContent = ENGINE_LABELS[appState.selectedEngine] || appState.selectedEngine;
  $("reviewStatus").textContent = STATUS_LABELS[appState.taskStatus] || appState.taskStatus || "等待输入";
}

function renderWorkflow() {
  const activeKey = STATUS_TO_STEP[appState.taskStatus] || "CREATED";
  const activeIndex = WORKFLOW_STEPS.findIndex((step) => step.key === activeKey);
  $("workflowSteps").innerHTML = WORKFLOW_STEPS.map((step, index) => {
    const state = index < activeIndex ? "done" : index === activeIndex ? "active" : "";
    return `<li class="workflow-step ${state}">${escapeHtml(step.label)}</li>`;
  }).join("");
}

function fieldStatus(field, key) {
  if (key === "treatment_plan") {
    return appState.currentDraft
      ? { key: "candidate", label: "候选待确认" }
      : { key: "missing", label: "待补充" };
  }
  if (!field || field.missing || (!field.value && field.hint)) return { key: "missing", label: "待补充" };
  if (field.confirmed_by_doctor) return { key: "confirmed", label: "已确认" };
  if (typeof field.confidence === "number" && field.confidence < 0.7) return { key: "low", label: "低置信度" };
  return { key: "confirmed", label: "已确认" };
}

function fieldValue(fields, key) {
  if (key === "treatment_plan") {
    return appState.currentDraft ? "处理建议已生成在右栏病历草稿中，需医生确认后写入。" : "待医生补充处理建议";
  }
  const field = fields?.[key];
  return field?.value || field?.hint || "暂无内容";
}

function fieldEvidence(field, key) {
  if (key === "treatment_plan") return "处理建议来自 AI 病历草稿，需医生结合诊疗规范确认。";
  const spans = field?.source_spans || [];
  return spans.length ? spans.map((span) => span.text).filter(Boolean).join("\n") : "暂无证据片段，需结合原始转写复核。";
}

function renderFields() {
  const fields = appState.currentRecordFields;
  if (!fields) {
    $("fieldCountBadge").textContent = "待生成";
    $("fieldCountBadge").className = "status-badge neutral";
    $("recordFields").innerHTML = `<div class="empty-state">暂无病历字段。请点击“文本导入”或“上传生成病历”。</div>`;
    return;
  }

  let missingCount = 0;
  const cards = FIELD_DEFS.map(([key, title]) => {
    const field = fields[key] || null;
    const status = fieldStatus(field, key);
    if (status.key === "missing") missingCount += 1;
    const confidence = key === "treatment_plan" ? null : field?.confidence;
    return `
      <article class="field-card ${status.key}" data-field="${key}">
        <div class="field-head">
          <span class="field-title">${escapeHtml(title)}</span>
          <span class="status-badge ${status.key}">${escapeHtml(status.label)}</span>
        </div>
        <div class="field-value">${escapeHtml(fieldValue(fields, key))}</div>
        <div class="field-meta">
          <span class="confidence">${confidence == null ? "需医生复核" : `置信度 ${Math.round(confidence * 100)}%`}</span>
          <button type="button" data-evidence-toggle>证据</button>
        </div>
        <div class="field-evidence">${escapeHtml(fieldEvidence(field, key))}</div>
      </article>
    `;
  }).join("");

  const diagnoses = (fields.candidate_diagnoses || []).map((diagnosis, index) => `
    <article class="field-card candidate" data-field="diagnosis-${index}">
      <div class="field-head">
        <span class="field-title">候选诊断</span>
        <span class="status-badge candidate">${diagnosis.confirmed_by_doctor ? "已确认" : "候选待确认"}</span>
      </div>
      <div class="field-value">${escapeHtml(diagnosis.name || "未命名诊断")}</div>
      <div class="field-meta">
        <span class="confidence">${escapeHtml(diagnosis.status || "候选/待医生确认")}</span>
        <button type="button" data-evidence-toggle>证据</button>
      </div>
      <div class="field-evidence">${escapeHtml((diagnosis.evidence || []).map((item) => item.text).join("\n") || "暂无候选诊断证据。")}</div>
    </article>
  `).join("");

  $("fieldCountBadge").textContent = missingCount ? `${missingCount}项待补充` : "待医生确认";
  $("fieldCountBadge").className = `status-badge ${missingCount ? "missing" : "confirmed"}`;
  $("recordFields").innerHTML = cards + diagnoses;
}

function classifySpeaker(line, segment = {}) {
  const raw = `${segment.role || ""} ${segment.speaker || ""} ${line}`.toLowerCase();
  if (raw.includes("医生") || raw.includes("doctor")) return "doctor";
  if (raw.includes("患者") || raw.includes("patient")) return "patient";
  return "patient";
}

function transcriptRowsFromText(text) {
  const normalized = String(text || "")
    .replace(/\s*(\[(?:医生|患者|doctor|patient|待校正)\])/gi, "\n$1")
    .trim();
  return normalized
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => ({
      time: `00:${String(index * 8).padStart(2, "0")}`,
      speaker: classifySpeaker(line),
      label: classifySpeaker(line) === "doctor" ? "医生" : "患者",
      text: line.replace(/^\[(医生|患者|doctor|patient|待校正)\]\s*/i, ""),
    }));
}

function transcriptRows() {
  const asr = appState.currentAsrResult;
  if (asr?.segments?.length > 1) {
    return asr.segments.map((segment, index) => {
      const speaker = classifySpeaker(segment.text || "", segment);
      return {
        time: segment.start_time != null ? `${Number(segment.start_time).toFixed(1)}s` : `00:${String(index * 8).padStart(2, "0")}`,
        speaker,
        label: speaker === "doctor" ? "医生" : "患者",
        text: segment.text || "",
      };
    });
  }
  if (asr) return transcriptRowsFromText(asr.conversation_text || asr.text || "");
  return transcriptRowsFromText(appState.currentInputText);
}

function renderTranscript() {
  const asr = appState.currentAsrResult;
  const rows = transcriptRows();
  const warningBlocks = [];
  if (asr?.role_strategy === "single_segment_needs_review") {
    warningBlocks.push("当前 ASR 返回单段长文本，医生/患者角色需人工校正。");
  }
  (asr?.warnings || []).forEach((warning) => warningBlocks.push(warning));

  if (!rows.length && !asr) {
    $("transcriptBadge").textContent = "待转写";
    $("transcriptList").innerHTML = `<div class="empty-state">暂无对话转写。可导入文本或上传音频。</div>`;
    return;
  }

  $("transcriptBadge").textContent = asr
    ? `${asr.engine || appState.selectedEngine} · ${asr.segments?.length || 0}段`
    : `${rows.length}条`;

  const asrTextBlock = asr?.text
    ? `<div class="safety-strip"><strong>ASRResult.text</strong><br>${escapeHtml(asr.text)}</div>`
    : "";
  const conversationBlock = asr?.conversation_text
    ? `<div class="safety-strip"><strong>conversation_text</strong><br>${escapeHtml(asr.conversation_text)}</div>`
    : "";

  $("transcriptList").innerHTML = `
    ${warningBlocks.map((item) => `<div class="conversation-warning">${escapeHtml(item)}</div>`).join("")}
    ${asrTextBlock}
    ${conversationBlock}
    ${rows.map((item, index) => `
      <div class="chat-row">
        <div class="chat-time">${escapeHtml(item.time)}</div>
        <div class="chat-card ${index === 1 ? "highlight" : ""}">
          <span class="speaker-tag ${item.speaker}">${escapeHtml(item.label)}</span>
          ${escapeHtml(item.text)}
        </div>
      </div>
    `).join("")}
  `;
}

function missingItems() {
  const fields = appState.currentRecordFields;
  if (!fields) return [];
  return FIELD_DEFS.filter(([key]) => fieldStatus(fields[key], key).key === "missing").map(([, label]) => label);
}

function allEvidence() {
  const fields = appState.currentRecordFields;
  if (!fields) return [];
  const evidence = [];
  FIELD_DEFS.forEach(([key, label]) => {
    if (key === "treatment_plan") return;
    (fields[key]?.source_spans || []).forEach((span) => {
      if (span.text) evidence.push(`${label}：${span.text}`);
    });
  });
  (fields.candidate_diagnoses || []).forEach((diagnosis) => {
    (diagnosis.evidence || []).forEach((span) => {
      if (span.text) evidence.push(`候选诊断 ${diagnosis.name}：${span.text}`);
    });
  });
  return evidence.slice(0, 8);
}

function renderEvaluationBlock() {
  const evaluation = appState.currentEvaluation;
  if (!evaluation) {
    return `<div class="empty-state">暂无 ASR 评测结果。完成音频转写后点击“ASR评测”。</div>`;
  }
  const keywords = evaluation.medical_keywords || {};
  return `
    <div class="metric-grid">
      <div class="metric-card"><span>CER</span><strong>${Number(evaluation.cer ?? 0).toFixed(4)}</strong></div>
      <div class="metric-card"><span>keyword_recall</span><strong>${Number(evaluation.keyword_recall ?? 0).toFixed(2)}</strong></div>
    </div>
    <div class="safety-strip success"><strong>recognized</strong><br>${escapeHtml((keywords.recognized || []).join("、") || "无")}</div>
    <div class="safety-strip ${keywords.missing?.length ? "warning" : "success"}"><strong>missing</strong><br>${escapeHtml((keywords.missing || []).join("、") || "无")}</div>
  `;
}

function renderAssist() {
  const fields = appState.currentRecordFields;
  const safety = appState.currentSafetyCheck;
  const missing = missingItems();
  const diagnoses = fields?.candidate_diagnoses || [];
  const evidence = allEvidence();
  const warnings = [...(appState.currentAsrResult?.warnings || []), ...(safety?.warnings || [])];
  if (appState.currentAsrResult?.role_strategy === "single_segment_needs_review") {
    warnings.unshift("医生/患者角色需人工校正");
  }
  const errors = safety?.errors || [];

  $("assistPanels").innerHTML = `
    <section class="assist-block">
      <div class="assist-title">
        <h3>缺失项提醒</h3>
        <span class="status-badge ${missing.length ? "missing" : "confirmed"}">${missing.length ? `${missing.length}项` : "无"}</span>
      </div>
      <div class="assist-body">
        ${missing.length ? `<div class="safety-strip danger">${escapeHtml(missing.join("、"))}</div>` : `<div class="safety-strip success">暂无结构化字段缺失。</div>`}
      </div>
    </section>

    <section class="assist-block">
      <div class="assist-title">
        <h3>候选诊断</h3>
        <span class="status-badge candidate">${diagnoses.length ? "待确认" : "暂无"}</span>
      </div>
      <div class="assist-body">
        ${diagnoses.length ? diagnoses.map((diagnosis) => `
          <div class="diagnosis-card">
            <strong>${escapeHtml(diagnosis.name || "未命名诊断")}</strong>
            ${escapeHtml(diagnosis.status || "候选/待医生确认")}
          </div>
        `).join("") : `<div class="empty-state">暂无候选诊断。</div>`}
      </div>
    </section>

    <section class="assist-block">
      <div class="assist-title">
        <h3>病历草稿</h3>
        <span class="status-badge ${appState.currentDraft ? "info" : "neutral"}">${appState.currentDraft ? "已生成" : "待生成"}</span>
      </div>
      <div class="assist-body">
        <div class="draft-block">${escapeHtml(appState.currentDraft || "暂无病历草稿。")}</div>
      </div>
    </section>

    <section class="assist-block">
      <div class="assist-title">
        <h3>字段证据</h3>
        <span class="status-badge info">${evidence.length ? "可追溯" : "暂无"}</span>
      </div>
      <div class="assist-body">
        ${evidence.length ? evidence.map((item) => `<button type="button" class="evidence-chip">${escapeHtml(item)}</button>`).join("") : `<div class="empty-state">暂无字段证据。</div>`}
      </div>
    </section>

    <section class="assist-block">
      <div class="assist-title">
        <h3>ASR评测摘要</h3>
        <span class="status-badge info">CER / Recall</span>
      </div>
      <div class="assist-body">
        ${renderEvaluationBlock()}
      </div>
    </section>

    <section class="assist-block">
      <div class="assist-title">
        <h3>安全校验结果</h3>
        <span class="status-badge ${safety?.passed && !safety?.blocked ? "confirmed" : "missing"}">${safety ? (safety.passed && !safety.blocked ? "通过" : "需处理") : "待校验"}</span>
      </div>
      <div class="assist-body">
        ${warnings.map((item) => `<div class="safety-strip warning">${escapeHtml(item)}</div>`).join("")}
        ${errors.map((item) => `<div class="safety-strip danger">${escapeHtml(item)}</div>`).join("")}
        ${safety ? `<div class="safety-strip ${safety.passed && !safety.blocked ? "success" : "danger"}">安全校验：${safety.passed ? "通过" : "未通过"}${safety.blocked ? " / 阻止导出" : ""}</div>` : `<div class="empty-state">暂无AI校验结果。</div>`}
      </div>
    </section>
  `;
}

function renderDebug() {
  renderJson($("debugAsrJson"), appState.currentAsrResult);
  renderJson($("debugTaskJson"), appState.currentTask);
  renderJson($("debugStepsJson"), appState.currentSteps);
  renderJson($("debugSafetyJson"), appState.currentSafetyCheck);
}

function renderFooter() {
  $("currentTaskLabel").textContent = `当前任务：${STATUS_LABELS[appState.taskStatus] || appState.taskStatus || "等待输入"}`;
  $("currentTaskHint").textContent = appState.currentTaskId
    ? `任务 ${appState.currentTaskId} · ${appState.currentAudioId ? `音频 ${appState.currentAudioId}` : "文本导入"}`
    : "可通过文本导入或上传音频生成病历。";
}

function renderAll() {
  renderPatientBar();
  renderWorkflow();
  renderFields();
  renderTranscript();
  renderAssist();
  renderDebug();
  renderFooter();
}

function resetTaskState({ keepAsr = false } = {}) {
  appState.currentEvaluation = null;
  appState.currentTask = null;
  appState.currentSteps = [];
  appState.currentRecordFields = null;
  appState.currentDraft = "";
  appState.currentSafetyCheck = null;
  appState.currentInputText = "";
  if (!keepAsr) {
    appState.currentAsrResult = null;
    appState.currentAudioId = null;
    appState.uploadedFilename = "";
  }
}

async function refreshTask(taskId, taskFromEvent = null) {
  const task = taskFromEvent || await api(`/api/tasks/${taskId}`);
  const steps = await api(`/api/tasks/${taskId}/steps`);
  appState.currentTask = task;
  appState.currentSteps = steps;
  appState.currentTaskId = task.id || task.task_id || taskId;
  appState.taskStatus = task.status || task.current_stage || appState.taskStatus;
  const result = task.result_json || {};
  appState.currentRecordFields = result.fields || appState.currentRecordFields;
  appState.currentDraft = result.draft || appState.currentDraft;
  appState.currentSafetyCheck = result.safety_check || appState.currentSafetyCheck;
  renderAll();
}

function listenForEvents(taskId, eventsUrl) {
  if (appState.eventSource) appState.eventSource.close();
  const source = new EventSource(eventsUrl);
  appState.eventSource = source;
  let terminalReceived = false;

  ["CREATED", "EXTRACTING_FIELDS", "GENERATING_DRAFT", "SAFETY_CHECKING", "DEGRADED"].forEach((status) => {
    source.addEventListener(status, (event) => {
      const data = JSON.parse(event.data);
      appState.currentTaskId = data.task_id;
      appState.taskStatus = data.status;
      appState.currentTask = { ...(appState.currentTask || {}), id: data.task_id, status: data.status, current_stage: data.current_stage };
      renderAll();
    });
  });

  source.addEventListener("WAITING_DOCTOR_REVIEW", async (event) => {
    const data = JSON.parse(event.data);
    terminalReceived = true;
    appState.taskStatus = "WAITING_DOCTOR_REVIEW";
    await refreshTask(data.task_id, data.task);
    source.close();
    appState.eventSource = null;
    setBusy(false);
    showToast("病历已生成，等待医生审核");
  });

  source.addEventListener("FAILED", async (event) => {
    const data = JSON.parse(event.data);
    terminalReceived = true;
    appState.taskStatus = "FAILED";
    await refreshTask(data.task_id, data.task);
    source.close();
    appState.eventSource = null;
    setBusy(false);
    showToast("任务失败");
  });

  source.onerror = () => {
    if (!terminalReceived) {
      appState.taskStatus = "FAILED";
      showToast("SSE 连接异常，请到调试页查看任务日志");
    }
    source.close();
    appState.eventSource = null;
    setBusy(false);
    renderAll();
  };
}

async function createRecordTask(conversationText) {
  resetTaskState();
  appState.currentInputText = conversationText;
  appState.currentAsrResult = {
    audio_id: "text-import",
    engine: "text-import",
    text: conversationText,
    conversation_text: conversationText,
    segments: [],
    duration: null,
    medical_keywords: {},
    warnings: [],
  };
  appState.taskStatus = "CREATED";
  renderAll();
  setBusy(true, "正在创建病历生成任务...");
  const created = await api("/api/records/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conversation_text: conversationText }),
  });
  appState.currentTaskId = created.task_id;
  appState.taskStatus = created.status;
  appState.currentTask = { id: created.task_id, status: created.status };
  renderAll();
  listenForEvents(created.task_id, created.events_url);
}

async function uploadAndTranscribe(file, engine) {
  if (!file) throw new Error("请选择音频文件");
  appState.selectedEngine = engine;
  appState.uploadedFilename = "上传中";
  appState.taskStatus = "CREATED";
  renderAll();

  const form = new FormData();
  form.append("file", file);
  setBusy(true, "正在上传音频...");
  const uploaded = await api("/api/audio/upload", { method: "POST", body: form });
  appState.currentAudioId = uploaded.audio_id;
  appState.uploadedFilename = uploaded.filename || uploaded.audio_id;
  renderAll();

  setBusy(true, `正在使用 ${ENGINE_LABELS[engine] || engine} 转写...`);
  const transcribed = await api(`/api/audio/${uploaded.audio_id}/transcribe?engine=${engine}`, { method: "POST" });
  appState.currentAsrResult = transcribed.asr_result;
  appState.currentAudioId = transcribed.audio_id;
  appState.taskStatus = "TRANSCRIBED";
  appState.currentEvaluation = null;
  renderAll();
  showToast("音频转写完成");
  return transcribed;
}

async function submitTextImport() {
  try {
    const text = $("conversationInput").value.trim();
    if (!text) throw new Error("请输入问诊文本");
    closeDrawer();
    await createRecordTask(text);
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

async function submitAudio() {
  try {
    closeDrawer();
    resetTaskState();
    const file = $("audioFileInput").files[0];
    const engine = $("audioEngineSelect").value;
    appState.selectedEngine = engine;
    const transcribed = await uploadAndTranscribe(file, engine);
    if (appState.audioMode === "generate") {
      setBusy(true, "正在从转写文本生成病历...");
      const created = await api(`/api/audio/${transcribed.audio_id}/generate-record`, { method: "POST" });
      appState.currentTaskId = created.task_id;
      appState.taskStatus = created.status;
      appState.currentTask = { id: created.task_id, status: created.status };
      renderAll();
      listenForEvents(created.task_id, created.events_url);
    } else {
      setBusy(false);
      renderAll();
    }
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

async function runEvaluation() {
  try {
    if (!appState.currentAudioId) throw new Error("暂无可评测的音频转写");
    const expectedKeywords = $("keywordsInput").value
      .split(/[\n,，]+/)
      .map((item) => item.trim())
      .filter(Boolean);
    appState.currentEvaluation = await api(`/api/audio/${appState.currentAudioId}/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ground_truth_text: $("groundTruthInput").value || " ",
        expected_keywords: expectedKeywords,
      }),
    });
    $("evaluationDrawerResult").innerHTML = renderEvaluationBlock();
    renderAll();
    showToast("ASR 评测完成");
  } catch (error) {
    $("evaluationDrawerResult").innerHTML = `<div class="safety-strip danger">${escapeHtml(error.message)}</div>`;
    showToast(error.message);
  }
}

async function regenerateRecord() {
  try {
    const text = appState.currentAsrResult?.conversation_text || appState.currentInputText || $("conversationInput").value.trim();
    if (!text) throw new Error("暂无可重新生成的对话文本");
    await createRecordTask(text);
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

async function saveDraftReview() {
  try {
    if (!appState.currentTaskId || !appState.currentRecordFields) throw new Error("暂无可保存的病历字段");
    setBusy(true, "正在保存草稿...");
    appState.currentTask = await api(`/api/tasks/${appState.currentTaskId}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fields: appState.currentRecordFields }),
    });
    await refreshTask(appState.currentTaskId, appState.currentTask);
    setBusy(false);
    showToast("草稿已保存");
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

async function confirmFields() {
  try {
    if (!appState.currentTaskId) throw new Error("暂无可确认的任务");
    setBusy(true, "正在确认字段...");
    appState.currentTask = await api(`/api/tasks/${appState.currentTaskId}/approve`, { method: "POST" });
    appState.taskStatus = "approved";
    await refreshTask(appState.currentTaskId, appState.currentTask);
    setBusy(false);
    showToast("字段已确认");
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

async function exportRecord() {
  try {
    if (!appState.currentTaskId) throw new Error("暂无可导出的任务");
    setBusy(true, "正在导出...");
    const result = await api(`/api/tasks/${appState.currentTaskId}/export`, { method: "POST" });
    appState.taskStatus = "EXPORTED";
    renderAll();
    setBusy(false);
    showToast(`导出完成：${Object.values(result.exports || {}).join(" / ")}`);
  } catch (error) {
    setBusy(false);
    showToast(error.message);
  }
}

function openTextImport() {
  openDrawer("textImportPanel", "文本导入生成病历");
}

function openAudioTranscribe() {
  appState.audioMode = "transcribe";
  $("audioPanelHint").textContent = "上传预录音频，仅测试 ASR 转写。医生端默认使用 FunASR。";
  $("submitAudioButton").textContent = "上传并转写";
  openDrawer("audioPanel", "上传音频测试转写");
}

function openAudioGenerate() {
  appState.audioMode = "generate";
  $("audioPanelHint").textContent = "上传预录音频，先由 FunASR 转写，再生成病历。";
  $("submitAudioButton").textContent = "上传并生成病历";
  openDrawer("audioPanel", "上传音频生成病历");
}

function openEvaluation() {
  const expected = appState.currentAsrResult?.medical_keywords?.expected || [];
  if (expected.length && !$("keywordsInput").value.trim()) {
    $("keywordsInput").value = expected.join("\n");
  }
  $("evaluationDrawerResult").innerHTML = renderEvaluationBlock();
  openDrawer("evaluationPanel", "ASR 评测");
}

function openDebug() {
  renderDebug();
  openDrawer("debugPanel", "医生端调试详情");
}

function bindEvents() {
  $("openTextImportButton").addEventListener("click", openTextImport);
  $("openAudioTranscribeButton").addEventListener("click", openAudioTranscribe);
  $("openAudioGenerateButton").addEventListener("click", openAudioGenerate);
  $("openEvaluationButton").addEventListener("click", openEvaluation);
  $("openDebugButton").addEventListener("click", openDebug);
  $("closeDrawerButton").addEventListener("click", closeDrawer);
  $("drawerBackdrop").addEventListener("click", closeDrawer);
  $("submitTextButton").addEventListener("click", submitTextImport);
  $("submitAudioButton").addEventListener("click", submitAudio);
  $("submitEvaluationButton").addEventListener("click", runEvaluation);
  $("audioEngineSelect").addEventListener("change", () => {
    appState.selectedEngine = $("audioEngineSelect").value;
    renderPatientBar();
  });
  $("recordFields").addEventListener("click", (event) => {
    if (event.target.matches("[data-evidence-toggle]")) {
      event.target.closest(".field-card").classList.toggle("open");
    }
  });
  $("regenerateButton").addEventListener("click", regenerateRecord);
  $("saveDraftButton").addEventListener("click", saveDraftReview);
  $("confirmFieldsButton").addEventListener("click", confirmFields);
  $("exportButton").addEventListener("click", exportRecord);
}

function init() {
  bindEvents();
  renderAll();
}

init();
