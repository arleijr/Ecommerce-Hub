#Importa todas as bibliotecas necessárias para o funcionamento do programa

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, QFileInfo)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
from PySide6 import QtCharts
import datetime
import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from ui_main import Ui_MainWindow 
import bcrypt
import re
import pandas as pd
from babel.numbers import format_decimal
import locale
import sys
import time
import numpy as np
from PySide6.QtWidgets import *
from ui_dashboard import Ui_Dashboard
from ui_bases import Ui_Bases
from ui_utilitarios import Ui_Utilitario
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



#Configura o local da biblioteca "locale" pata pt_BR. Usado aqui para formatar valores monetários em Real.
locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')



#Classe de funções da interface principal. Aqui contém todas as funções presentes na interface "Ecommerce Hub"
class UIFunction:
    def __init__(self):
        pass

    #Vai para a página de login
    def page_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page) 

    #Vai para a página de cadastro
    def page_cadastro(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)

    #Valida as informações inseridas no campo de cadastro de novo usuário
    def cadastro(self):
        ok_name = False
        ok_user = False
        ok_password = False
        ok_group = False

        #Barra para inserir o nome
        self.nome_input = self.ui.lineEdit_3.text()
        if len(self.nome_input)<1:
            self.ui.label_19.setText('O nome não pode estar vazio')
        else:
            val_name = re.fullmatch("^.+[^0-9!@#$%&\*\.]$",self.nome_input)
            if val_name:
                self.ui.label_19.setText('')
                ok_name = True
            else:
                self.ui.label_19.setText('O nome não pode conter caracteres especiais ou números')
        
        #Barra para inserir o usuário
        self.user_input = self.ui.lineEdit_4.text()
        if len(self.user_input) < 4:
            self.ui.label_18.setText('O nome de usuário deve ter no mínimo 4 caracteres')
        else:
            val_user = re.fullmatch("^.+[A-Za-z0-9\.\_]$", self.user_input)
            if val_user:
                self.ui.label_18.setText('')
                ok_user = True
            else:
                self.ui.label_18.setText('O nome de usuário só pode conter letras, números, "." e "_"')


        #Validação de senha
        #Barra para inserir a senha
        self.input_password_cad = self.ui.lineEdit_5.text()
        
        if len(self.input_password_cad) <6:
            self.ui.label_17.setText('A senha deve conter no mínimo 6 caracteres')  
        else:
            val_password = re.fullmatch(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$",self.input_password_cad)
            if val_password:
                self.ui.label_17.setText('')
                self.password = UIFunction.hash_password(self)
                ok_password = True
            else:
                self.ui.label_17.setText('A senha deve conter letra maiúscula, letra minúscula e número')
        
        #Combobox para selecionar o grupo na área de cadastro
        self.group_input = self.ui.comboBox.currentText()
        if self.group_input != "":
            ok_group = True
            self.ui.label_20.setText('')
        else:
            self.ui.label_20.setText('Você deve selecionar uma área de atuação')
        
        if ok_name and ok_user and ok_password and ok_group:
            UIFunction.info_to_sql(self)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
    
    #Manda as informações de cadastro para o banco de dados
    def info_to_sql(self):
        file_path = "dados/user_autentication.xlsx"
        file_user_info = pd.read_excel(file_path)
        user_info = pd.DataFrame({"username":[self.user_input],"password":[self.password],"name":[self.nome_input],"group":[self.group_input]})
        updated_df = pd.concat([file_user_info,user_info], ignore_index=True)
        updated_df.to_excel("dados/user_autentication.xlsx", index=False)
        
    #Criptografa a senha cadastrada pelo usuário
    def hash_password(self):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.input_password_cad.encode("utf-8"),salt)
        hashed_password = hashed_password.decode("utf-8")
        return hashed_password
    
    #Função que realiza o login do usuário
    def login(self):
    
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        file_path = "dados/user_autentication.xlsx"
        file_info = pd.read_excel(file_path)
        user_info = file_info[file_info['username']==username]
        
        sql_password = user_info['password'].values[0]
        sql_name = user_info['name'].values[0]
        global sql_group
        sql_group = user_info['group'].values[0]
        
        check_password = bcrypt.checkpw(password.encode("utf-8"),sql_password.encode('utf-8'))
        if check_password:
            self.ui.label_13.setText(f'Bem-vindo(a) {sql_name}')
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)
        else:
            self.ui.label_21.setText("Usuário ou senha inválido")
  
        access = ["Ecommerce - Gestão","Ecommerce - Inteligência"]
        if sql_group not in access:
            self.ui.bn_relatorios.setDisabled(True)
            self.ui.bn_relatorios.setStyleSheet('QPushButton {	border-color: rgb(255, 255, 255);	border: none;	border-width: 2px;	border-radius: 10px;		font: 600 16pt "Bahnschrift SemiBold Condensed";				background-color: rgb(80, 80, 80);	color:rgb(0, 0, 0);}QPushButton:hover {		background-color: rgb(166, 166, 166);}QPushButton:pressed {		background-color: rgb(70, 70, 70);}')
    #except:
            #self.ui.label_14.setStyleSheet('color: rgb(255, 0, 0)')
            #self.ui.label_14.setText("Usuário ou senha incorretos")
    #retorna o grupo do usuário para validação
    def retornar_grupo(self):
        grupo = sql_group
        return grupo
        
    

    
    #Conecta os botões clicados às funções da interface principal
    def pressed_button(self, button):

        #Conecta o texto clicável "cadastre-se" à função que vai para a pagina de cadastro
        if button == "label_4":
            UIFunction.page_cadastro(self)

        #Conecta o botão à função de cadastro
        if button == "pushButton_10":
            UIFunction.cadastro(self)

        #Conecta o botão de login à função de login
        if button == "pushButton_9":
            UIFunction.login(self)

        #Abre a interface de "Ações" através do botão "ações"
        if button == "bn_acoes":
            self.w = Validador()
            self.w.show()

        if button=="label_6":
            UIFunction.page_login(self)
        #Abre a interface "Dashboard" através do botão "dashboard"
        if button == "bn_dashboard":
            self.y = Dashboard()
            self.y.show()
            #self.ui.label_22.setText("")
        if button == "loading":
            time.sleep(5)
            self.ui.label_22.setText("Carregando")

        #Abre a interface relatórios
        if button == "bn_relatorios":
            self.bases = Bases()
            self.bases.show()
        
        #Abre a interface web
        if button == "bn_web":
            self.web = Web()
            self.web.show()
        
        if button == "bn_utilitarios":
            self.utilitario = Utilitario()
            self.utilitario.show()





