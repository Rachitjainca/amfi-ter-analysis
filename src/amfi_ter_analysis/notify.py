"""Google Chat webhook notification."""

from __future__ import annotations

import logging
import os

import requests

log = logging.getLogger(__name__)
ENV_VAR = "GOOGLE_CHAT_WEBHOOK_URL"


def send(message: str, webhook_url: str | None = None, timeout: int = 30) -> bool:
    """Post `message` to the webhook in GOOGLE_CHAT_WEBHOOK_URL. Returns False when skipped or failed."""
    url = webhook_url or os.environ.get(ENV_VAR)
    if not url:
        log.info("%s is not set; skipping notification", ENV_VAR)
        return False
    if not url.startswith("https://chat.googleapis.com/"):
        log.error("%s must be a https://chat.googleapis.com/ URL", ENV_VAR)
        return False
    try:
        response = requests.post(url, json={"text": message}, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Do not log the exception text: it can contain the webhook key and token.
        log.error("notification failed (%s)", type(exc).__name__)
        return False
    log.info("notification sent")
    return True
