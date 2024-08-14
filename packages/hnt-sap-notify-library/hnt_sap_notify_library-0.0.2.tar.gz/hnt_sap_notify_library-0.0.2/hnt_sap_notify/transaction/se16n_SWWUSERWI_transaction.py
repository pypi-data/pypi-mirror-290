import logging
from hnt_sap_notify.common.tx_result import TxResult
logger = logging.getLogger(__name__)

class Se16nSWWUSERWITransaction:
    def __init__(selft) -> None:
        pass

    def execute(self, sapGuiLib, id):
        sapGuiLib.run_transaction('/nSE16N')
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/usr/ctxtGD-TAB").Text = "SWWUSERWI" # Informa tabela
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,2]").Text = id # Insere ID
        sapGuiLib.session.findById("wnd[0]/tbar[1]/btn[8]").press()

        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton("&MB_VIEW") # Ativa botão "Visões"
        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem("&PRINT_BACK_PREVIEW") # Seleciona "Saída list."
        user = sapGuiLib.session.findById("wnd[0]/usr/lbl[1,3]").Text # Captura o uer SAP
        tx_result = TxResult(user)
        logger.info(f"Leave execute user :'{str(tx_result)}'")
        return tx_result
