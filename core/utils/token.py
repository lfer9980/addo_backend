from fastapi_login import LoginManager

from core import SECRET_KEY, API_PREFIX

Manager = LoginManager(SECRET_KEY,
                       token_url=API_PREFIX + '/auth' + '/login')
