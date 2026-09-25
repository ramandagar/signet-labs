# Contributing to var-runtime

Thanks for helping make agents prove their work.

## The one rule

Every behavioral change ships with a check. The repo runs three suites, all
dependency-free:

```bash
python3 test_runtime.py        # 7 core feature checks
python3 test_launch.py         # 5 launch-stack checks (boots real HTTP + MCP)
python3 evals/gate_evals.py    # 13 adversarial gate scenarios (exit 1 on fail)
```

If your change touches the gate, attestation, identity, or billing signature
verification, add a case to `evals/gate_evals.py` — one scenario, one correct
verdict.

## Ways to contribute

- **Evidence fetchers** — adapters for your CI/observability system
  (`var_runtime/integrations.py` has the GitHub Actions pattern to follow)
- **Proof Registry claim types** — new claim → evidence mappings in
  `proofs.json` (ship the eval case with it)
- **Framework adapters** — LangGraph/CrewAI/OpenAI Agents SDK glue
- **Recovery strategies** — SERF taxonomy extensions in `var_runtime/errors.py`

## Ground rules

- **Stdlib only** for the runtime core and API. Zero dependencies is a
  product decision (supply-chain surface, `pip install` portability).
  Dev-tool exceptions need a case in the PR.
- **Deterministic, replayable logic** in the runtime — no wall-clock reads
  inside verification paths (clocks are injectable; see `GateEngine.now`).
- **Constant-time comparisons** on every secret path (keys, signatures).
  If you touch `identity.py`/`server.py` auth, keep `hmac.compare_digest`.
- Money/verification code gets a test, not a comment.

## Pull requests

1. Fork, branch (`feat/…`, `fix/…`)
2. All three suites green locally
3. PR description: what claim does this make verifiable?

## Reporting a security issue

Email security@var-runtime.dev (or open a private security advisory on the
repo). Please do not open public issues for signature-verification bypasses.

## License

MIT — see LICENSE. Contributions are MIT-licensed.
