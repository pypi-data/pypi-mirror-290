import json
import logging
import locale
from SapGuiLibrary import SapGuiLibrary
from dotenv import load_dotenv

from hnt_sap_notify.RPA_HNT_Constants import COD_LIBERACAO_BLOQUADO
from hnt_sap_notify.transaction.me2n_transaction import Me2nTransaction
from hnt_sap_notify.transaction.se16n_SWWUSERWI_transaction import Se16nSWWUSERWITransaction
from hnt_sap_notify.transaction.se16n_SWWWIHEAD_transaction import Se16nSWWWIHEADTransaction
from hnt_sap_notify.transaction.su01_transaction import Su01Transaction
from .common.session import sessionable
logger = logging.getLogger(__name__)
class SapGui(SapGuiLibrary):
    def __init__(self) -> None:
        SapGuiLibrary.__init__(self, screenshots_on_error=True)
        locale.setlocale(locale.LC_ALL, ('pt_BR.UTF-8'))
        load_dotenv()
        pass
    def format_float(self, value):
        return locale.format_string("%.2f", value)

    @sessionable
    def email_approvers(self, cod_pedidos):
        logger.info(f"Enter execute email_approvers cod_pedidos:{cod_pedidos}")
        results = []
        for cod_pedido in cod_pedidos:
            result = {
                "email": None,
                "error": None
            }
            try:
                tx_result_liberacao = Me2nTransaction().execute(self, cod_pedido)
                if COD_LIBERACAO_BLOQUADO == tx_result_liberacao.codigo:
                    tx_result_id = Se16nSWWWIHEADTransaction().execute(self, cod_pedido)
                    tx_result_user = Se16nSWWUSERWITransaction().execute(self, tx_result_id.codigo)
                    tx_result_email = Su01Transaction().execute(self, tx_result_user.codigo)
                    results.append({
                        'cod_pedido': cod_pedido,
                        'email': tx_result_email.codigo
                    })
            except Exception as ex:
                logger.error(str(ex))
                result["error"] = str(ex)
            
        logger.info(f"Leave execute email_approvers results:{results}")
        return results