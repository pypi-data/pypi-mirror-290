from PySide6.QtWidgets import  QDialog, QFileDialog
from debyetools.tpropsgui.ui_dialog_outcar import Ui_Dialog as Ui_OUTCAR
from debyetools.aux_functions import load_EM as dt_load_EM

class dialogOUTCAR(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_OUTCAR()
        self.ui.setupUi(self)

        self.ui.browseoutcar.clicked.connect(self.getfilesoutcar)
        self.ui.ok.clicked.connect(self.on_pushButton_OK)
        self.filepath='.'

    def getfilesoutcar(self):
        outcarpath, _ = QFileDialog.getOpenFileName(self, caption='Select an OUTCAR file')
        self.ui.outcarpath.setText(outcarpath)

    def on_pushButton_OK(self):
        self.outcarpath = self.ui.outcarpath.text()
        self.close()
    def closeEvent(self, event):
        EM = dt_load_EM(self.outcarpath)

        txt2paste = ''
        for rowi in EM:
            txt2paste=txt2paste+' '.join(['%.2f'%(float(coli)/10) for coli in rowi])+'\n'
        self.elastic_constants.setText(txt2paste)
