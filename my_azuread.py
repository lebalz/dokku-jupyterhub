"""
Custom Authenticator to use Azure AD with JupyterHub

"""
# import logging
# logging.basicConfig(filename='example_jwt.log', encoding='utf8', level=logging.DEBUG)

from jupyterhub.auth import LocalAuthenticator

from traitlets import default
from .azuread import AzureAdOAuthenticator


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


class LocalMyAzureAdOAuthenticator(LocalAuthenticator, MyAzureAdOAuthenticator):
    """A version that mixes in local system user creation"""
    pass
