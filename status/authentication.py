# status/authentication.py
import os
import json
import base64
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Load .env variables
load_dotenv()

# Get and decode the base64-encoded JSON
firebase_b64 = os.environ.get("FIREBASE_CREDENTIAL_BASE64")
if not firebase_b64:
    raise Exception("Missing FIREBASE_CREDENTIAL_BASE64 environment variable")

try:
    firebase_json = json.loads(base64.b64decode(firebase_b64).decode("utf-8"))
except Exception as e:
    raise Exception(f"Invalid Firebase credential JSON: {e}")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json)
    firebase_admin.initialize_app(cred)

# DRF auth class
class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header:
            return None

        token = header.split(' ').pop()
        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception:
            raise AuthenticationFailed('Invalid Firebase token')

        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(username=decoded['uid'])
        return (user, None)
