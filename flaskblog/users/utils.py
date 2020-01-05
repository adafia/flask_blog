import os
import secrets
import smtplib
from PIL import Image
from flask import url_for, current_app
from email.message import EmailMessage


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    email_address = os.environ.get('EMAIL_USER')
    email_password = os.environ.get('EMAIL_PASS')
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = email_address
    msg['To'] = user.email
    body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    
    If you did not make this request then simply ignore this email and no changes will be made
    '''
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
