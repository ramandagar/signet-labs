"""Billing — Stripe Checkout + webhooks, stdlib only (REST + HMAC).

create_checkout: POSTs to Stripe's REST API (form-encoded, urllib) to open a
Checkout Session for a plan, returns the hosted payment URL.
handle_webhook: verifies the Stripe-Signature header (t=…,v1=… — HMAC-SHA256
of "{t}.{payload}" with the webhook secret, constant-time compare, 5-minute
replay window), then maps checkout.session.completed / subscription lifecycle
events onto the customers table, upgrading the tenant's api_keys plan.

Config (env): STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
STRIPE_PRICE_PRO, STRIPE_PRICE_TEAM. Test mode: sk_test_/whsec_ keys.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request

from .server import ApiError

STRIPE_API = "https://api.stripe.com/v1"
PLANS = {  # price ids come from env; tiers mirror README pricing
    "pro": {"env": "STRIPE_PRICE_PRO", "name": "VAR Pro", "amount": 4900},
    "team": {"env": "STRIPE_PRICE_TEAM", "name": "VAR Team", "amount": 49900},
}


def _stripe_post(path: str, data: dict, secret: str) -> dict:
    req = urllib.request.Request(
        STRIPE_API + path, data=urllib.parse.urlencode(data).encode(),
        headers={"Authorization": f"Bearer {secret}",
                 "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ApiError(502, "STRIPE_ERROR",
                       f"stripe {e.code}: {e.read().decode()[:300]}")


def create_checkout(api, auth: dict, body: dict) -> tuple[int, dict]:
    plan = body.get("plan")
    if plan not in PLANS:
        raise ApiError(400, "VALIDATION", f"plan must be one of {sorted(PLANS)}")
    if not api.stripe_secret:
        raise ApiError(503, "BILLING_UNCONFIGURED",
                       "set STRIPE_SECRET_KEY to enable checkout")
    price = os.environ.get(PLANS[plan]["env"])
    if not price:
        raise ApiError(503, "BILLING_UNCONFIGURED",
                       f"set {PLANS[plan]['env']} (Stripe price id for {plan})")

    session = _stripe_post("/checkout/sessions", {
        "mode": "subscription",
        "line_items[0][price]": price,
        "line_items[0][quantity]": "1",
        "success_url": body.get("success_url", os.environ.get(
            "VAR_BASE_URL", "http://localhost:8788") + "/app?billing=success"),
        "cancel_url": body.get("cancel_url", os.environ.get(
            "VAR_BASE_URL", "http://localhost:8788") + "/app?billing=cancelled"),
        "client_reference_id": auth["tenant"],
        "metadata[tenant]": auth["tenant"],
        "metadata[plan]": plan,
        "allow_promotion_codes": "true",
    }, api.stripe_secret)
    return 200, {"checkout_url": session["url"],
                 "session_id": session["id"], "plan": plan}


def verify_webhook_signature(payload: bytes, header: str, secret: str,
                             tolerance: int = 300) -> bool:
    try:
        parts = dict(p.split("=", 1) for p in header.split(","))
        t, v1 = parts["t"], parts["v1"]
    except (ValueError, KeyError):
        return False
    if abs(time.time() - int(t)) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{t}.".encode() + payload,
                        hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, v1)


def handle_webhook(api, payload: bytes, signature: str | None = None) -> tuple[int, dict]:
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not secret:
        # fail closed: unsigned acceptance would let anyone upgrade their plan
        raise ApiError(503, "BILLING_UNCONFIGURED",
                       "set STRIPE_WEBHOOK_SECRET — unsigned webhooks are never accepted")
    if not signature or not verify_webhook_signature(payload, signature, secret):
        raise ApiError(400, "INVALID_SIGNATURE", "webhook signature invalid")
    event = json.loads(payload)
    et = event.get("type", "")
    obj = event.get("data", {}).get("object", {})

    if et == "checkout.session.completed":
        tenant = obj.get("client_reference_id") or obj.get("metadata", {}).get("tenant")
        plan = obj.get("metadata", {}).get("plan", "pro")
        sub = obj.get("subscription")
        if tenant:
            api.db.execute(
                "INSERT INTO customers(tenant, stripe_customer_id, "
                "stripe_subscription_id, plan, status, current_period_end) "
                "VALUES (?,?,?,?,?,?) ON CONFLICT(tenant) DO UPDATE SET "
                "stripe_subscription_id=excluded.stripe_subscription_id, "
                "plan=excluded.plan, status=excluded.status",
                (tenant, obj.get("customer"), sub, plan, "active", None))
            api.db.execute("UPDATE api_keys SET plan=? WHERE tenant=? AND revoked=0",
                           (plan, tenant))
            api.db.commit()
            return 200, {"status": "activated", "tenant": tenant, "plan": plan}
    elif et in ("customer.subscription.deleted", "invoice.payment_failed"):
        sub_tenant = api.db.execute(
            "SELECT tenant FROM customers WHERE stripe_subscription_id=?",
            (obj.get("id"),)).fetchone()
        if sub_tenant:
            api.db.execute("UPDATE customers SET status=?, plan='free' WHERE tenant=?",
                           ("cancelled" if "deleted" in et else "past_due", sub_tenant[0]))
            api.db.execute("UPDATE api_keys SET plan='free' WHERE tenant=?",
                           (sub_tenant[0],))
            api.db.commit()
            return 200, {"status": "downgraded", "tenant": sub_tenant[0]}
    return 200, {"status": "ignored", "type": et}
