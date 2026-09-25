// var-client.js — VAR hosted API client for the browser and Node 18+.
// No dependencies: plain fetch.
//
//   import { VarClient } from "./var-client.js";
//   const var = new VarClient("http://localhost:8788", "var_live_…");
//   const s = await var.createSession({ permissions: ["run:tests"], maxUsd: 2 });
//   const d = await var.gateClaim(s.session_id, "tests_passed", { commit_sha });
//   if (!d.admitted) console.log(d.error.recovery);

export class VarApiError extends Error {
  constructor(status, body) { super(`${status}: ${body?.error?.message ?? JSON.stringify(body)}`); this.status = status; this.body = body; }
}

export class VarClient {
  constructor(baseUrl = "http://localhost:8788", apiKey = "", timeoutMs = 30000) {
    this.base = baseUrl.replace(/\/$/, "");
    this.key = apiKey;
    this.timeoutMs = timeoutMs;
  }

  async #req(method, path, body) {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), this.timeoutMs);
    try {
      const r = await fetch(this.base + path, {
        method, signal: ctrl.signal,
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.key}` },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      const json = await r.json().catch(() => ({}));
      if (!r.ok) throw new VarApiError(r.status, json);
      return json;
    } finally { clearTimeout(t); }
  }

  // sessions
  async createSession({ agentId = "agent", permissions = [], maxUsd, maxTokens, maxWallClockSeconds } = {}) {
    const budget = { max_usd: maxUsd, max_tokens: maxTokens, max_wall_clock_seconds: maxWallClockSeconds };
    for (const k of Object.keys(budget)) if (budget[k] === undefined) delete budget[k];
    return this.#req("POST", "/v1/sessions", { agent_id: agentId, permissions, ...(Object.keys(budget).length ? { budget } : {}) });
  }
  async sessions() { return (await this.#req("GET", "/v1/sessions")).sessions; }
  async sessionState(id) { return this.#req("GET", `/v1/sessions/${id}`); }
  async resume(id) { return this.#req("POST", `/v1/sessions/${id}/resume`); }
  async checkpoint(id, { memory = {}, messages = [] } = {}) { return this.#req("POST", `/v1/sessions/${id}/checkpoint`, { memory, messages }); }

  // Proof-or-Stop
  async gateClaim(sessionId, claim, target, confidence = 1.0) {
    const d = await this.#req("POST", `/v1/sessions/${sessionId}/gate`, { claim, target, confidence });
    return { ...d, admitted: d.decision === "ADMIT" };
  }
  async recordApproval(sessionId, approver, role, claim, target = {}) {
    return this.#req("POST", `/v1/sessions/${sessionId}/approvals`, { approver, role, claim, target });
  }

  // metering / attestation
  async meterLlm(sessionId, stakes, inputTokens, outputTokens) {
    return this.#req("POST", `/v1/sessions/${sessionId}/meter`, { kind: "llm", stakes, input_tokens: inputTokens, output_tokens: outputTokens });
  }
  async usage(sessionId) { return this.#req("GET", `/v1/sessions/${sessionId}/usage`); }
  async verify(sessionId) { return this.#req("GET", `/v1/sessions/${sessionId}/verify`); }
  async audit(sessionId, { principal, type } = {}) {
    const q = new URLSearchParams(Object.entries({ principal, type }).filter(([, v]) => v));
    return (await this.#req("GET", `/v1/sessions/${sessionId}/audit?${q}`)).events;
  }
  async perf() { return (await this.#req("GET", "/v1/perf")).tools; }
  async proofs() { return (await this.#req("GET", "/v1/proofs")).claims; }
  async billingCheckout(plan) { return this.#req("POST", "/v1/billing/checkout", { plan }); }
}
