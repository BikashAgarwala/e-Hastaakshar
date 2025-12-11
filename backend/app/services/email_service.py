import resend
from app.core.config import settings


class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.sender = settings.EMAIL_SENDER

    def send_signature_alert(self, recipient_email: str, user_name: str, location: dict, transaction_id: str):

        if not resend.api_key:
            print("⚠️ RESEND_API_KEY missing in settings. Skipping email.")
            return

        lat = location.get('latitude')
        lon = location.get('longitude')
        maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        verify_link = f"https://ehastaakshar-portal.com/verify/{transaction_id}"

        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #2563eb;">e-Hastaakshar Signature Alert</h2>
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>A new signature request has been processed securely.</p>

            <div style="background-color: #f9fafb; padding: 15px; margin: 15px 0; border-radius: 5px;">
                <p style="margin: 5px 0;"><strong>📍 Location:</strong> <a href="{maps_link}">View on Map</a></p>
                <p style="margin: 5px 0;"><strong>⏰ Time:</strong> {location.get('timestamp')}</p>
                <p style="margin: 5px 0;"><strong>🆔 Transaction ID:</strong> {transaction_id}</p>
            </div>

            <p>Your document is currently pending Partner Review.</p>

            <a href="{verify_link}" style="background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Status</a>

            <p style="font-size: 12px; color: #6b7280; margin-top: 20px;">
                If this wasn't you, please contact support immediately.
            </p>
        </div>
        """

        try:
            params = {
                "from": f"e-Hastaakshar <{self.sender}>",
                # "to": [recipient_email],
                "to": ["bikash.agarwala.01@gmail.com"],
                "subject": f"✅ Signature Processed: {transaction_id}",
                "html": html_content,
            }

            email = resend.Emails.send(params)
            print(f"📧 [RESEND] Email sent to {recipient_email}. ID: {email.get('id')}")
            return email

        except Exception as e:
            print(f"❌ [RESEND ERROR] Failed to send: {e}")


email_notifier = EmailService()