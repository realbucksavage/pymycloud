import owncloud_utils.strings as stru
from apis.resource_base import ResourceBase
from database.models import Transmissions
from database.session import SessionFactoryPool


class ClientTransmissionApi(ResourceBase):

    def get(self):
        user = self.get_principal()
        _db = SessionFactoryPool.get_current_session()
        tran = _db.query(Transmissions).filter(
            Transmissions.user_id == user.id).first()

        if tran:
            return {'success': False}, 415

        tran = Transmissions()
        tran.user = user
        tran.transmission_type = Transmissions.TYPE_GET
        tran.transmission_key = stru.randstr()

        _db.add(tran)
        _db.commit()

        return {'transmission_key': tran.transmission_key, 'typ': 'GET'}

    def post(self):
        user = self.get_principal()
        _db = SessionFactoryPool.get_current_session()
        tran = _db.query(Transmissions).filter(
            Transmissions.user_id == user.id).first()

        if tran:
            return {'success': False}, 415

        tran = Transmissions()
        tran.user = user
        tran.transmission_type = Transmissions.TYPE_POST
        tran.transmission_key = stru.randstr()

        _db.add(tran)
        _db.commit()

        return {'transmission_key': tran.transmission_key, 'typ': 'POST'}
