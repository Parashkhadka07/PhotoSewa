from django.conf import settings
from django.core.mail import send_mail
import random

def email_verify(request,user):
    otp=random.randint(1000,9999)
    send_mail(
    subject='PhotoSewa | Security Verification Key',
    message='Welcome to PhotoSewa! Your security verification code is enclosed in the HTML version of this email. Authorized Access Only.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    html_message="""
    <div style="background-color: #050505; color: #ffffff; padding: 40px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: center; max-width: 500px; margin: 0 auto; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.08);">
        <h2 style="color: #4F46E5; font-weight: 800; letter-spacing: -0.05em; margin: 0 0 20px 0; font-size: 24px; text-transform: uppercase;">PHOTO<span style="color: #ffffff;">SEWA</span></h2>
        <p style="color: #9CA3AF; font-size: 14px; line-height: 1.6; margin: 0 0 32px 0;">Thanks for signing up to Nepal's premier photography marketplace. Enter the secure authentication key below to activate your account.</p>
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: inline-block; padding: 16px 40px; border-radius: 16px; font-size: 32px; font-weight: 800; letter-spacing: 0.2em; color: #ffffff; margin: 0 0 32px 0;">
            %s
        </div>
        <p style="color: #4b5563; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.1em;">Authorized Access Only.</p>
    </div>
    """% otp,
    fail_silently=False,
    )
    
