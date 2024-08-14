import logging
from hnt_sap_notify.common.tx_result import TxResult
logger = logging.getLogger(__name__)

class Su01Transaction:
    def __init__(self) -> None:
        pass

    def execute(self, sapGuiLib, user):
        sapGuiLib.run_transaction('/nSU01')
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/usr/ctxtSUID_ST_BNAME-BNAME").Text = user # Informa o user SAP
        sapGuiLib.session.findById("wnd[0]/tbar[1]/btn[7]").press()

        user_email = sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR/ssubMAINAREA:SAPLSUID_MAINTENANCE:1900/txtSUID_ST_NODE_COMM_DATA-SMTP_ADDR").Text # Captura o e-mail do user SAP
        tx_result = TxResult(user_email)
        logger.info(f"Leave execute id :'{str(tx_result)}'")
        return tx_result

