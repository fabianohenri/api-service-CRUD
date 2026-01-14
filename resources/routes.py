from api.service.status_api import StatusApi
from api.user.get import UserApiGet
from api.user.post import UserApiPost
from api.user.put import UserApiPut
from api.user.delete import UserApiDelete
from api.user_login import UserLoginApi
from api.version.get import VersionApiGet
from api.version.put import VersionApiPut


def initialize_routes(api):
    # Rotas de acesso aos endpoints da API
    # Rotas para userApis - Feita dessa forma para o swagger ficar mais limpo
    api.add_resource(UserApiGet,
                     f'/api/users',
                     f'/api/user/id/<int:user_id>',
                     f'/api/user/email/<string:user_email>')
    # Api.decorators = ['/user/email/{user_email}': ["parameters", {"tags": ['Infra Structure']]]
    api.add_resource(UserApiPost, f'/api/user')
    api.add_resource(UserApiPut, f'/api/user/id/<int:user_id>')
    api.add_resource(UserApiDelete, f'/api/user/id/<int:user_id>')

    api.add_resource(VersionApiGet, f'/api/version')
    api.add_resource(VersionApiPut, f'/api/version')

    api.add_resource(UserLoginApi, '/api/login')
    api.add_resource(StatusApi, '/api/status')
