import asyncio
from app.services.email_service import EmailService

async def test_email():
    # Replace with your test email
    test_email = "kedar.vartak22@vit.edu"
    code = EmailService.generate_verification_code()
    
    print(f"Sending verification code {code} to {test_email}")
    result = await EmailService.send_verification_email(test_email, code)
    
    if result:
        print("Email sent successfully!")
    else:
        print("Failed to send email")

# Run the test
asyncio.run(test_email()) 