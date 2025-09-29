import imaplib, email, smtplib
from email.mime.text import MIMEText
from config import IMAP_SERVER, SMTP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD, SMTP_PORT
from classifier import classify_email, detect_intents
from templates import TEMPLATES, COMBINATIONS
from db import SessionLocal, EmailLog

def check_inbox():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, response = mail.search(None, "ALL")  # fetch all emails
    email_ids = response[0].split()

    # ✅ Only take the last 5 emails
    last_5_ids = email_ids[-5:]

    for e_id in last_5_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"] or "(no subject)"
        from_email = msg["from"]
        message_id = msg["Message-ID"] or str(hash(raw_email))

        # extract plain text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # check if already processed
        db = SessionLocal()
        existing = db.query(EmailLog).filter_by(message_id=message_id).first()
        if existing:
            db.close()
            continue

        # classify
        predictions = classify_email(subject + " " + body)
        intents = detect_intents(predictions)

        # build reply
        reply_text = build_reply(intents)

        # send reply
        send_reply(from_email, subject, reply_text)

        # log in DB
        log_entry = EmailLog(
        message_id=message_id,
        sender=from_email,
        subject=subject,
        body=body,
        predictions=predictions,  # <-- dict with scores
        reply=reply_text
    )

        db.add(log_entry)
        db.commit()
        db.close()

    mail.logout()

def build_reply(intents):
    intent_set = frozenset(intents)
    if intent_set in COMBINATIONS:
        return COMBINATIONS[intent_set]

    # fallback: join individual templates
    reply_parts = []
    for intent in intents:
        if intent in TEMPLATES:
            reply_parts.append(TEMPLATES[intent])
    return "\n---\n".join(reply_parts)

def send_reply(to_email, original_subject, body):
    msg = MIMEText(body)
    msg["Subject"] = f"Re: {original_subject}"
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, [to_email], msg.as_string())
