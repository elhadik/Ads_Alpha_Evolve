/**
 * Circana Liquid Data × AlphaEvolve — Frontend Visual Controller
 */
(() => {
  // Configuration Form Inputs
  const aeConfigForm = document.getElementById("aeConfigForm");
  const cfgConcurrency = document.getElementById("cfgConcurrency");
  const cfgMaxPrograms = document.getElementById("cfgMaxPrograms");
  const cfgMaxIterations = document.getElementById("cfgMaxIterations");
  const cfgTimeout = document.getElementById("cfgTimeout");
  const cfgBackend = document.getElementById("cfgBackend");
  const cfgResetInterval = document.getElementById("cfgResetInterval");
  const cfgModelPreset = document.getElementById("cfgModelPreset");
  const cfgPrimaryModel = document.getElementById("cfgPrimaryModel");
  const cfgPrimaryWeight = document.getElementById("cfgPrimaryWeight");
  const cfgSecondaryModel = document.getElementById("cfgSecondaryModel");
  const cfgSecondaryWeight = document.getElementById("cfgSecondaryWeight");
  const cfgBudget = document.getElementById("cfgBudget");
  const cfgMinFlight = document.getElementById("cfgMinFlight");
  const cfgCooldown = document.getElementById("cfgCooldown");
  const cfgProject = document.getElementById("cfgProject");
  const cfgEngine = document.getElementById("cfgEngine");

  // Top & Scrubber Controls
  const aeCliStatusText = document.getElementById("aeCliStatusText");
  const playEvolutionBtn = document.getElementById("playEvolutionBtn");
  const resetEvolutionBtn = document.getElementById("resetEvolutionBtn");
  const stageSlider = document.getElementById("stageSlider");
  const stageCounterBadge = document.getElementById("stageCounterBadge");
  const activeNicknameBadge = document.getElementById("activeNicknameBadge");
  const activeSummaryTitle = document.getElementById("activeSummaryTitle");
  const activeWhatChanged = document.getElementById("activeWhatChanged");
  const milestoneList = document.getElementById("milestoneList");
  const improvementBadge = document.getElementById("improvementBadge");

  // KPI Elements
  const kpiGenerated = document.getElementById("kpiGenerated");
  const kpiEvaluated = document.getElementById("kpiEvaluated");
  const kpiConcurrency = document.getElementById("kpiConcurrency");
  const kpiModelUsed = document.getElementById("kpiModelUsed");
  const kpiLift = document.getElementById("kpiLift");
  const kpiRoas = document.getElementById("kpiRoas");
  const kpiWaste = document.getElementById("kpiWaste");
  const kpiLossBreakdown = document.getElementById("kpiLossBreakdown");
  const kpiScore = document.getElementById("kpiScore");
  const chart1CapBadge = document.getElementById("chart1CapBadge");
  const chart4LiftDelta = document.getElementById("chart4LiftDelta");

  // Canvases
  const evoChartCanvas = document.getElementById("evoChartCanvas");
  const scurveChartCanvas = document.getElementById("scurveChartCanvas");
  const heatmapChartCanvas = document.getElementById("heatmapChartCanvas");
  const weeklyLiftChartCanvas = document.getElementById("weeklyLiftChartCanvas");

  // Code Inspector & Tabs
  const codeEditorTextarea = document.getElementById("codeEditorTextarea");
  const diffViewerPre = document.getElementById("diffViewerPre");
  const cliCommandsPre = document.getElementById("cliCommandsPre");
  const evaluatorInsightsPre = document.getElementById("evaluatorInsightsPre");
  const evalCustomCodeBtn = document.getElementById("evalCustomCodeBtn");

  let evolutionData = null;
  let currentStageIdx = 0;
  let playTimer = null;

  function readConfigFromForm() {
    return {
      concurrency: parseInt(cfgConcurrency.value || "10", 10),
      max_programs: parseInt(cfgMaxPrograms.value || "100", 10),
      max_iterations: parseInt(cfgMaxIterations.value || "100", 10),
      timeout_seconds: parseInt(cfgTimeout.value || "60", 10),
      backend: cfgBackend.value,
      reset_interval: parseInt(cfgResetInterval.value || "25", 10),
      model_preset: cfgModelPreset.value,
      primary_model: cfgPrimaryModel.value.trim(),
      primary_weight: parseFloat(cfgPrimaryWeight.value || "0.9"),
      secondary_model: cfgSecondaryModel.value.trim(),
      secondary_weight: parseFloat(cfgSecondaryWeight.value || "0.1"),
      gcp_project: cfgProject.value.trim(),
      gcp_engine: cfgEngine.value.trim(),
      gcp_location: "global",
      experiment_title: "Circana Omni-Channel Retail Media Flighting & iROAS Optimizer",
      total_budget_musd: parseFloat(cfgBudget.value || "2.50"),
      min_flight_musd: parseFloat(cfgMinFlight.value || "0.025"),
      pantry_cooldown_weeks: parseInt(cfgCooldown.value || "3", 10),
    };
  }

  function populateFormFromConfig(cfg) {
    if (!cfg) return;
    cfgConcurrency.value = cfg.concurrency;
    cfgMaxPrograms.value = cfg.max_programs;
    cfgMaxIterations.value = cfg.max_iterations;
    cfgTimeout.value = cfg.timeout_seconds;
    cfgBackend.value = cfg.backend;
    cfgResetInterval.value = cfg.reset_interval;
    cfgModelPreset.value = cfg.model_preset;
    cfgPrimaryModel.value = cfg.primary_model;
    cfgPrimaryWeight.value = cfg.primary_weight;
    cfgSecondaryModel.value = cfg.secondary_model;
    cfgSecondaryWeight.value = cfg.secondary_weight;
    cfgProject.value = cfg.gcp_project;
    cfgEngine.value = cfg.gcp_engine;
    cfgBudget.value = cfg.total_budget_musd;
    cfgMinFlight.value = cfg.min_flight_musd;
    cfgCooldown.value = cfg.pantry_cooldown_weeks;
  }

  async function checkAeCliStatus() {
    try {
      const res = await fetch("/api/ae_status");
      const data = await res.json();
      aeCliStatusText.textContent = `${data.ae_version || "ae ready"} • Local Evaluator Ready`;
    } catch (_) {
      aeCliStatusText.textContent = "Local Evaluator Active";
    }
  }

  async function runEvolutionSimulation(keepStageIdx = false) {
    const cfg = readConfigFromForm();
    const res = await fetch("/api/simulate_evolution", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cfg),
    });
    evolutionData = await res.json();
    stageSlider.max = String(evolutionData.milestones.length - 1);
    if (!keepStageIdx) {
      currentStageIdx = 0;
      stageSlider.value = "0";
    }
    improvementBadge.textContent = `+${evolutionData.improvement_pct}% Score`;
    cliCommandsPre.textContent = evolutionData.cli_commands.combined;
    renderMilestoneSidebar();
    renderStage(currentStageIdx);
  }

  function renderMilestoneSidebar() {
    if (!evolutionData) return;
    milestoneList.innerHTML = evolutionData.milestones
      .map(
        (m, idx) => `
        <div class="milestone-item ${idx === currentStageIdx ? "active" : ""}" data-idx="${idx}">
          <div class="milestone-top">
            <span>#${m.evaluated_count} • ${m.nickname}</span>
            <span class="text-emerald">${m.score.toFixed(1)}</span>
          </div>
          <div class="milestone-desc">${m.summary}</div>
        </div>
      `
      )
      .join("");

    milestoneList.querySelectorAll(".milestone-item").forEach((el) => {
      el.addEventListener("click", () => {
        const idx = parseInt(el.getAttribute("data-idx"), 10);
        currentStageIdx = idx;
        stageSlider.value = String(idx);
        renderStage(idx);
      });
    });
  }

  function renderStage(idx) {
    if (!evolutionData || !evolutionData.milestones[idx]) return;
    currentStageIdx = idx;
    const m = evolutionData.milestones[idx];
    const seed = evolutionData.milestones[0];
    const t = m.telemetry || {};

    milestoneList.querySelectorAll(".milestone-item").forEach((el, i) => {
      el.classList.toggle("active", i === idx);
    });

    activeNicknameBadge.textContent = m.nickname;
    activeSummaryTitle.textContent = m.summary;
    activeWhatChanged.textContent = m.what_changed;
    stageCounterBadge.textContent = `Eval ${m.evaluated_count} / ${m.max_evaluated_cap}`;

    kpiGenerated.textContent = `${m.generated_count} / ${m.max_generated_cap}`;
    kpiEvaluated.textContent = `${m.evaluated_count} / ${m.max_evaluated_cap}`;
    kpiConcurrency.textContent = `${m.active_workers} / ${m.concurrency} parallel`;
    kpiModelUsed.textContent = `Generator: ${m.model_used}`;

    const liftMusd = t.incremental_lift_musd ?? 0;
    const iroas = t.iroas ?? 0;
    const spend = t.total_spend_musd ?? 2.5;
    const waste = t.waste_pct ?? 0;

    kpiLift.textContent = `+$${liftMusd.toFixed(2)}M`;
    kpiRoas.textContent = `iROAS: ${iroas.toFixed(2)}x ($${spend.toFixed(2)}M spend)`;
    kpiWaste.textContent = `${waste.toFixed(1)}%`;
    kpiLossBreakdown.textContent = `Pantry: $${(t.pantry_loss_musd || 0).toFixed(2)}M | Overlap: $${(t.overlap_loss_musd || 0).toFixed(2)}M`;
    kpiScore.textContent = m.score.toFixed(2);
    chart1CapBadge.textContent = `Cap: ${m.max_evaluated_cap} evals (Concurrency ${m.concurrency})`;

    const seedLift = (seed.telemetry && seed.telemetry.incremental_lift_musd) || liftMusd;
    const deltaLift = liftMusd - seedLift;
    chart4LiftDelta.textContent = `${deltaLift >= 0 ? "+" : ""}$${deltaLift.toFixed(2)}M vs. Seed`;

    codeEditorTextarea.value = m.evolve_block_code;
    diffViewerPre.textContent = m.unified_diff;
    evaluatorInsightsPre.textContent = JSON.stringify(
      { score: m.score, insights: m.insights },
      null,
      2
    );

    drawEvoChart(idx);
    drawSCurveChart(m);
    drawHeatmapChart(m);
    drawWeeklyLiftChart(m, seed);
  }

  // Chart 1: Evolutionary Fitness Progression
  function drawEvoChart(activeIdx) {
    const ctx = evoChartCanvas.getContext("2d");
    const w = evoChartCanvas.width;
    const h = evoChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 44, padR = 18, padT = 18, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const milestones = evolutionData.milestones;
    const maxEvalCap = milestones[activeIdx].max_evaluated_cap;
    const currentEval = milestones[activeIdx].evaluated_count;

    const minS = Math.floor(milestones[0].score * 0.72);
    const maxS = Math.ceil(milestones[milestones.length - 1].score * 1.06);
    const spanS = Math.max(20, maxS - minS);

    const toX = (evalNum) => padL + ((evalNum - 1) / Math.max(1, maxEvalCap - 1)) * pw;
    const toY = (score) => padT + ph - ((score - minS) / spanS) * ph;

    // Gridlines
    ctx.strokeStyle = "rgba(148, 163, 184, 0.15)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padT + (ph * i) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      const labelVal = Math.round(maxS - (spanS * i) / 4);
      ctx.fillStyle = "#94a3b8";
      ctx.font = "11px monospace";
      ctx.fillText(String(labelVal), 6, y + 4);
    }

    // Scatter points up to currentEval
    (evolutionData.scatter_points || []).forEach((pt) => {
      if (pt.eval_num > currentEval) return;
      const x = toX(pt.eval_num);
      if (pt.status === "FAILED" || pt.score === null) {
        const y = padT + ph - 8;
        ctx.strokeStyle = "rgba(239, 68, 68, 0.75)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x - 3, y - 3);
        ctx.lineTo(x + 3, y + 3);
        ctx.moveTo(x + 3, y - 3);
        ctx.lineTo(x - 3, y + 3);
        ctx.stroke();
      } else {
        const y = toY(pt.score);
        ctx.fillStyle = "rgba(56, 189, 248, 0.42)";
        ctx.beginPath();
        ctx.arc(x, y, 2.8, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Elite Frontier Step Curve
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2.6;
    ctx.beginPath();
    for (let i = 0; i <= activeIdx; i++) {
      const m = milestones[i];
      const x = toX(m.evaluated_count);
      const y = toY(m.score);
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        const prevY = toY(milestones[i - 1].score);
        ctx.lineTo(x, prevY);
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();

    // Milestone nodes
    for (let i = 0; i <= activeIdx; i++) {
      const m = milestones[i];
      const x = toX(m.evaluated_count);
      const y = toY(m.score);
      ctx.fillStyle = i === activeIdx ? "#f59e0b" : "#10b981";
      ctx.beginPath();
      ctx.arc(x, y, i === activeIdx ? 5.5 : 4, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px sans-serif";
    ctx.fillText("Eval #1", padL, h - 6);
    ctx.fillText(`Eval #${maxEvalCap}`, padL + pw - 58, h - 6);
  }

  // Chart 2: Hill S-Curve Operating Points
  function drawSCurveChart(milestone) {
    const ctx = scurveChartCanvas.getContext("2d");
    const w = scurveChartCanvas.width;
    const h = scurveChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 40, padR = 18, padT = 18, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const hill = (x) => Math.pow(x, 3.15) / (Math.pow(0.45, 3.15) + Math.pow(x, 3.15));

    // Dead-zone band
    ctx.fillStyle = "rgba(239, 68, 68, 0.08)";
    ctx.fillRect(padL, padT, pw * 0.34, ph);

    // Optimal knee band (0.48 - 0.65)
    const kx1 = padL + 0.48 * pw;
    const kx2 = padL + 0.65 * pw;
    ctx.fillStyle = "rgba(16, 185, 129, 0.15)";
    ctx.fillRect(kx1, padT, kx2 - kx1, ph);

    // S-curve line
    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    for (let i = 0; i <= 80; i++) {
      const xv = i / 80;
      const yv = hill(xv);
      const x = padL + xv * pw;
      const y = padT + ph - yv * ph;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Operating points from telemetry (dispersed slightly along curve so all points are visible)
    const pts = (milestone.telemetry && milestone.telemetry.scurve_operating_points) || [0.25];
    const rmnLabels = ["WMT", "TGT", "KRG", "INST", "AMZ"];
    pts.forEach((rawXv, i) => {
      const jitterX = (i - (pts.length - 1) / 2) * 0.014;
      const xv = Math.max(0.06, Math.min(0.94, rawXv + jitterX));
      const yv = hill(xv);
      const x = padL + xv * pw;
      const y = padT + ph - yv * ph;
      const inKnee = rawXv >= 0.42 && rawXv <= 0.68;
      ctx.fillStyle = inKnee ? "#10b981" : "#f59e0b";
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#0b1120";
      ctx.lineWidth = 1.5;
      ctx.stroke();

      if (i < rmnLabels.length) {
        ctx.fillStyle = "#e2e8f0";
        ctx.font = "bold 9px monospace";
        ctx.fillText(rmnLabels[i], x - 10, y - 9 - (i % 2) * 8);
      }
    });

    ctx.fillStyle = "#f87171";
    ctx.font = "11px sans-serif";
    ctx.fillText("Dead Zone (<0.75κ)", padL + 8, padT + ph - 10);
    ctx.fillStyle = "#34d399";
    ctx.fillText("Optimal Marginal Knee (1.15–1.45κ)", kx1 - 18, padT + 14);
    ctx.fillStyle = "#94a3b8";
    ctx.fillText("Spend / Max Tier →", padL + pw - 105, h - 6);
  }

  // Chart 3: 5 RMNs x 8 Weeks Flighting Matrix Heatmap
  function drawHeatmapChart(milestone) {
    const ctx = heatmapChartCanvas.getContext("2d");
    const w = heatmapChartCanvas.width;
    const h = heatmapChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const rmns = ["WMT Connect", "TGT Roundel", "Kroger PM", "Instacart", "Amazon Fresh"];
    const hillK = [0.095, 0.088, 0.082, 0.076, 0.072];
    const invCaps = [
      [0.24, 0.09, 0.22, 0.24, 0.08, 0.22, 0.24, 0.18],
      [0.18, 0.23, 0.08, 0.21, 0.23, 0.09, 0.20, 0.23],
      [0.20, 0.18, 0.22, 0.08, 0.20, 0.22, 0.08, 0.20],
      [0.19, 0.20, 0.20, 0.19, 0.20, 0.08, 0.19, 0.20],
      [0.20, 0.08, 0.20, 0.20, 0.08, 0.20, 0.19, 0.20],
    ];

    const alloc = (milestone.telemetry && milestone.telemetry.allocation_matrix_musd) || [];
    const padL = 90, padR = 12, padT = 10, padB = 26;
    const rows = 5, cols = 8;
    const cellW = (w - padL - padR) / cols;
    const cellH = (h - padT - padB) / rows;

    for (let r = 0; r < rows; r++) {
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "11px monospace";
      ctx.fillText(rmns[r], 6, padT + r * cellH + cellH * 0.65);

      for (let c = 0; c < cols; c++) {
        const valMusd = (alloc[r] && alloc[r][c]) || 0;
        const valK = Math.round(valMusd * 1000);
        let bg = "rgba(30, 41, 59, 0.65)";
        if (valMusd > invCaps[r][c] + 0.002) {
          bg = "rgba(239, 68, 68, 0.85)";
        } else if (valMusd >= 1.02 * hillK[r] && valMusd <= 1.85 * hillK[r]) {
          bg = "rgba(16, 185, 129, 0.84)";
        } else if (valMusd > 0.01) {
          bg = "rgba(245, 158, 11, 0.75)";
        }

        const x = padL + c * cellW;
        const y = padT + r * cellH;
        ctx.fillStyle = bg;
        ctx.fillRect(x + 2, y + 2, cellW - 4, cellH - 4);

        ctx.fillStyle = valK > 0 ? "#0f172a" : "#64748b";
        ctx.font = "bold 10px monospace";
        const label = valK > 0 ? `$${valK}k` : "—";
        ctx.fillText(label, x + 8, y + cellH * 0.64);
      }
    }

    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px sans-serif";
    for (let c = 0; c < cols; c++) {
      ctx.fillText(`Wk ${c + 1}`, padL + c * cellW + 12, h - 7);
    }
  }

  // Chart 4: Cumulative Weekly Incremental Sales Lift ($M)
  function drawWeeklyLiftChart(milestone, seedMilestone) {
    const ctx = weeklyLiftChartCanvas.getContext("2d");
    const w = weeklyLiftChartCanvas.width;
    const h = weeklyLiftChartCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const padL = 44, padR = 18, padT = 18, padB = 28;
    const pw = w - padL - padR;
    const ph = h - padT - padB;

    const curWeekly = (milestone.telemetry && milestone.telemetry.weekly_lift_musd) || [0, 0, 0, 0, 0, 0, 0, 0];
    const seedWeekly = (seedMilestone.telemetry && seedMilestone.telemetry.weekly_lift_musd) || [0, 0, 0, 0, 0, 0, 0, 0];

    const cumCur = [];
    const cumSeed = [];
    let s1 = 0, s2 = 0;
    for (let i = 0; i < 8; i++) {
      s1 += curWeekly[i] || 0;
      s2 += seedWeekly[i] || 0;
      cumCur.push(s1);
      cumSeed.push(s2);
    }

    const maxY = Math.max(12.0, s1 * 1.1, s2 * 1.1);
    const toX = (wkIdx) => padL + (wkIdx / 7) * pw;
    const toY = (val) => padT + ph - (val / maxY) * ph;

    // Grid
    ctx.strokeStyle = "rgba(148, 163, 184, 0.15)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padT + (ph * i) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + pw, y);
      ctx.stroke();

      const v = (maxY * (4 - i)) / 4;
      ctx.fillStyle = "#94a3b8";
      ctx.font = "11px monospace";
      ctx.fillText(`$${v.toFixed(1)}M`, 4, y + 4);
    }

    // Seed dashed curve
    ctx.strokeStyle = "rgba(148, 163, 184, 0.65)";
    ctx.setLineDash([5, 4]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    cumSeed.forEach((v, i) => {
      const x = toX(i);
      const y = toY(v);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.setLineDash([]);

    // Active evolved cumulative curve
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    cumCur.forEach((v, i) => {
      const x = toX(i);
      const y = toY(v);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    cumCur.forEach((v, i) => {
      const x = toX(i);
      const y = toY(v);
      ctx.fillStyle = "#10b981";
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px sans-serif";
    for (let i = 0; i < 8; i++) {
      ctx.fillText(`W${i + 1}`, toX(i) - 8, h - 6);
    }
  }

  // Event Listeners
  stageSlider.addEventListener("input", () => {
    renderStage(parseInt(stageSlider.value, 10));
  });

  aeConfigForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    await runEvolutionSimulation(true);
  });

  playEvolutionBtn.addEventListener("click", () => {
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
      playEvolutionBtn.textContent = "▶ Play Evolution";
      return;
    }
    playEvolutionBtn.textContent = "⏸ Pause Evolution";
    if (!evolutionData) return;
    if (currentStageIdx >= evolutionData.milestones.length - 1) {
      currentStageIdx = -1;
    }
    playTimer = setInterval(() => {
      currentStageIdx++;
      if (currentStageIdx >= evolutionData.milestones.length) {
        clearInterval(playTimer);
        playTimer = null;
        playEvolutionBtn.textContent = "▶ Play Evolution";
        return;
      }
      stageSlider.value = String(currentStageIdx);
      renderStage(currentStageIdx);
    }, 1250);
  });

  resetEvolutionBtn.addEventListener("click", () => {
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
      playEvolutionBtn.textContent = "▶ Play Evolution";
    }
    stageSlider.value = "0";
    renderStage(0);
  });

  // Tab switching
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.add("hidden"));
      btn.classList.add("active");
      const target = document.getElementById(btn.getAttribute("data-tab"));
      if (target) target.classList.remove("hidden");
    });
  });

  // Evaluate Custom Edited Code Live via evaluator.py
  evalCustomCodeBtn.addEventListener("click", async () => {
    const origLabel = evalCustomCodeBtn.textContent;
    evalCustomCodeBtn.textContent = "⏳ Evaluating...";
    try {
      const cfg = readConfigFromForm();
      const res = await fetch("/api/evaluate_custom", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          evolve_block_code: codeEditorTextarea.value,
          total_budget_musd: cfg.total_budget_musd,
          min_flight_musd: cfg.min_flight_musd,
          pantry_cooldown_weeks: cfg.pantry_cooldown_weeks,
          timeout_seconds: cfg.timeout_seconds,
        }),
      });
      const data = await res.json();
      if (data.score === null || data.score === undefined) {
        alert("Evaluation failed! Check the 'Generated ae CLI Commands & Insights' tab for traceback details.");
        evaluatorInsightsPre.textContent = JSON.stringify(data, null, 2);
        return;
      }
      // Update current stage view with the custom evaluated candidate
      const customMilestone = {
        ...evolutionData.milestones[currentStageIdx],
        nickname: "custom-edited-candidate",
        summary: "Custom Edited Python Candidate (Evaluated Live by evaluator.py)",
        score: data.score,
        insights: data.insights,
        telemetry: data.telemetry,
        evolve_block_code: codeEditorTextarea.value,
        unified_diff: data.unified_diff,
      };
      evolutionData.milestones[currentStageIdx] = customMilestone;
      renderMilestoneSidebar();
      renderStage(currentStageIdx);
      evalCustomCodeBtn.textContent = `✅ Score: ${data.score.toFixed(2)}`;
      setTimeout(() => {
        evalCustomCodeBtn.textContent = origLabel;
      }, 1800);
    } catch (err) {
      console.error("Custom evaluation failed:", err);
      evalCustomCodeBtn.textContent = origLabel;
    }
  });

  // Initialize
  (async () => {
    await checkAeCliStatus();
    const cfgRes = await fetch("/api/config");
    const cfgData = await cfgRes.json();
    populateFormFromConfig(cfgData.config);
    await runEvolutionSimulation(false);
  })();
})();

