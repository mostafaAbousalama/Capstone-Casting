import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
    Attempt to get the header from the request
    Raise an AuthError if no header is present
    Attempt to split bearer and the token
    Raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
   auth = request.headers.get('Authorization', None)
   if not auth:
       raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is expected.'
       }, abort(401))

   parts = auth.split()
   if parts[0].lower() != 'bearer':
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must start with "Bearer".'
       }, abort(401))

   elif len(parts) == 1:
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Token not found.'
       }, abort(401))

   elif len(parts) > 2:
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must be bearer token.'
       }, abort(401))

   token = parts[1]
   return token

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    Raise an AuthError if permissions are not included in the payload
    Raise an AuthError if the requested permission string is not
    in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, abort(400))

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, abort(401))
    return True

'''
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    Verify the token using Auth0 /.well-known/jwks.json
    Decode the payload from the token
    Validate the claims
    return the decoded payload
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, abort(401))

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, abort(401))

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, abort(401))
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, abort(400))
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, abort(400))

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    Use the get_token_auth_header method to get the token
    Use the verify_decode_jwt method to decode the jwt
    Use the check_permissions method validate claims
    and check the requested permission
    return the decorator which passes the decoded payload
    to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
            except AuthError:
                abort(401)
            try:
                payload = verify_decode_jwt(token)
            except AuthError:
                abort(401)
            try:
                check_permissions(permission, payload)
            except AuthError:
                abort(401)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
