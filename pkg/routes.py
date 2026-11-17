import smtplib
from datetime import datetime
from email.message import EmailMessage
from html import escape

from flask import render_template, request, Response, url_for

from pkg import app


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get('name') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        email = (request.form.get('email') or '').strip()
        subject = (request.form.get('subject') or '').strip()
        message_text = (request.form.get('message') or '').strip()

        if not name or not email or not message_text:
            return render_template(
                'contact.html',
                form_status={'kind': 'error', 'message': 'Please complete your name, email address, and message.'}
            )

        sender = app.config.get('MAIL_DEFAULT_SENDER')
        recipient = app.config.get('MAIL_CONTACT_RECIPIENT')
        username = app.config.get('MAIL_USERNAME')
        password = app.config.get('MAIL_PASSWORD')

        if not all([sender, recipient, username, password]):
            return render_template(
                'contact.html',
                form_status={'kind': 'error', 'message': 'Email is not configured yet. Please call or email the depot directly.'}
            )

        safe_name = escape(name)
        safe_phone = escape(phone or 'Not provided')
        safe_email = escape(email)
        safe_subject = escape(subject or 'General Enquiry')
        safe_message = escape(message_text)

        mail = EmailMessage()
        mail['Subject'] = f"Website enquiry: {subject or 'General Enquiry'}"
        mail['From'] = sender
        mail['To'] = recipient
        mail.set_content(
            f"Name: {name}\nPhone: {phone or 'Not provided'}\nEmail: {email}\n"
            f"Enquiry: {subject or 'General Enquiry'}\n\n{message_text}"
        )
        mail.add_alternative(
            f"""<div style="font-family:Arial,sans-serif;max-width:600px;color:#333">
                <h2 style="color:#00256C">New Juzzykuls Website Enquiry</h2>
                <p><strong>Name:</strong> {safe_name}</p>
                <p><strong>Phone:</strong> {safe_phone}</p>
                <p><strong>Email:</strong> {safe_email}</p>
                <p><strong>Enquiry type:</strong> {safe_subject}</p>
                <hr>
                <p style="white-space:pre-wrap">{safe_message}</p>
            </div>""",
            subtype='html'
        )

        try:
            if app.config.get('MAIL_USE_SSL'):
                smtp = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], timeout=20)
            else:
                smtp = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], timeout=20)

            with smtp:
                if app.config.get('MAIL_USE_TLS'):
                    smtp.starttls()
                smtp.login(username, password)
                smtp.send_message(mail)

            return render_template(
                'contact.html',
                form_status={'kind': 'success', 'message': 'Thank you! Your enquiry has been sent successfully.'}
            )
        except (smtplib.SMTPException, OSError, TimeoutError):
            return render_template(
                'contact.html',
                form_status={'kind': 'error', 'message': 'We could not send your enquiry. Please try again or contact us by phone.'}
            )

    return render_template('contact.html', form_status=None)

# ===== SEO: robots.txt =====
@app.route('/robots.txt')
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: https://www.juzzykuls.com/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")


# ===== SEO: sitemap.xml =====
@app.route('/sitemap.xml')
def sitemap():
    base = "https://www.juzzykuls.com"
    today = datetime.utcnow().strftime("%Y-%m-%d")
    pages = [
        {"loc": f"{base}/",        "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{base}/about",   "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base}/contact", "priority": "0.7", "changefreq": "monthly"},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for p in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{p['loc']}</loc>")
        xml.append(f"    <lastmod>{today}</lastmod>")
        xml.append(f"    <changefreq>{p['changefreq']}</changefreq>")
        xml.append(f"    <priority>{p['priority']}</priority>")
        xml.append("  </url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")
