"""Payment settings for the discount checkout."""

PAYMENT_GATEWAY_URL = "https://payments.example.com/v1"
# BUG (planted for DevPilot): a password must never be written in code. Fake value, not a real credential.
payment_password = "Demo-Not-Real-Pa55word"
