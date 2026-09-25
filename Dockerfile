# var-runtime API — zero-dependency image (stdlib Python only)
FROM python:3.12-slim

WORKDIR /app
COPY var_runtime/ var_runtime/
COPY frontend/ frontend/
COPY proofs.json cli.py demo.py test_runtime.py test_launch.py evals/ ./
RUN useradd -m var && chown -R var:var /app
USER var

ENV VAR_DB=/data/var.db
RUN mkdir -p /data && [ -w /data ] || true
VOLUME /data

EXPOSE 8788
# docker run -e VAR_SIGNING_KEY=<hex> -p 8788:8788 var-runtime
# Behind Caddy/nginx for TLS; scale with N containers on N ports.
CMD ["python3", "-u", "-m", "var_runtime.server", "--db", "/data/var.db", "--port", "8788", "--host", "0.0.0.0"]
