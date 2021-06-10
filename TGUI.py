from PySide2.QtCore import QCoreApplication, Qt, QModelIndex, QSortFilterProxyModel, Slot
from PySide2.QtWidgets import QMainWindow, QGroupBox, QLineEdit, QPushButton, QTableView, QWidget, QGridLayout, \
    QApplication, QAbstractItemView
from PySide2.QtGui import QIcon, QPainter, QColor
from MinimasiEnergiGibbs1 import SyngasComposition_Calculations
from tableModelT import TableModel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.resize(1366, 768)
        self.setWindowTitle("Thermodynamics Equilibrium - Universitas Riau")

        self.uiInit()
        self.tableInit()
        self.matplotlibInit()

    def uiInit(self):
        appIcon = QIcon("universitasriau.png")
        self.setWindowIcon(appIcon)

        # Frame in MainWindows

        self.frame01 = QGroupBox("Temperature", self)
        self.frame01.setGeometry(15, 22, 92, 53)
        self.frame01.setAlignment(Qt.AlignCenter)

        self.frame02 = QGroupBox("EquivalenceRatio", self)
        self.frame02.setGeometry(117, 22, 92, 53)
        self.frame02.setAlignment(Qt.AlignCenter)

        self.frame03 = QGroupBox("wCarbon", self)
        self.frame03.setGeometry(229, 22, 92, 53)
        self.frame03.setAlignment(Qt.AlignCenter)

        self.frame04 = QGroupBox("wHydrogen", self)
        self.frame04.setGeometry(331, 22, 92, 53)
        self.frame04.setAlignment(Qt.AlignCenter)

        self.frame05 = QGroupBox("wOxygen", self)
        self.frame05.setGeometry(432, 22, 92, 53)
        self.frame05.setAlignment(Qt.AlignCenter)

        self.frame06 = QGroupBox("wNitrogen", self)
        self.frame06.setGeometry(534, 22, 92, 53)
        self.frame06.setAlignment(Qt.AlignCenter)

        self.frame07 = QGroupBox("Ultimate Analysis", self)
        self.frame07.setGeometry(219, 10, 418, 73)
        self.frame07.setAlignment(Qt.AlignCenter)

        self.frame08 = QGroupBox("GasificationAgent", self)
        self.frame08.setGeometry(646, 22, 92, 53)
        self.frame08.setAlignment(Qt.AlignCenter)

        self.frame09 = QGroupBox("Basis", self)
        self.frame09.setGeometry(748, 22, 92, 53)
        self.frame09.setAlignment(Qt.AlignCenter)

        self.frame10 = QGroupBox("Syngas Composition", self)
        self.frame10.setGeometry(15, 93, 663, 600)
        self.frame10.setAlignment(Qt.AlignCenter)

        self.frame11 = QGroupBox("Graph of Syngas Composition versus T/ER", self)
        self.frame11.setGeometry(688, 93, 663, 600)
        self.frame11.setAlignment(Qt.AlignCenter)

        # Temperature
        self.Temperature = QLineEdit(self)
        self.Temperature.setGeometry(25, 37, 72, 30)
        self.Temperature.setAlignment(Qt.AlignCenter)
        self.Temperature.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")

        # Equivalence Ratio
        self.Equivalence_Ratio = QLineEdit(self)
        self.Equivalence_Ratio.setGeometry(127, 37, 72, 30)
        self.Equivalence_Ratio.setAlignment(Qt.AlignCenter)
        self.Equivalence_Ratio.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")

        # Ultimate Analysis
        self.wCarbon = QLineEdit(self)
        self.wCarbon.setGeometry(239, 37, 72, 30)
        self.wCarbon.setAlignment(Qt.AlignCenter)
        self.wCarbon.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")
        self.wHydrogen = QLineEdit(self)
        self.wHydrogen.setGeometry(341, 37, 72, 30)
        self.wHydrogen.setAlignment(Qt.AlignCenter)
        self.wHydrogen.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")
        self.wOxygen = QLineEdit(self)
        self.wOxygen.setGeometry(442, 37, 72, 30)
        self.wOxygen.setAlignment(Qt.AlignCenter)
        self.wOxygen.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")
        self.wNitrogen = QLineEdit(self)
        self.wNitrogen.setGeometry(544, 37, 72, 30)
        self.wNitrogen.setAlignment(Qt.AlignCenter)
        self.wNitrogen.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")

        # Gasification Agent
        self.Gasification_Agent = QLineEdit(self)
        self.Gasification_Agent.setGeometry(656, 37, 72, 30)
        self.Gasification_Agent.setAlignment(Qt.AlignCenter)
        self.Gasification_Agent.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")

        # Basis
        self.Basis = QLineEdit(self)
        self.Basis.setGeometry(758, 37, 72, 30)
        self.Basis.setAlignment(Qt.AlignCenter)
        self.Basis.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")

        self.initData()

        # Process Button for Show Value
        self.button1 = QPushButton("Process", self)
        self.button1.move(850, 37)
        self.button1.setStyleSheet("background-color: lightcyan; border: 1.6px solid red")
        self.button1.clicked.connect(self.process_data)

    def initData(self):
        self.Temperature.setText("675")
        self.Equivalence_Ratio.setText('0.3')
        self.wHydrogen.setText('0.058')
        self.wCarbon.setText('0.424')
        self.wOxygen.setText('0.482')
        self.wNitrogen.setText('0.036')
        self.Gasification_Agent.setText('3.7619')
        self.Basis.setText('12000')

    def tableInit(self):
        self.model = TableModel()
        proxyModel = QSortFilterProxyModel(self)
        proxyModel.setSourceModel(self.model)
        proxyModel.setDynamicSortFilter(True)

        self.table = QTableView(self)
        self.table.setModel(proxyModel)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setGeometry(25, 110, 640, 570)
        #self.repaint()

    def matplotlibInit(self):
        self.w_Canvas = QWidget(self)
        self.w_Canvas.setGeometry(690, 150, 655, 473)
        self.l_Canvas = QGridLayout(self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.l_Canvas.addWidget(self.canvas)
        self.w_Canvas.setLayout(self.l_Canvas)

        self.xdata = []
        self.ydata = []
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        self.show()

    #def update_plot(self):
        # Drop off the first y element, append a new one.
        
       

    @Slot()
    def process_data(self):
        T = float(self.Temperature.text())
        Alfa = float(self.Equivalence_Ratio.text())
        wC = float(self.wCarbon.text())
        wH = float(self.wHydrogen.text())
        wO = float(self.wOxygen.text())
        wN = float(self.wNitrogen.text()) 
        Beta = float(self.Gasification_Agent.text())
        W = float(self.Basis.text())
        hasil = SyngasComposition_Calculations(T, Alfa, wC, wH, wO, wN, Beta, W)
        print(hasil)
        dictHasil = {"Temperature": T, "yCH4": float(hasil[0]), "yCO": float(hasil[1]), "yCO2": float(hasil[2]), "yH2": float(hasil[3]),
                     "yN2": float(hasil[4]), "yH2O": float(hasil[5])}
        self.model.insertRows(0)
        ix = self.model.index(0, 0, QModelIndex())
        self.model.setData(ix, dictHasil["Temperature"], Qt.EditRole)
        self.table.resizeRowToContents(ix.row())

        ix = self.model.index(0, 1, QModelIndex())
        self.model.setData(ix, dictHasil["yCH4"], Qt.EditRole)

        ix = self.model.index(0, 2, QModelIndex())
        self.model.setData(ix, dictHasil["yCO"], Qt.EditRole)
        self.table.resizeRowToContents(ix.row())

        ix = self.model.index(0, 3, QModelIndex())
        self.model.setData(ix, dictHasil["yCO2"], Qt.EditRole)

        ix = self.model.index(0, 4, QModelIndex())
        self.model.setData(ix, dictHasil["yH2"], Qt.EditRole)

        ix = self.model.index(0, 5, QModelIndex())
        self.model.setData(ix, dictHasil["yN2"], Qt.EditRole)

        ix = self.model.index(0, 6, QModelIndex())
        self.model.setData(ix, dictHasil["yH2O"], Qt.EditRole)
        print(dictHasil)
        print(self.model.datas)
        print(len(self.model.datas))
        print(self.model.datas[0]["Temperature"])
        print(self.model.datas[0]["yCH4"])
        self.plotDataBaseOnDatas(self.model.datas)

        
    def plotDataBaseOnDatas(self, datas):
        self.canvas.axes.cla()  # Clear the canvas.
        jumlahData = len(datas)
        x_suhu = []
        yCH4_comp = []
        yCO_comp = []
        yCO2_comp = []
        yH2_comp = []
        yN2_comp = []
        yH2O_comp = []

        for data in datas:
            x_suhu.append(data["Temperature"])
            yCH4_comp.append(data["yCH4"])
            yCO_comp.append(data["yCO"])
            yCO2_comp.append(data["yCO2"])
            yH2_comp.append(data["yH2"])
            yN2_comp.append(data["yN2"])
            yH2O_comp.append(data["yH2O"])

            # for yCH4
            self.canvas.axes.plot(x_suhu, yCH4_comp, 'peru', marker='s', linestyle=':')

            # for yCO
            self.canvas.axes.plot(x_suhu, yCO_comp, 'fuchsia', marker='o', linestyle=':')

            # for yCO2
            self.canvas.axes.plot(x_suhu, yCO2_comp, 'darkgreen', marker='d', linestyle=':')

            # for yH2
            self.canvas.axes.plot(x_suhu, yH2_comp, 'mediumblue', marker='^', linestyle=':')

            # for yN2
            #self.canvas.axes.plot(x_suhu, yN2_comp, 'teal', marker='*', linestyle=':')

            # for yH2O
            self.canvas.axes.plot(x_suhu, yH2O_comp, 'crimson', marker='x', linestyle=':')
        
        self.canvas.axes.set_xlabel('Suhu Gasifikasi (K)')
        self.canvas.axes.set_ylabel('Komposisi Syngas (%)')
        self.canvas.axes.legend(['CH4', 'CO', 'CO2', 'H2', 'H2O'])
        #self.canvas.axes.set_title('Pengaruh Suhu pada Rasio Ekuivalen 0,3')
        self.canvas.axes.set_facecolor('honeydew')
        self.canvas.figure.set_facecolor('skyblue')
        self.canvas.figure.savefig("TempVSSyngasComp")
        # Trigger the canvas to update and redraw.
        self.canvas.draw()



def main():
    import sys
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainW = Main()
    mainW.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
