from flask_restx import Resource

from controller.user_controller import UsersController
from resources.authentication import auth


class UserApiGet(Resource):

    # @auth.login_required
    def get(self, user_id=None, user_email=None):
        """
                Retorna todos os utilizadores se o ‘token’ for valido.
                :parameter user_id: 'Int'.
                :parameter user_email: ‘String’.
                :return: lista utilizadores.
                """
        if user_id:
            response = UsersController.get_user_by_id(user_id=user_id)
        elif user_email:
            response = UsersController.get_user_by_email(user_email=user_email)
        else:
            response = UsersController.get_all_users()

        return response
