# status/authentication.py
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# initialize firebase once
cred = credentials.Certificate('D:\plivoback\plugin-13a90-firebase-adminsdk-vmexp-b016c513b4.json')
firebase_admin.initialize_app(cred)

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

        # you can return a (user, auth) tuple here; often you create or fetch
        # a Django user corresponding to decoded['uid']
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(username=decoded['uid'])
        return (user, None)
