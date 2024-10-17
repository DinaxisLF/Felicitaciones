from flask import Blueprint

email_sender_class = Blueprint('email_sender', __name__)

from app.email_service import email_sender