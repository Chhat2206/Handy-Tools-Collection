import imaplib
import smtplib
import email
from email.header import decode_header
import re

# Email account credentials
EMAIL = "your_email@gmail.com"
PASSWORD = "your_password"
IMAP_SERVER = "imap.your_email_provider.com"  # e.g., imap.gmail.com
SMTP_SERVER = "smtp.your_email_provider.com"  # e.g., smtp.gmail.com
SMTP_PORT = 587  # For TLS connections

def connect_to_email():
    """Connect to the email server."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        return mail
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def search_unsubscribe_emails(mail):
    """Search for emails with unsubscribe links."""
    mail.select("inbox")
    _, messages = mail.search(None, 'ALL')

    email_ids = messages[0].split()
    unsubscribe_links = []

    for email_id in email_ids:
        _, msg = mail.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Decode email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                # Search for unsubscribe link in email content
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode()
                            # Find unsubscribe links
                            links = re.findall(r'href=["\'](https?://[^"\']*unsubscribe[^"\']*)["\']', body, re.IGNORECASE)
                            unsubscribe_links.extend(links)
                else:
                    body = msg.get_payload(decode=True).decode()
                    links = re.findall(r'href=["\'](https?://[^"\']*unsubscribe[^"\']*)["\']', body, re.IGNORECASE)
                    unsubscribe_links.extend(links)
    return unsubscribe_links

def send_unsubscribe_requests(links):
    """Send unsubscribe requests."""
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        for link in links:
            print(f"Unsubscribing via: {link}")
            # Normally, you would click the link manually. Automating web interaction
            # for unsubscribing might require tools like Selenium or requests.

if __name__ == "__main__":
    mail = connect_to_email()
    if mail:
        print("Searching for emails with unsubscribe links...")
        links = search_unsubscribe_emails(mail)
        if links:
            print(f"Found {len(links)} unsubscribe links.")
            send_unsubscribe_requests(links)
        else:
            print("No unsubscribe links found.")
        mail.logout()
