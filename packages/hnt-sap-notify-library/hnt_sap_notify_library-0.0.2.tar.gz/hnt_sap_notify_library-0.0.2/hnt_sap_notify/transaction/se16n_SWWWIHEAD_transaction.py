import logging
from hnt_sap_notify.common.tx_result import TxResult
logger = logging.getLogger(__name__)

class Se16nSWWWIHEADTransaction:
    def __init__(selft) -> None:
        pass

    def execute(self, sapGuiLib, codigo_pedido):
        sapGuiLib.run_transaction('/nSE16N')
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/usr/ctxtGD-TAB").Text = 'SWWWIHEAD' # Informa tabela
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,5]").Text = f"*{codigo_pedido}" # Insere Doc Pedido
        sapGuiLib.session.findById("wnd[0]/tbar[1]/btn[8]").press()

        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").setCurrentCell(-1, "WI_STAT") # Ativa coluna "Status"
        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectColumn("WI_STAT") # Seleciona coluna "Status"
        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarButton("&MB_FILTER") # Abre filtro
        sapGuiLib.session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN001-LOW").Text = "READY" # Insere condição
        sapGuiLib.session.findById("wnd[1]/tbar[0]/btn[0]").press()

        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton("&MB_VIEW") # Ativa botão "Visões"
        sapGuiLib.session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem("&PRINT_BACK_PREVIEW") # Seleciona "Saída list."
        id = sapGuiLib.session.findById("wnd[0]/usr/lbl[1,3]").Text # Coleta ID na primeira linha da priemira coluna
        tx_result = TxResult(id)
        logger.info(f"Leave execute id :'{str(tx_result)}'")
        return tx_result