#classe da interface do Dashboard
class Dashboard(QWidget):

    #Executa quando o Dashboard for iniciado
    def __init__(self):
        super().__init__()
        self.dashboard_ui = Ui_Dashboard()
        self.dashboard_ui.setupUi(self)
        #self.ui = Ui_MainWindow()
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.dashboard_ui.centralwidget)
        self.setLayout(self.layout2)
        
        self.setWindowTitle("Ecommerce Dashboard")

        self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_about_android)
        #Dashboard_func.constantFunction(self)
        

        self.dashboard_ui.widget.setStyleSheet(u"background-color: transparent")
        self.dashboard_ui.widget_6.setStyleSheet(u"background-color: transparent")
        self.dashboard_ui.widget_3.setStyleSheet(u"background-color: transparent")
        self.dashboard_ui.frame_toodle.setStyleSheet("background-color: rgba(22,17,58,255)")
        self.dashboard_ui.lab_home_main_hed_37.hide()
        self.dashboard_ui.lab_home_main_hed_38.hide()
        self.dashboard_ui.lab_home_main_hed_39.hide()
        self.dashboard_ui.lab_home_main_hed_40.hide()
        self.dashboard_ui.lab_home_main_hed_41.hide()
        self.dashboard_ui.lab_home_main_hed_42.hide()
        self.dashboard_ui.lab_home_main_hed_43.hide()
        self.dashboard_ui.lab_home_main_hed_44.hide()
        self.dashboard_ui.lab_home_main_hed_45.hide()
        self.dashboard_ui.lab_home_main_hed_46.hide()
        self.dashboard_ui.lab_home_main_hed_47.hide()
        self.dashboard_ui.lab_home_main_hed_48.hide()
        self.first_time_open = True
        
    #Executa quando o Dashboard for aberto pela primeira vez
    def showEvent(self, event):

        #Verifica se é a primeira vez que está sendo aberto
        if self.first_time_open:
            
            
            #Esconde alguns elementos que não serão usados no início
            self.dashboard_ui.lab_home_main_hed_67.hide()
            self.dashboard_ui.lab_home_main_hed_68.hide()
            self.dashboard_ui.lab_home_main_hed_24.hide()
            self.dashboard_ui.toodle.hide()
            self.dashboard_ui.widget_2.setStyleSheet("background-color:transparent")
            self.dashboard_ui.widget_10.setStyleSheet("background-color:transparent")
            self.dashboard_ui.widget_11.setStyleSheet("background-color:transparent")
            self.dashboard_ui.widget_12.setStyleSheet("background-color:transparent")
            self.dashboard_ui.lab_home_main_hed_70.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
            self.dashboard_ui.lab_home_main_hed_51.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
            self.dashboard_ui.lab_home_main_hed_69.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
            
            #configura o dia de hoje e o dia que estará disponível para a seleção do usuário no Dashboard
            today = datetime.date.today()
            minimumtd = today + datetime.timedelta(days=-90)
            yesterday = today + datetime.timedelta(days=-1)
            yesterday_day = yesterday.day
            yesterday_month = yesterday.month
            yesterday_year = yesterday.year
            today_day = today.day
            today_month = today.month
            self.today_month = today_month
            self.today_day = today_day
            today_year = today.year
            self.today_year = today_year
            min_day = minimumtd.day
            min_month = minimumtd.month
            min_year = minimumtd.year
            self.dashboard_ui.dateEdit.setMinimumDate(QtCore.QDate(QtCore.QDate(min_year,min_month,min_day)))
            self.dashboard_ui.dateEdit.setMaximumDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))
            self.dashboard_ui.dateEdit.setDate(QtCore.QDate(QtCore.QDate(yesterday_year,yesterday_month,yesterday_day)))
            self.dashboard_ui.dateEdit_2.setMinimumDate(QtCore.QDate(QtCore.QDate(min_year,min_month,min_day)))
            self.dashboard_ui.dateEdit_2.setMaximumDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))
            self.dashboard_ui.dateEdit_2.setDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))

            self.dashboard_ui.dateEdit_3.setMinimumDate(QtCore.QDate(QtCore.QDate(min_year,min_month,min_day)))
            self.dashboard_ui.dateEdit_3.setMaximumDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))
            self.dashboard_ui.dateEdit_3.setDate(QtCore.QDate(QtCore.QDate(yesterday_year,yesterday_month,yesterday_day)))
            self.dashboard_ui.dateEdit_4.setMinimumDate(QtCore.QDate(QtCore.QDate(min_year,min_month,min_day)))
            self.dashboard_ui.dateEdit_4.setMaximumDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))
            self.dashboard_ui.dateEdit_4.setDate(QtCore.QDate(QtCore.QDate(today_year,today_month,today_day)))

            
            #Conecta os botões do Dashboard com a função buttonPressed, que dá função aos botões
            self.dashboard_ui.bn_mgl.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_mgl"))
            self.dashboard_ui.bn_via.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_via"))
            self.dashboard_ui.bn_bww.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_bww"))
            self.dashboard_ui.bn_mcl.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_mcl"))
            self.dashboard_ui.bn_amz.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_amz"))
            self.dashboard_ui.bn_cev.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_cev"))
            self.dashboard_ui.bn_crf.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_crf"))
            self.dashboard_ui.bn_zmm.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_zmm"))
            self.dashboard_ui.bn_lry.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_lry"))
            self.dashboard_ui.bn_shopee.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_shopee"))
            self.dashboard_ui.bn_inter.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_inter"))
            self.dashboard_ui.bn_kbm.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_kbm"))
            self.dashboard_ui.bn_mgl_2.clicked.connect(lambda: Dashboard_func.buttonPressed(self,"bn_mgl_2"))
            self.dashboard_ui.dateEdit.dateChanged.connect(lambda: Dashboard_func.buttonPressed(self,"dateEdit"))
            self.dashboard_ui.dateEdit_2.dateChanged.connect(lambda: Dashboard_func.buttonPressed(self,"dateEdit_2"))
            self.dashboard_ui.dateEdit_3.dateChanged.connect(lambda: Dashboard_func.buttonPressed(self,"dateEdit_3"))
            self.dashboard_ui.dateEdit_4.dateChanged.connect(lambda: Dashboard_func.buttonPressed(self,"dateEdit_4"))
            self.execute_functions()
            

    #Executa as funções iniciais necessárias para o programa rodar, como import de tabelas e cálculos        
    def execute_functions(self):
        Dashboard_func.import_tables(self)
        Dashboard_func.set_marketplace(self,13)
        Dashboard_func.create_bar_graph(self)
        Dashboard_func.dashboard_geral(self)
        self.first_time_open = False



