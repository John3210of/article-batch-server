import requests
import logging
from django.conf import settings

def send_discord_embed(title, description=None, fields=None, color=0x3498db):
    """
    Send a detailed embed message to Discord via Webhook.

    :param title: Title of the embed
    :param description: Description of the embed (optional)
    :param fields: List of fields to include in the embed (optional)
                   Example: [{"name": "Field 1", "value": "Value 1", "inline": True}]
    :param color: Embed color (default: blue)
    """
    webhook_url = settings.DISCORD_WEBHOOK_URL
    embed = {
        "title": title,
        "description": description,
        "color": color,
    }

    # Add fields if provided
    if fields:
        embed["fields"] = fields

    payload = {"embeds": [embed]}

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logging.info(f"Discord embed sent: {title}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Discord embed: {e}")
