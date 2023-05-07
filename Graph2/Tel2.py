#  Se importan todas las librerías necesarias
import sys    
import csv
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg

class SerialPlot(QWidget):   ## Se declara una clase para el manejo del Widget

    def __init__(self, parent = None):              ### Función para configurar la ventana
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal 
        self.setWindowTitle("Datos del cohete")
        self.setGeometry(0, 0, 800, 600)

        # Configuración del gráfico de la aceleración 
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 50, 600, 200)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'Magnitud')
        self.graphWidget.setLabel('bottom', 'Muestras')
        
         # Configuración del gráfico del giroscopio 
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(50, 300, 600, 200)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', 'Magnitud')
        self.graphWidget2.setLabel('bottom', 'Muestras')
        
        # Configuración del gráfico de la Altura 
        self.graphWidget3 = pg.PlotWidget(self)
        self.graphWidget3.setGeometry(50, 550, 600, 200)
        self.graphWidget3.setBackground('w')
        self.graphWidget3.showGrid(x=True, y=True)
        self.graphWidget3.setLabel('left', 'Altitud')
        self.graphWidget3.setLabel('bottom', 'Muestras')
        
        # Configuración del puerto serial
        self.ser = serial.Serial('COM4', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 100  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)    ## Tiempo
        self.y_data_1 = np.zeros(num_points)  # AcX
        self.y_data_2 = np.zeros(num_points)  # AcY
        self.y_data_3 = np.zeros(num_points)  # AcZ
        self.y_data_4 = np.zeros(num_points)  # GyX
        self.y_data_5 = np.zeros(num_points)  # GyY
        self.y_data_6 = np.zeros(num_points)  # GyZ
        self.y_data_7 = np.zeros(num_points)  # Altura

        # Crear las líneas para cada valor a graficar
        self.curve1 = self.graphWidget.plot(self.x_data, self.y_data_1, pen='r', name='AcX')
        self.curve2 = self.graphWidget.plot(self.x_data, self.y_data_2, pen='g', name='AcY')
        self.curve3 = self.graphWidget.plot(self.x_data, self.y_data_3, pen='b', name='AcZ')
        # Crear las líneas para cada valor a graficar
        self.curve4 = self.graphWidget2.plot(self.x_data, self.y_data_4, pen='r', name='GyX')
        self.curve5 = self.graphWidget2.plot(self.x_data, self.y_data_5, pen='g', name='GyY')
        self.curve6 = self.graphWidget2.plot(self.x_data, self.y_data_6, pen='b', name='GyZ')
        # Crear las líneas para cada valor a graficar
        self.curve7 = self.graphWidget3.plot(self.x_data, self.y_data_7, pen='orange', name='Altura')
        
        layout = QHBoxLayout()
        layout.addWidget(self.graphWidget)   ### addWidget para adicionar paneles independientes
        layout.addWidget(self.graphWidget2)
        layout.addWidget(self.graphWidget3)
        self.setLayout(layout)
        self.showFullScreen()    ### Utilizar la pantalla completa

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)    

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Añadir los nuevos valores a los datos de la aceleración
        self.y_data_1[:-1] = self.y_data_1[1:]
        self.y_data_1[-1] = float(values[0])
        self.y_data_2[:-1] = self.y_data_2[1:]
        self.y_data_2[-1] = float(values[1])
        self.y_data_3[:-1] = self.y_data_3[1:]
        self.y_data_3[-1] = float(values[2])
        # Añadir los nuevos valores a los datos del giroscopio
        self.y_data_4[:-1] = self.y_data_4[1:]
        self.y_data_4[-1] = float(values[3])
        self.y_data_5[:-1] = self.y_data_5[1:]
        self.y_data_5[-1] = float(values[4])
        self.y_data_6[:-1] = self.y_data_6[1:]
        self.y_data_6[-1] = float(values[5])
        # Añadir los nuevos valores a los datos de la altura
        self.y_data_7[:-1] = self.y_data_7[1:]
        self.y_data_7[-1] = float(values[6])
        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]
        self.x_data[-1] = self.x_data[-2] + 1

        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Aceleración)
        self.curve1.setData(self.x_data, self.y_data_1)
        self.curve2.setData(self.x_data, self.y_data_2)
        self.curve3.setData(self.x_data, self.y_data_3)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Giroscopio)
        self.curve4.setData(self.x_data, self.y_data_4)
        self.curve5.setData(self.x_data, self.y_data_5)
        self.curve6.setData(self.x_data, self.y_data_6)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Altura)
        self.curve7.setData(self.x_data, self.y_data_7)
        # Guardar los nuevos datos en el archivo CSV
        with open('datos.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([values[0], values[1], values[2], values[3], values[4], values[5], values[6]])

    def resizeEvent1(self, event):
        #Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 50, self.width() - 100, self.height() - 100)
    def resizeEvent2(self, event):
        #Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 300, self.width() - 100, self.height() - 100)
    def resizeEvent3(self, event):
        #Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 550, self.width() - 100, self.height() - 100)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    sys.exit(app.exec_())
    

