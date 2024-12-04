import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def generate_verification_code() -> str:
        return str(random.randint(100000, 999999))

    @staticmethod
    async def send_verification_email(email: str, code: str) -> bool:
        try:
            sender_email = os.getenv('EMAIL_SENDER')
            password = os.getenv('EMAIL_PASSWORD')

            # Create multipart message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Verify your FINN account'
            msg['From'] = sender_email
            msg['To'] = email

            # Create HTML version of the email
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
                </style>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Inter', sans-serif; background-color: #f4f4f5;">
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="center" style="padding: 40px 0;">
                            <table role="presentation" width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                                <!-- Header -->
                                <tr>
                                    <td style="background-color: #000000; padding: 32px; text-align: center;">
                                        <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">FINN</h1>
                                    </td>
                                </tr>
                                
                                <!-- Content -->
                                <tr>
                                    <td style="padding: 48px 32px;">
                                        <h2 style="margin: 0 0 24px; color: #18181b; font-size: 20px; font-weight: 600;">Verify your email address</h2>
                                        <p style="margin: 0 0 24px; color: #3f3f46; font-size: 16px; line-height: 24px;">
                                            Thanks for signing up for FINN! Please use the verification code below to complete your registration.
                                        </p>
                                        
                                        <!-- Verification Code Box -->
                                        <div style="background-color: #f4f4f5; border-radius: 8px; padding: 24px; text-align: center; margin: 32px 0;">
                                            <span style="font-family: monospace; font-size: 32px; font-weight: 600; color: #18181b; letter-spacing: 4px;">
                                                {code}
                                            </span>
                                        </div>
                                        
                                        <p style="margin: 24px 0 0; color: #71717a; font-size: 14px; line-height: 20px;">
                                            This code will expire in 10 minutes. If you didn't request this code, you can safely ignore this email.
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: #f4f4f5; padding: 24px 32px; text-align: center;">
                                        <p style="margin: 0; color: #71717a; font-size: 14px;">
                                            © 2024 FINN. All rights reserved.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Footer Links -->
                            <table role="presentation" width="600" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td style="padding: 24px 32px; text-align: center;">
                                        <p style="margin: 0; color: #71717a; font-size: 14px;">
                                            <a href="#" style="color: #71717a; text-decoration: none; margin: 0 8px;">Privacy Policy</a> •
                                            <a href="#" style="color: #71717a; text-decoration: none; margin: 0 8px;">Terms of Service</a> •
                                            <a href="#" style="color: #71717a; text-decoration: none; margin: 0 8px;">Contact Support</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """

            # Create plain text version for email clients that don't support HTML
            text = f"""
            Welcome to FINN!
            
            Your verification code is: {code}
            
            This code will expire in 10 minutes.
            
            If you didn't request this code, please ignore this email.
            """

            # Add both plain text and HTML versions to the message
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Create secure SSL/TLS connection
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False 