class Utilitario(QWidget):
    #Executado sempre que o programa é iniciado
    def __init__(self):
        super().__init__()
        self.utilitario_ui = Ui_Utilitario()
        self.utilitario_ui.setupUi(self)
        #self.ui = Ui_MainWindow()
        self.layout6 = QVBoxLayout()
        self.layout6.addWidget(self.utilitario_ui.centralwidget)
        self.setLayout(self.layout6)
        
        self.setWindowTitle("Utilitários")
        self.utilitario_ui.stackedWidget.setCurrentWidget(self.utilitario_ui.page_4)
        self.utilitario_ui.bn_relatorios.clicked.connect((lambda:Utilitario_func.buttonPressed(self,"bn_relatorios")))
        self.utilitario_ui.pushButton_9.clicked.connect((lambda:Utilitario_func.buttonPressed(self,"pushButton_9")))

class Utilitario_func:
    def __init__(self):
        pass
    def buttonPressed(self,button):
        if button=="bn_relatorios":
            self.utilitario_ui.stackedWidget.setCurrentWidget(self.utilitario_ui.page)
        if button=="pushButton_9":
            Utilitario_func.find_sku(self)
    
    def find_sku(self):
        self.utilitario_ui.label_4.setText(f"")
        self.utilitario_ui.label_16.setText(f"")
        self.utilitario_ui.label_27.setText(f"")
        self.utilitario_ui.label_22.setText(f"")
        self.utilitario_ui.label_23.setText(f"")
        self.utilitario_ui.label_30.setText(f"")

        sku = self.utilitario_ui.lineEdit_2.text()
        sku = int(sku)
        sku_info = pd.read_excel("dados/estoque.xlsx")
        sku_info = sku_info[sku_info["SKU"]==sku]
        sku_info = sku_info.drop_duplicates("SKU",keep="last")
        material = sku_info["SKU"].values[0]
        produto = sku_info["Produto"].values[0]
        categoria = sku_info["Categoria"].values[0]
        tipo = sku_info["Tipo"].values[0]
        marca = sku_info["Marca"].values[0]
        valor = sku_info["Valor"].values[0]

        self.utilitario_ui.label_4.setText(f"SKU: {material}")
        self.utilitario_ui.label_16.setText(f"Produto: {produto}")
        self.utilitario_ui.label_27.setText(f"Valor: R${valor}")
        self.utilitario_ui.label_22.setText(f"Marca: {marca}")
        self.utilitario_ui.label_23.setText(f"Categoria: {categoria}")
        self.utilitario_ui.label_30.setText(f"Tipo: {tipo}")






