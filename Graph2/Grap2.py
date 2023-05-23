#  Se importan todas las librerías necesarias
import sys    
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap

class SerialPlot(QWidget):   ## Se declara una clase para el manejo del Widget

    def __init__(self, parent = None):              ### Función para configurar la ventana
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal 
        self.setWindowTitle("Datos del cohete DELTA")
        self.setWindowState(Qt.WindowMaximized)    ### Utilizar la pantalla completa
        self.setGeometry(0, 0, 800, 600)
        image = QPixmap("LOGO_UMNG.png")

        # Configuración del gráfico de la aceleración 
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 50, 600, 200)
        self.graphWidget.setBackground('black')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', '<span style="color: white; font-size: 18px;">Magnitud</span>')
        self.graphWidget.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget.setLabel('top', '<span style="color: white; font-size: 18px;">Aceleración</span>')
        self.graphWidget.getAxis('left').setStyle(tickFont=QFont('Trebuchet MS', 12))
        self.graphWidget.getAxis('bottom').setStyle(tickFont=QFont('Trebuchet MS', 12))
        
         # Configuración del gráfico del giroscopio 
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(50, 300, 600, 200)
        self.graphWidget2.setBackground('black')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', '<span style="color: white; font-size: 18px;">Magnitud</span>')
        self.graphWidget2.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo (s)</span>')
        self.graphWidget2.setLabel('top', '<span style="color: white; font-size: 18px;">Giroscopio</span>')
        self.graphWidget2.getAxis('left').setStyle(tickFont=QFont('Trebuchet MS', 12))
        self.graphWidget2.getAxis('bottom').setStyle(tickFont=QFont('Trebuchet MS', 12))
        
        # Configuración del gráfico de la Altura 
        self.graphWidget3 = pg.PlotWidget(self)
        self.graphWidget3.setGeometry(50, 550, 600, 200)
        self.graphWidget3.setBackground('black')
        self.graphWidget3.showGrid(x=True, y=True)

        self.graphWidget3.setLabel('left', '<span style="color: white; font-size: 18px;">Altitud (metros)</span>')
        self.graphWidget3.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo</span>')
        self.graphWidget3.setLabel('top', '<span style="color: white; font-size: 18px;">Altura vs Tiempo</span>')
        self.graphWidget3.getAxis('left').setStyle(tickFont=QFont('Futura', 12))
        self.graphWidget3.getAxis('bottom').setStyle(tickFont=QFont('Futura', 12))
        
       # Crear etiquetas para la fecha y la hora
        self.pos_0_0 = QLabel(self)
        self.pos_0_1 = QLabel(self)
        self.pos_0_2 = QLabel(self)
        self.pos_2_0 = QLabel(self)
        self.pos_2_1 = QLabel(self)
        self.pos_2_2 = QLabel(self)
        
        # Crear etiqueta para la imagen
        pixmap = QPixmap("/escritorio/TEL.jpg")
        self.pos_0_2.setPixmap(pixmap)
        
        # Configuración de la matriz de layouts
        layout_matrix = QGridLayout()
        layout_matrix.addWidget(self.pos_0_0, 0, 0)  
        layout_matrix.addWidget(self.pos_0_1, 0, 1)  
        layout_matrix.addWidget(self.pos_2_0, 2, 0)  
        layout_matrix.addWidget(self.pos_2_1, 2, 1)  
        layout_matrix.addWidget(self.pos_2_2, 2, 2)  
        self.pos_0_2.setPixmap(image)

        # Ajustar posiciones de las gráficas
        layout_matrix.addWidget(self.graphWidget, 1, 0)  
        layout_matrix.addWidget(self.graphWidget2, 1, 1)  
        layout_matrix.addWidget(self.graphWidget3, 1, 2)  
        layout_matrix.addWidget(self.pos_0_2, 0, 2)
        
        self.pos_0_0.setText("Universidad Militar Nueva Granada" + " \nPrograma de ingeniería en Telecomunicaciones")
        self.pos_0_1.setText("Proyecto de telemetría"+ " Cohete: RocketDelta")
        self.pos_2_1.setText("Temperatura: "+"\nVelocidad: ")
        self.pos_2_2.setText("Altura: ")
        
        self.pos_0_0.setStyleSheet("font-size: 20px; font-weight: bold; font-family: Trebuchet MS;")
        self.pos_2_0.setStyleSheet("font-size: 20px; font-weight: normal; font-family: Trebuchet MS;")
        self.pos_0_1.setStyleSheet("font-size: 20px; font-weight: normal; font-family: Trebuchet MS;")
        self.pos_2_1.setStyleSheet("font-size: 20px; font-weight: normal; font-family: Trebuchet MS;")
        self.pos_0_2.setStyleSheet("font-size: 20px; font-weight: normal; font-family: Trebuchet MS;")
        self.pos_2_2.setStyleSheet("font-size: 20px; font-weight: normal; font-family: Trebuchet MS;")
        
        """self.pos_0_0.setGeometry(50, 50, 100, 200)
        self.pos_2_0.setGeometry(50, 50, 100, 200)
        
        self.pos_0_1.setGeometry(50, 300, 100, 200)
        self.pos_2_1.setGeometry(50, 300, 100, 200)
        
        self.pos_0_2.setGeometry(50, 550, 100, 200)
        self.pos_2_2.setGeometry(50, 550, 100, 200)"""

        # Configuración del diseño principal
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_matrix)
        self.setLayout(layout_main)
        # Crear un temporizador para actualizar la hora cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)
        
    def update_datetime(self):
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.pos_2_0.setText("Fecha: " + date_str +" Hora: " + time_str)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    ex.update_datetime()
    sys.exit(app.exec_())
    

