import os
import string

from flask_restful import Resource, reqparse

import owncloud_utils.crypto as cryp
import owncloud_utils.strings as stru
from apis import resource_base
from constants import constants
from database.models import Users
from database.session import SessionFactoryPool


class ClientLoginApi(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('username')
        self._parser.add_argument('password')

    def post(self):
        args = self._parser.parse_args(strict=True)
        username = args['username']
        password = args['password']

        _session = SessionFactoryPool.get_current_session()
        user = _session.query(Users).filter(Users.username == username).first()

        if user and cryp.check_digest(password, user.password):
            if user.access_key is None:
                user.access_key = stru.randstr(
                    chars=(string.ascii_uppercase
                           + string.digits + string.ascii_lowercase),
                    len=32)

                _session.commit()

            return {'success': True, 'access_key': user.access_key}

        return {'success': False}, 403


class ClientFileManagementApi(resource_base.ResourceBase):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('dir')
        self._parser.add_argument('access_key')

    def get(self):
        args = self._parser.parse_args(strict=True)

        user = self.get_principal()
        request_dir = args['dir']
        if request_dir is None:
            request_dir = '/'

        if not request_dir[0] == '/':
            request_dir = f"/{request_dir}"

        user_dir = f"{constants.work_dir}/{user.username}/_user{request_dir}"
        response = {'files': list(), 'dirs': list()}
        if os.path.exists(user_dir):
            for _f in os.listdir(user_dir):
                _coll = response['files'] if os.path.isfile(
                    f'{user_dir}{_f}') else response['dirs']
                _coll.append(_f)

            return response

        return {'success': False, 'message': f'{request_dir} does not exist'}, 404
