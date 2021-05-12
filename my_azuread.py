"""
Custom Authenticator to use Azure AD with JupyterHub

""""""
Custom Authenticator to use Azure AD with JupyterHub

"""
import json
import jwt
import urllib

from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from jupyterhub.auth import LocalAuthenticator

from traitlets import default
from .azuread import AzureAdOAuthenticator


def azure_token_url_for(tentant):
    return 'https://login.microsoftonline.com/{0}/oauth2/token'.format(tentant)


def azure_authorize_url_for(tentant):
    return 'https://login.microsoftonline.com/{0}/oauth2/authorize'.format(
        tentant)


def sanitized_username(raw):
    cleaned_name = raw.lower()
    cleaned_name = cleaned_name.replace(',', '')
    cleaned_name = cleaned_name.replace(' ', '')
    cleaned_name = cleaned_name.replace('@', '--')
    cleaned_name = cleaned_name.replace('.', '-')

    if len(cleaned_name) > 31:
        # we need to shorten this because it won't work with the system's useradd!
        splitpos = cleaned_name.find("--")
        before = cleaned_name[0:splitpos]
        after = cleaned_name[splitpos:]
        remaining = 31 - len(after)
        shortened = before[0:remaining]
        cleaned_name = shortened + after
    return cleaned_name


class MyAzureAdOAuthenticator(AzureAdOAuthenticator):
    login_service = "Office365 GBSL"

    @default('username_claim')
    def _username_claim_default(self):
        return 'unique_name'

    def normalize_username(self, username):
        """
        Override normalize_username to avoid lowercasing usernames
        """
        return sanitized_username(username)

    async def authenticate(self, handler, data=None):
        code = handler.get_argument("code")
        http_client = AsyncHTTPClient()

        params = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='authorization_code',
            code=code,
            redirect_uri=self.get_callback_url(handler))

        data = urllib.parse.urlencode(
            params, doseq=True, encoding='utf-8', safe='=')

        url = azure_token_url_for(self.tenant_id)

        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = HTTPRequest(
            url,
            method="POST",
            headers=headers,
            body=data  # Body is required for a POST...
        )

        resp = await http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        # app_log.info("Response %s", resp_json)
        access_token = resp_json['access_token']

        id_token = resp_json['id_token']
        decoded = jwt.decode(id_token, verify=False)
        cleaned_name = sanitized_username(decoded[self.username_claim])

        userdict = {"name": cleaned_name}

        userdict["auth_state"] = auth_state = {}
        auth_state['access_token'] = access_token
        # results in a decoded JWT for the user data
        auth_state['user'] = decoded

        return userdict


class LocalMyAzureAdOAuthenticator(LocalAuthenticator, MyAzureAdOAuthenticator):
    """A version that mixes in local system user creation"""
    pass
