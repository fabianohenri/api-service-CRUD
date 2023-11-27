from controller.version_controller import VersionController

from util.logging_format import LoggingFormat


class CheckDB:

    @staticmethod
    def validate():
        LoggingFormat.format("Inciando teste de conexão com o banco.", "Info")
        version = VersionController.get_version()
        if version:
            LoggingFormat.format(f"Conexão ao banco bem sucedida!", "Alert")
            LoggingFormat.format(f"Api Online - v {version}", "Success")
            return True
        else:
            message = "Erro ao conectar no banco. Verifique a string de conexão ou se o banco está ativo. "
            LoggingFormat.format(message, "Error")
            return False


