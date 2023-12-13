#Este é o arquivo principal, que deve ser executado para abrir o software


#Importa tudo que está no arquivo functions, incluindo as bibliotecas
from functions import *


#Classe da interface principal, essa é a classe que inicia todas as outras
class MainWindow(QMainWindow):
    #Fução que é executada sempre que o aplicativo inicia.
    #Tudo que tiver que rodar antes do aplicativo abrir deve ser colocada nesta função
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
        
    
    #Funções que fazem os textos clicáveis na interface principal terem funções    
    def label_4_click(self, event):
        UIFunction.pressed_button(self,"label_4")
    def label_6_click(self, event):
        UIFunction.pressed_button(self,"label_6")


#Todo o resto das funções se encontram no arquivo functions



        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