#Classe de funções da interface Dashboard
class Dashboard_func:
    def __init__(self):
        pass

    #Configura o widget que aparece inicialmente
    def initStackTab(self):
        global init
        if init==False:
            self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
            self.dashboard_ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True

    #Configura o título da janela
    def labelTitle(self, appName):
        self.dashboard_ui.lab_appname.setText(appName)
        self.dashboard_ui.lab_appname.setStyleSheet("color: rgb(240, 240, 240);background-color: rgba(22,17,58,255)")
    


    
    #Cria os gráficos do dashboard
    def create_bar_graph(self):
        self.set5 = QtCharts.QBarSet("Venda")
        self.set5.append([])
        self.barSeries2 = QtCharts.QBarSeries()
        self.barSeries2.append(self.set5)
        self.chart2 = QtCharts.QChart()
        self.chart2.addSeries(self.barSeries2)
        self.chart2.setTitle("Diarização")
        self.categories2 = []
        self.axisX2 = QtCharts.QBarCategoryAxis()
        self.axisX2.append(self.categories2)
        self.chart2.setAxisX(self.axisX2, self.barSeries2)
        self.axisX2.setRange("01/06", "19/06")
        self.axisY2 = QtCharts.QValueAxis()
        self.chart2.setAxisY(self.axisY2, self.barSeries2)
        self.axisY2.setRange(0, 1000.00)
        self.chart2.legend().setVisible(True)
        self.chart2.legend().setAlignment(Qt.AlignBottom)
        self.chartView2 = QtCharts.QChartView(self.chart2)
        self.chartView2.setRenderHint(QPainter.Antialiasing)
        self.chart2.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.chartView2.chart().setTheme(QtCharts.QChart.ChartThemeDark)
        self.chartView2.chart().setBackgroundBrush(QBrush(QColor("transparent")))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartView2.sizePolicy().hasHeightForWidth())
        self.chartView2.setSizePolicy(sizePolicy)
        self.chartView2.setMinimumSize(QtCore.QSize(0, 300))
        self.dashboard_ui.bar_charts_cont_4.addWidget(self.chartView2, 0, 0, 9, 9)
        self.dashboard_ui.frame_21.setStyleSheet(u"background-color: transparent")
        self.dashboard_ui.frame_13.setStyleSheet(u"background-color: transparent")
        self.dashboard_ui.widget_5.setStyleSheet(u"background-color: transparent")


    #Calcula e retorna os valores de venda do dashboard geral
    def dashboard_geral(self):
        self.datefrom =  self.dashboard_ui.dateEdit_3.date()
        self.datetill =  self.dashboard_ui.dateEdit_4.date()
        self.from_day = self.datefrom.day()
        self.from_month = self.datefrom.month()
        self.from_year = self.datefrom.year()
        self.date_de = (f"{self.from_year}-{self.from_month}-{self.from_day}")
        self.date_de = self.date_de.format("%Y/%m/%d")
        today = datetime.date.today()
        today_month = today.month
        today_year = today.year
        self.ate_day = self.datetill.day()
        self.ate_month = self.datetill.month()
        self.ate_year = self.datetill.year()
        self.date_ate = (f"{self.ate_year}-{self.ate_month}-{self.ate_day}")
        self.date_ate = self.date_ate.format("%Y/%m/%d")
        self.datas = pd.date_range(start=self.date_de, end=self.date_ate)
        data_from = self.date_de
        data_until = self.date_ate
        self.sql_df['Data'] = pd.to_datetime(self.sql_df['Data'], format="%d/%m/%Y")
        venda_mes = self.sql_df[(self.sql_df["Mes"]==today_month)&(self.sql_df["Ano"]==today_year)]
        venda_mes_total = venda_mes['Venda Total'].sum()

        self.magalu = self.sql_df[(self.sql_df['SalesChannel']==13) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.via = self.sql_df[(self.sql_df['SalesChannel']==4) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.bww = self.sql_df[(self.sql_df['SalesChannel']==6) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.mcl = self.sql_df[(self.sql_df['SalesChannel']==17) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.amz = self.sql_df[(self.sql_df['SalesChannel']==12) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.cev = self.sql_df[(self.sql_df['SalesChannel']==18) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.crf = self.sql_df[(self.sql_df['SalesChannel']==8) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.zmm = self.sql_df[(self.sql_df['SalesChannel']==7) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.lry = self.sql_df[(self.sql_df['SalesChannel']==14) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.shopee = self.sql_df[(self.sql_df['SalesChannel']==1) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.inter = self.sql_df[(self.sql_df['SalesChannel']==15) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]
        self.kbm = self.sql_df[(self.sql_df['SalesChannel']==21) & (self.sql_df['Data']>=data_from) & (self.sql_df['Data']<=data_until)]

        self.magalu_venda = self.magalu['Venda Total'].sum()
        self.via_venda = self.via['Venda Total'].sum()
        self.bww_venda = self.bww['Venda Total'].sum()
        self.mcl_venda = self.mcl['Venda Total'].sum()
        self.amz_venda = self.amz['Venda Total'].sum()
        self.cev_venda = self.cev['Venda Total'].sum()
        self.crf_venda = self.crf['Venda Total'].sum()
        self.zmm_venda = self.zmm['Venda Total'].sum()
        self.lry_venda = self.lry['Venda Total'].sum()
        self.inter_venda = self.inter['Venda Total'].sum()
        self.kbm_venda = self.kbm['Venda Total'].sum()
        self.shopee_venda = self.shopee['Venda Total'].sum()

        self.magalu_mc = (self.magalu["MC"].sum())/(self.magalu["Venda Total"].sum())
        self.via_mc = (self.via["MC"].sum())/(self.via["Venda Total"].sum())
        self.bww_mc = (self.bww["MC"].sum())/(self.bww["Venda Total"].sum())
        self.mcl_mc = (self.mcl["MC"].sum())/(self.mcl["Venda Total"].sum())
        self.amz_mc = (self.amz["MC"].sum())/(self.amz["Venda Total"].sum())
        self.cev_mc = (self.cev["MC"].sum())/(self.cev["Venda Total"].sum())
        self.crf_mc = (self.crf["MC"].sum())/(self.crf["Venda Total"].sum())
        self.zmm_mc = (self.zmm["MC"].sum())/(self.zmm["Venda Total"].sum())
        self.lry_mc = (self.lry["MC"].sum())/(self.lry["Venda Total"].sum())
        self.inter_mc = (self.inter["MC"].sum())/(self.inter["Venda Total"].sum())
        self.kbm_mc = (self.kbm["MC"].sum())/(self.kbm["Venda Total"].sum())
        self.shopee_mc = (self.shopee["MC"].sum())/(self.shopee["Venda Total"].sum())
        
        
        meta_hoje = self.base_metas[(self.base_metas['MES']==today_month) & (self.base_metas['ANO']==today_year)]
        meta_vendas = meta_hoje['METAFAT'].sum()
        self.dashboard_ui.lab_home_main_hed_49.setText(locale.currency(meta_vendas, grouping=True))
        self.dashboard_ui.lab_home_main_hed_50.setText(locale.currency(venda_mes_total, grouping=True))

        self.dashboard_ui.lab_home_main_hed_25.setText(locale.currency(self.magalu_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_26.setText(locale.currency(self.via_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_27.setText(locale.currency(self.bww_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_28.setText(locale.currency(self.mcl_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_29.setText(locale.currency(self.amz_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_30.setText(locale.currency(self.cev_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_31.setText(locale.currency(self.crf_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_32.setText(locale.currency(self.zmm_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_33.setText(locale.currency(self.lry_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_34.setText(locale.currency(self.inter_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_35.setText(locale.currency(self.kbm_venda, grouping=True))
        self.dashboard_ui.lab_home_main_hed_36.setText(locale.currency(self.shopee_venda, grouping=True))

        self.dashboard_ui.lab_home_main_hed_25.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_26.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_27.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_28.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_29.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_30.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_31.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_32.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_33.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_34.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_35.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_36.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')



        self.dashboard_ui.lab_home_main_hed_63.setText("MC%: {:.2%}".format(self.magalu_mc))
        self.dashboard_ui.lab_home_main_hed_52.setText("MC%: {:.2%}".format(self.via_mc))
        self.dashboard_ui.lab_home_main_hed_56.setText("MC%: {:.2%}".format(self.bww_mc))
        self.dashboard_ui.lab_home_main_hed_53.setText("MC%: {:.2%}".format(self.mcl_mc))
        self.dashboard_ui.lab_home_main_hed_54.setText("MC%: {:.2%}".format(self.amz_mc))
        self.dashboard_ui.lab_home_main_hed_55.setText("MC%: {:.2%}".format(self.cev_mc))
        self.dashboard_ui.lab_home_main_hed_58.setText("MC%: {:.2%}".format(self.crf_mc))
        self.dashboard_ui.lab_home_main_hed_59.setText("MC%: {:.2%}".format(self.zmm_mc))
        self.dashboard_ui.lab_home_main_hed_57.setText("MC%: {:.2%}".format(self.lry_mc))
        self.dashboard_ui.lab_home_main_hed_60.setText("MC%: {:.2%}".format(self.inter_mc))
        self.dashboard_ui.lab_home_main_hed_61.setText("MC%: {:.2%}".format(self.kbm_mc))
        self.dashboard_ui.lab_home_main_hed_62.setText("MC%: {:.2%}".format(self.shopee_mc))

        self.dashboard_ui.lab_home_main_hed_63.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_52.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_56.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_53.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_54.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_55.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_58.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_59.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_57.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_60.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_61.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_62.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')

        

        realizado = (venda_mes_total/meta_vendas)*100
        self.dashboard_ui.progressBar_bug_6.setValue(realizado)



    #Verifica quais datas estão selecionadas e qual tipo de valor (vendas, faturamento) selecionado no dashboard
    def verificar(self):
        self.datefrom = self.dashboard_ui.dateEdit.date()
        self.datetill = self.dashboard_ui.dateEdit_2.date()
        self.text_box1 = self.dashboard_ui.comboBox_bug_5.currentText()
        self.text_box2 = self.dashboard_ui.comboBox_bug_6.currentText()



    #Seleciona de qual marketplace deve vir o valor
    def set_marketplace(self, marketplace):
        self.mktp = marketplace
    

    #Faz os cálculos e retorna os dados do dashboard individual por marketplace
    def organize_data(self):
        today = datetime.date.today()
        day = today.day
        month = today.month
        year = today.year
        Marketplace = self.mktp
        Data_from = self.date_de
        Data_until = self.date_ate
        #display(choosen_data['Total Value'].sum())
        self.sql_df['Data'] = pd.to_datetime(self.sql_df['Data'], format="%Y-%m-%d")
        if Marketplace == 17:
            self.cdata = self.sql_df[(self.sql_df['SalesChannel'].isin([17,23])) & (self.sql_df['Data']>=Data_from) & (self.sql_df['Data']<=Data_until)]
            self.actual_df = self.sql_df[(self.sql_df['SalesChannel'].isin([17,23])) & (self.sql_df['Mes']==month) & (self.sql_df['Ano']==year)]
            
        else:    
            self.cdata = self.sql_df[(self.sql_df['SalesChannel']==Marketplace) & (self.sql_df['Data']>=Data_from) & (self.sql_df['Data']<=Data_until)]
            self.actual_df = self.sql_df[(self.sql_df['SalesChannel']==Marketplace) & (self.sql_df['Mes']==month) & (self.sql_df['Ano']==year)]
        
        if Marketplace == 17:
            self.metas_mktp = [(self.base_metas['MES']==month) & (self.base_metas['ANO']==year) & (self.base_metas['CODVENDEDOR']==7430)]

        cod_marketplace = {13:4001,4:7719,6:7437,17:7430,12:1478,18:10368,8:4000,7:448,14:989,1:102,15:73,21:13}
        self.metas_mktp = self.base_metas[(self.base_metas['MES']==month) & (self.base_metas['ANO']==year) & (self.base_metas['CODVENDEDOR']==cod_marketplace[Marketplace])]
        meta_fat = self.metas_mktp['METAFAT'].sum()
        
        meta_vendas = meta_fat


        best_seller_sku_1 = ""
        best_seller_sku_2 = ""
        best_seller_sku_3 = ""
        best_seller_name_1 = ""
        best_seller_name_2 = ""
        best_seller_name_3 = ""
        best_seller_marca_1 = ""
        best_seller_marca_2 = ""
        best_seller_marca_3 = ""
        best_seller_uf_1 = ""
        best_seller_uf_2 = ""
        best_seller_uf_3 = ""
        
        
        
        try:
            best_seller_sku = (self.cdata.groupby("ID_SKU")["Quantity_SKU"].sum()).nlargest(3)
            best_seller_sku_1 = best_seller_sku.index[0]
            best_seller_sku_2 = best_seller_sku.index[1]
            best_seller_sku_3 = best_seller_sku.index[2]
            best_seller_name_1 = self.cdata[(self.cdata["ID_SKU"]==best_seller_sku_1)]["Produto"].drop_duplicates().to_string(index=False)
            best_seller_name_2 = self.cdata[(self.cdata["ID_SKU"]==best_seller_sku_2)]["Produto"].drop_duplicates().to_string(index=False)
            best_seller_name_3 = self.cdata[(self.cdata["ID_SKU"]==best_seller_sku_3)]["Produto"].drop_duplicates().to_string(index=False)
        except:
            pass
        try:
            best_seller_marca = (self.cdata.groupby("Marca")["Quantity_SKU"].sum()).nlargest(3)
            best_seller_marca_1 = best_seller_marca.index[0]
            best_seller_marca_2 = best_seller_marca.index[1]
            best_seller_marca_3 = best_seller_marca.index[2]
        except:
            pass

        try:
            best_seller_uf = (self.cdata.groupby("UF")["Quantity_SKU"].sum()).nlargest(3)
            best_seller_uf_1 = best_seller_uf.index[0]
            best_seller_uf_2 = best_seller_uf.index[1]
            best_seller_uf_3 = best_seller_uf.index[2]
        except:
            pass

        self.categories2 = []
        for i in reversed(range(self.set5.count())):
            self.set5.remove(i)

        
        try:
            self.sql_df['Creation Date'] =pd.to_datetime(self.sql_df['Creation Date'],format='%Y-%m-%d %H:%M:%S')
            att_datetime = self.sql_df['Creation Date'].max()
        except:
            att_datetime = "Wrong Date Format"
        
        month_value = self.actual_df['Venda Total'].sum()
        values_per_date = self.cdata.groupby(['Data', 'SalesChannel'])['Venda Total'].sum().reset_index()
        values_per_marketplace = values_per_date[values_per_date['SalesChannel']==Marketplace]
        values_per_marketplace['Venda Total'] = values_per_marketplace['Venda Total'].astype(float)
        value_list = list(values_per_marketplace['Venda Total'])
        self.set5.append(value_list)
        cdates = values_per_marketplace['Data'].dt.strftime('%d/%m/%Y')
        cdates = cdates.astype(str)
        valor_maximo = values_per_marketplace['Venda Total'].max()
        valor_minimo = values_per_marketplace['Venda Total'].min()
        value_total = self.cdata['Venda Total'].sum()

        margem = (self.cdata["MC"].sum())/(self.cdata["Venda Total"].sum())
        meta_total = self.base_metas[(self.base_metas['MES']==self.today_month) & (self.base_metas['ANO']==self.today_year)]
        selling_value = locale.currency(value_total, grouping=True)
        self.dashboard_ui.lab_home_main_hed_66.setText(selling_value)
        self.dashboard_ui.lab_home_main_hed_66.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_23.setText("MC%: {:.2%}".format(margem))
        self.dashboard_ui.lab_home_main_hed_14.setText(f"1° - SKU:{best_seller_sku_1}")
        self.dashboard_ui.lab_home_main_hed_74.setText(f"Produto:{best_seller_name_1}")
        self.dashboard_ui.lab_home_main_hed_75.setText(f"2° - SKU:{best_seller_sku_2}")
        self.dashboard_ui.lab_home_main_hed_73.setText(f"Produto:{best_seller_name_2}")
        self.dashboard_ui.lab_home_main_hed_15.setText(f"3° - SKU:{best_seller_sku_3}")
        self.dashboard_ui.lab_home_main_hed_77.setText(f"Produto:{best_seller_name_3}")
        self.dashboard_ui.lab_home_main_hed_17.setText(f"1° - {best_seller_marca_1}")
        self.dashboard_ui.lab_home_main_hed_72.setText(f"2° - {best_seller_marca_2}")
        self.dashboard_ui.lab_home_main_hed_71.setText(f"3° - {best_seller_marca_3}")
        self.dashboard_ui.lab_home_main_hed_20.setText(f"1° - {best_seller_uf_1}")
        self.dashboard_ui.lab_home_main_hed_21.setText(f"2° - {best_seller_uf_2}")
        self.dashboard_ui.lab_home_main_hed_76.setText(f"3° - {best_seller_uf_3}")
        self.dashboard_ui.lab_home_main_hed_78.setText(f"Atualizado por último: {att_datetime}")
        self.dashboard_ui.lab_home_main_hed_51.setText(f"Realizado: {locale.currency(month_value, grouping=True)}")
        self.dashboard_ui.lab_home_main_hed_69.setText(f"Meta: {locale.currency(meta_vendas, grouping=True)}")
        self.dashboard_ui.lab_home_main_hed_14.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_74.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_75.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_73.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_15.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_77.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_17.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_72.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_71.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_20.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_21.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_76.setStyleSheet('font: 600 10pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_51.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_69.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_23.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')
        self.dashboard_ui.lab_home_main_hed_78.setStyleSheet('font: 600 12pt "Bahnschrift SemiBold";color: rgb(240, 240, 240)')


        realizado = (month_value/meta_vendas)*100
        self.dashboard_ui.progressBar_bug_5.setValue(realizado)

        self.categories2 = cdates
        self.axisX2.clear()
        self.axisX2.append(self.categories2)
        self.axisX2.setRange(cdates.iloc[0], cdates.iloc[-1])

        self.axisY2.setRange(0,(int(np.ceil((int(((float(valor_maximo))+(float(valor_maximo)*0.10)))/1000))*1000)))




   


    #Importa as tabelas do banco necessárias para fazer o dashboard funcionar
    def import_tables(self):
        today = datetime.date.today()
        months_to_get = datetime.timedelta(32)
        months = today - months_to_get 
        query = f'SELECT `Data`,Ano,Mes,Dia,Hora,Minuto,Produto,MC,`Order`,UF,Marca,City,Quantity_SKU,ID_SKU,`SKU Total Price`, `Shipping Value`,`Creation Date`, SalesChannel FROM base_vendas WHERE `Data`>{months}'
        
        self.sql_df = pd.read_excel('dados/vendas.xlsx')
        self.sql_df['Venda Total'] = self.sql_df['SKU Total Price']+self.sql_df['Shipping Value']
        self.base_metas = pd.read_excel('dados/metas.xlsx')


    #Retorna a data selecionada no dashboard e formata para pegar o valor na tabela
    def getdate(self):
        self.datefrom =  self.dashboard_ui.dateEdit.date()
        self.datetill =  self.dashboard_ui.dateEdit_2.date()
        
        self.from_day = self.datefrom.day()
        self.from_month = self.datefrom.month()
        self.from_year = self.datefrom.year()
        self.date_de = (f"{self.from_year}-{self.from_month}-{self.from_day}")
        self.date_de = self.date_de.format("%Y/%m/%d")
        
        self.ate_day = self.datetill.day()
        self.ate_month = self.datetill.month()
        self.ate_year = self.datetill.year()
        self.date_ate = (f"{self.ate_year}-{self.ate_month}-{self.ate_day}")
        self.date_ate = self.date_ate.format("%Y/%m/%d")
        self.datas = pd.date_range(start=self.date_de, end=self.date_ate)


    #Função que conecta os botões à outras funções do programa
    def buttonPressed(self, buttonName):
        if buttonName=='dateEdit':
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
        elif buttonName=='dateEdit_2':
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
        elif buttonName=='dateEdit_3':
                Dashboard_func.dashboard_geral(self)
        elif buttonName=='dateEdit_4':
                Dashboard_func.dashboard_geral(self)
        else:

            for each in self.dashboard_ui.frame_bottom_west.findChildren(QFrame):
                each.setStyleSheet("background:rgb(0,0,0)")
            for each in self.dashboard_ui.frame_bottom_west_2.findChildren(QFrame):
                each.setStyleSheet("background:rgb(0,0,0)")

        if buttonName=='bn_mgl':
                self.dashboard_ui.frame_home.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,13)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                

        elif buttonName=='bn_via':
                self.dashboard_ui.frame_home_2.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,4)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                

        elif buttonName=='bn_bww':
                self.dashboard_ui.frame_cloud.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,6)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                

        elif buttonName=='bn_mcl':
                self.dashboard_ui.frame_bug.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,17)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_amz':
                self.dashboard_ui.frame_home_3.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,12)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_cev':
                self.dashboard_ui.frame_home_4.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,18)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_crf':
                self.dashboard_ui.frame_home_5.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,8)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_zmm':
                self.dashboard_ui.frame_home_6.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,7)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_lry':
                self.dashboard_ui.frame_android.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,14)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                
        elif buttonName=='bn_shopee':
                self.dashboard_ui.frame_home_7.setStyleSheet("background:rgb(170, 255, 255)") 
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,1)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
        elif buttonName=='bn_inter':
                self.dashboard_ui.frame_android_2.setStyleSheet("background:rgb(170, 255, 255)")
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,15)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
        elif buttonName=='bn_kbm':
                self.dashboard_ui.frame_android_3.setStyleSheet("background:rgb(170, 255, 255)")
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
                Dashboard_func.set_marketplace(self,21)
                Dashboard_func.getdate(self)
                Dashboard_func.organize_data(self)
                
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_home)
        elif buttonName=='bn_mgl_2':
                self.dashboard_ui.stackedWidget.setCurrentWidget(self.dashboard_ui.page_about_android)
                Dashboard_func.dashboard_geral(self)
        
    
    

