/* VAR console — no build step, no deps. Talks to the VAR REST API. */
"use strict";
const $ = (id) => document.getElementById(id);
const state = { base: "", key: "", session: null };

const fmt = {
  n: (x) => x == null ? "–" : x.toLocaleString(),
  usd: (x) => x == null ? "–" : "$" + Number(x).toFixed(4),
  ms: (x) => x == null ? "–" : x >= 1000 ? (x / 1000).toFixed(2) + " s" : x.toFixed(1) + " ms",
  when: (ts) => ts ? new Date(ts * 1000).toLocaleTimeString() : "",
};

async function api(path, opts = {}) {
  const r = await fetch(state.base + path, {
    ...opts,
    headers: { "Content-Type": "application/json",
               "Authorization": "Bearer " + state.key, ...(opts.headers || {}) },
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(body.error?.message || r.status);
  return body;
}

async function connect() {
  state.base = ($("baseUrl").value || "http://localhost:8788").replace(/\/$/, "");
  state.key = $("apiKey").value.trim();
  if (!state.key.startsWith("var_live_")) { alert("Paste a var_live_… API key"); return; }
  localStorage.setItem("var_key", state.key);
  localStorage.setItem("var_base", state.base);
  await refresh();
  $("disconnected").hidden = true; $("app").hidden = false;
}

async function refresh() {
  try {
    const [{ sessions }, perf] = await Promise.all([api("/v1/sessions"), api("/v1/perf")]);
    renderTiles(sessions);
    renderSessions(sessions);
    renderPerf(perf.tools || {});
    if (state.session) await selectSession(state.session, false);
  } catch (e) { console.error(e); alert("API error: " + e.message); }
}

function renderTiles(sessions) {
  $("tSessions").textContent = fmt.n(sessions.length);
  $("tSessionsSub").textContent = sessions.length ? "latest " + fmt.when(Math.max(...sessions.map(s => s.started_at).filter(Boolean))) : "";
  const admits = sessions.reduce((a, s) => a + s.admits, 0);
  const halts = sessions.reduce((a, s) => a + s.halts, 0);
  $("tGates").textContent = fmt.n(admits + halts);
  $("tAdmits").textContent = admits; $("tHalts").textContent = halts;
}

function renderSessions(sessions) {
  const tb = $("sessionTable").querySelector("tbody");
  tb.innerHTML = "";
  for (const s of sessions) {
    const tr = document.createElement("tr");
    tr.dataset.sid = s.session_id;
    tr.innerHTML = `<td class="mono">${s.session_id.slice(0, 14)}…</td>
      <td>${s.agent || "–"}</td><td>${s.principal || "–"}</td>
      <td>${s.steps}</td><td>${s.events}</td>
      <td><span class="chip good">✓ ${s.admits}</span> <span class="chip warn">⏸ ${s.halts}</span></td>
      <td class="chainCell">–</td>`;
    tr.onclick = () => selectSession(s.session_id);
    tb.appendChild(tr);
    // chain status per session (verify is cheap; run async)
    api(`/v1/sessions/${s.session_id}/verify`).then(v => {
      tr.querySelector(".chainCell").innerHTML =
        v.chain_valid ? '<span class="chip good">✓ intact</span>'
                      : `<span class="chip crit">⚠ ${v.error || "broken"}</span>`;
    }).catch(() => {});
  }
}

function renderPerf(tools) {
  const box = $("perfChart"); box.innerHTML = "";
  const entries = Object.entries(tools);
  if (!entries.length) { box.innerHTML = '<p class="dim">No tool calls metered yet.</p>'; $("perfLegend").innerHTML = ""; return; }
  const max = Math.max(...entries.flatMap(([, p]) => [p.p99_ms, p.p50_ms]), 1);
  for (const [tool, p] of entries) {
    const row = document.createElement("div"); row.className = "barRow";
    row.innerHTML = `<div class="tool" title="${tool}">${tool}</div>
      <div class="barTrack">
        <div class="b s1" data-tip="${tool} · p50 ${fmt.ms(p.p50_ms)} · ${p.calls} calls · fail ${(p.failure_rate * 100).toFixed(0)}%"
             style="width:${Math.max(2, p.p50_ms / max * 100)}%"></div>
        <div class="b s2" data-tip="${tool} · p99 ${fmt.ms(p.p99_ms)}"
             style="width:${Math.max(2, p.p99_ms / max * 100)}%"></div>
      </div>
      <div class="val">${fmt.ms(p.p99_ms)}</div>`;
    box.appendChild(row);
  }
  $("perfLegend").innerHTML =
    `<span><span class="sw" style="background:var(--series-1)"></span>p50</span>
     <span><span class="sw" style="background:var(--series-2)"></span>p99</span>`;
}

async function selectSession(sid, scroll = true) {
  state.session = sid;
  document.querySelectorAll("#sessionTable tbody tr").forEach(
    tr => tr.classList.toggle("selected", tr.dataset.sid === sid));
  $("detailCard").hidden = false;
  $("detailTitle").textContent = "Session " + sid;
  if (scroll) $("detailCard").scrollIntoView({ behavior: "smooth", block: "nearest" });

  const [stateJ, verify, audit, usage] = await Promise.all([
    api(`/v1/sessions/${sid}`), api(`/v1/sessions/${sid}/verify`),
    api(`/v1/sessions/${sid}/audit?type=gate_decision`), api(`/v1/sessions/${sid}/usage`),
  ]);
  $("envBox").textContent = stateJ.state.identity_envelope;

  $("verifyBox").innerHTML = verify.chain_valid
    ? `<p><span class="chip good">✓ chain intact</span></p>
       <p class="dim">${verify.length} events · head <span class="mono">${verify.head_hash?.slice(0, 24)}…</span><br>signed by ${verify.signed_by}</p>`
    : `<p><span class="chip crit">⚠ chain broken</span></p><p class="dim">${verify.error || ""}</p>`;

  const feed = $("gateFeed"); feed.innerHTML = "";
  for (const g of (audit.events || []).slice().reverse()) {
    const admit = g.decision === "ADMIT";
    const div = document.createElement("div");
    div.className = "feedItem";
    div.innerHTML = `<div><span class="chip ${admit ? "good" : "warn"}">${admit ? "✓ ADMIT" : "⏸ HALT"}</span>
      <b>${g.claim}</b> <span class="when">${fmt.when(g.decided_at)}</span></div>
      ${admit ? "" : `<div class="dim">${g.error?.error_code}: ${g.error?.message}</div>`}`;
    feed.appendChild(div);
  }
  if (!audit.events?.length) feed.innerHTML = '<p class="dim">No gate decisions yet.</p>';

  const u = usage.usage || {};
  $("budgetSession").textContent = sid.slice(0, 14) + "…";
  $("budgetBox").innerHTML = `
    <div class="gauge"><div class="${u.usd > 5 ? "critState" : usage.fraction_used >= .8 ? "warnState" : ""}"
      style="width:${Math.min(100, (usage.fraction_used || 0) * 100)}%"></div></div>
    <div class="gaugeRow"><span>${((usage.fraction_used || 0) * 100).toFixed(1)}% of budget used</span>
      <span>${fmt.usd(u.usd)}</span></div>`;
  $("usageBox").innerHTML = `
    <div class="kv"><b>${fmt.n(u.tokens)}</b><span>tokens</span></div>
    <div class="kv"><b>${fmt.usd(u.usd)}</b><span>usd</span></div>
    <div class="kv"><b>${u.wall_clock_seconds ?? "–"}s</b><span>wall clock</span></div>
    <div class="kv"><b>${stateJ.steps}</b><span>steps</span></div>`;
}

/* tooltips on bars */
document.addEventListener("mousemove", (e) => {
  const tip = $("tooltip");
  const t = e.target.closest("[data-tip]");
  if (t) { tip.hidden = false; tip.textContent = t.dataset.tip;
           tip.style.left = e.clientX + 14 + "px"; tip.style.top = e.clientY + 10 + "px"; }
  else tip.hidden = true;
});

$("loadBtn").onclick = connect;
$("apiKey").addEventListener("keydown", e => e.key === "Enter" && connect());
$("baseUrl").value = localStorage.getItem("var_base") || "http://localhost:8788";
$("apiKey").value = localStorage.getItem("var_key") || "";
