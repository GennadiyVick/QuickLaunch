
from window import Ui_window
from mygraphicsview import MyGraphicsView

class Ui_panelwindow(Ui_window):
    def setupUi(self, window, width = 300, height = 300):
        super(Ui_panelwindow,self).setupUi(window,width,height)
        self.gv = MyGraphicsView(self.wcenter)
        self.gv.setObjectName("gv")
        self.centerLayout.addWidget(self.gv)
