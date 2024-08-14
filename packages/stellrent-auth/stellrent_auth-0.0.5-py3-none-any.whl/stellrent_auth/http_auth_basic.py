from decouple import config
from flask_httpauth import HTTPBasicAuth
import logging

basic_auth = HTTPBasicAuth()
__log = logging.getLogger()
__keys = eval(config('STLRNT_AUTH_BASIC_KEYS', cast=str))
__log.info('STLRNT_AUTH BasicAuth database lenght: ' + str(len(__keys)))

@basic_auth.verify_password
def verify_password(username, password):
    __log.debug('Requested username ' + username)
    for key in __keys:
        if key.get(username) is not None:
            __log.debug('Username founded. Validating password')
            if password == key[username]:
                __log.debug('Password match. Login granted!!!')
                return True
    return False
