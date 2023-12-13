#This is the main file that should be run to open the software.


#This imports everything from the 'functions' file, including the libraries.
from functions import *


#Class of the main interface, this is the class that initiates all others.
class MainWindow(QMainWindow):
    #Function that is executed whenever the application starts.
    #Everything that needs to run before the application opens should be placed in this function.
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        applicationName = "ECOMMERCE HUB"
        self.setWindowTitle(applicationName)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.comboBox.setCurrentIndex(-1)
        self.ui.label_4.mousePressEvent = self.label_4_click
        self.ui.label_6.mousePressEvent = self.label_6_click
        self.ui.label_12.mousePressEvent = self.label_6_click
        self.ui.label_14.setText("")
        

        self.ui.bn_dashboard.clicked.connect((lambda:UIFunction.pressed_button(self,"bn_dashboard")))
        self.ui.bn_utilitarios.clicked.connect((lambda:UIFunction.pressed_button(self,"bn_utilitarios")))
        self.ui.lineEdit.returnPressed.connect((lambda:UIFunction.pressed_button(self,"pushButton_9")))
        self.ui.lineEdit_2.returnPressed.connect((lambda:UIFunction.pressed_button(self,"pushButton_9")))
        self.ui.pushButton_10.clicked.connect((lambda:UIFunction.pressed_button(self,"pushButton_10")))
        self.ui.pushButton_9.clicked.connect((lambda:UIFunction.pressed_button(self,"pushButton_9")))
        
    
    #Functions that make the clickable texts in the main interface have actions.   
    def label_4_click(self, event):
        UIFunction.pressed_button(self,"label_4")
    def label_6_click(self, event):
        UIFunction.pressed_button(self,"label_6")


#All the other functions are located in the 'functions' file



        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
