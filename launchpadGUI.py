import sys
import PyQt5
from PyQt5 import QtWidgets
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.resize(800,600)
        self.setWindowTitle("Isomorphic Launchpad Wrapper")
        self.statusBar().showMessage("No Controller Connected")




if __name__ == '__main__':
    app= QtWidgets.QApplication([]) #use sys.argv to take terminal input
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
