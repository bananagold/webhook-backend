from fastapi import FastAPI, Request, Header, HTTPException
import hmac, hashlib

app = FastAPI()
WEBHOOK_SECRET = "your-webhook-secret"  # Ideally passed via env var

@app.post("/webhook")
async def webhook(request: Request, x_signature: str = Header(None)):
    payload = await request.body()
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_signature or ""):
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()
    event = data.get("meta", {}).get("event_name")
    print(f"✅ Received: {event}")

    # Example: Handle subscription creation
    if event == "subscription_created":
        subscription = data["data"]
        print("New subscription:", subscription)

    return {"status": "ok"}
