from flask import request
from flask_restful import Resource

from database.models import Users
from database.session import SessionFactoryPool
import owncloud_utils.crypto as cryp
import owncloud_utils.strings as stru
import string


class ClientLoginApi(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']

        _session = SessionFactoryPool.get_current_session()
        user = _session.query(Users).filter(Users.username == username).first()

        if user and cryp.check_digest(password, user.password):
            if user.access_key is None:
                user.access_key = stru.randstr(
                    chars=(string.ascii_uppercase +
                           string.digits + string.ascii_lowercase),
                    len=32)

                _session.commit()

            return {'success': True, 'access_key': user.access_key}

        return {'success': False}, 403
