"""Webhook endpoints for CI/CD integration."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/scan-trigger")
async def webhook_scan_trigger(request: Request):
    """Trigger a scan from CI/CD pipeline webhook."""
    # TODO: Validate webhook signature, enqueue scan
    body = await request.json()
    return {"status": "accepted", "message": "Scan queued"}
