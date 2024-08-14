import logging
from botocore.exceptions import SSOTokenLoadError
from botocore.credentials import JSONFileCache
from botocore.utils import SSOTokenLoader
from botocore.credentials import JSONFileCache
from .vendored.awscli.sso.utils import SSO_TOKEN_DIR, _sso_json_dumps

logger = logging.getLogger()

def get_sso_token_by_start_url(start_url):
    token = None
    token_loader = SSOTokenLoader(JSONFileCache(SSO_TOKEN_DIR, dumps_func=_sso_json_dumps))

    try:
        token = token_loader(start_url)
    except SSOTokenLoadError:
        logger.debug("Token not found")
    except Exception as e:
        logger.debug(e)

    return token