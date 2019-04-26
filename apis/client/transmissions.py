import owncloud_utils.strings as stru
from apis.resource_base import ResourceBase
from database.models import Transmissions
from database.repositories import TransmissionRepository


class ClientTransmissionApi(ResourceBase):

    def get(self):
        user = self.get_principal()
        repo = TransmissionRepository.get_instance()
        tran = repo.get_by_user_id(user.id)

        if tran:
            return {'success': False}, 415

        tran = Transmissions()
        tran.user = user
        tran.transmission_type = Transmissions.TYPE_GET
        tran.transmission_key = stru.randstr()

        repo.create(tran)

        return {'transmission_key': tran.transmission_key, 'typ': 'GET'}

    def post(self):
        user = self.get_principal()
        repo = TransmissionRepository.get_instance()
        tran = repo.get_by_user_id(user.id)

        if tran:
            return {'success': False}, 415

        tran = Transmissions()
        tran.user = user
        tran.transmission_type = Transmissions.TYPE_UPLOAD
        tran.transmission_key = stru.randstr()

        repo.create(tran)

        return {'transmission_key': tran.transmission_key, 'typ': 'POST'}
