---
name: claim type / integration request
about: a claim you want gated, or a tool you want integrated
labels: enhancement
---

**The claim** — what should your agent have to *prove*?

```
claim: tests_passed          # example
target: {commit_sha}
evidence: what artifact shows it, produced by whom
```

**The failure you've seen** — what did a self-report let slip through?

**Would you write the fetcher?** (integrations.py has the GitHub Actions
pattern — ~30 lines)
