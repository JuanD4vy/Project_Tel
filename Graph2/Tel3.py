#  Se importan todas las librerías necesarias
import sys    
import csv
import serial
import time
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg

class SerialPlot(QWidget):   ## Se declara una clase para el manejo del Widget

    def __init__(self, parent = None):              ### Función para configurar la ventana
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal 
        self.setWindowTitle("Proyecto de telemetría")
        self.setWindowState(Qt.WindowMaximized)    ### Utilizar la pantalla completa
        self.setGeometry(0, 0, 800, 600)

        # Configuración del gráfico de la aceleración 
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 50, 600, 200)
        self.graphWidget.setBackground('black')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', '<span style="color: white; font-size: 18px;">Magnitud</span>')
        self.graphWidget.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo</span>')
        self.graphWidget.setLabel('top', '<span style="color: white; font-size: 18px;">Aceleración</span>')
        #self.graphWidget.setXRange(0, 30)
        
         # Configuración del gráfico del giroscopio 
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(50, 300, 600, 200)
        self.graphWidget2.setBackground('black')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', '<span style="color: white; font-size: 18px;">Magnitud</span>')
        self.graphWidget2.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo</span>')
        self.graphWidget2.setLabel('top', '<span style="color: white; font-size: 18px;">Giroscopio</span>')
        #self.graphWidget2.setXRange(0, 30)
        
        # Configuración del gráfico de la Altura 
        self.graphWidget3 = pg.PlotWidget(self)
        self.graphWidget3.setGeometry(50, 550, 600, 200)
        self.graphWidget3.setBackground('black')
        self.graphWidget3.showGrid(x=True, y=True)
        #self.graphWidget3.setXRange(0, 30)  # limite de Tiempo
        self.graphWidget3.setYRange(0, 50)  # Limite de altura

        self.graphWidget3.setLabel('left', '<span style="color: white; font-size: 18px;">Altitud (metros)</span>')
        self.graphWidget3.setLabel('bottom', '<span style="color: white; font-size: 18px;">Tiempo</span>')
        self.graphWidget3.setLabel('top', '<span style="color: white; font-size: 18px;">Altura vs Tiempo</span>')
       
        
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
        
        # Crear etiquetas para la fecha y la hora
        self.pos_0_0 = QLabel(self)
        self.pos_0_1 = QLabel(self)
        self.pos_0_2 = QLabel(self)
        self.pos_2_0 = QLabel(self)
        self.pos_2_1 = QLabel(self)
        self.pos_2_2 = QLabel(self)

        # Configuración de la matriz de layouts
        layout_matrix = QGridLayout()
        layout_matrix.addWidget(self.pos_0_0, 0, 0)  
        layout_matrix.addWidget(self.pos_0_1, 0, 1)  
        layout_matrix.addWidget(self.pos_2_0, 2, 0)  
        layout_matrix.addWidget(self.pos_2_1, 2, 1)  
        layout_matrix.addWidget(self.pos_2_2, 2, 2)  

        # Ajustar posiciones de las gráficas
        layout_matrix.addWidget(self.graphWidget, 1, 0)  
        layout_matrix.addWidget(self.graphWidget2, 1, 1)  
        layout_matrix.addWidget(self.graphWidget3, 1, 2)  

        # Configuración del diseño principal
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_matrix)
        self.setLayout(layout_main)
        
        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)                #####    Número de muestras por segundo

        # Llamar a la función update_datetime() para actualizar la hora
        self.update_datetime()
        
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
        ##self.x_data[:-1] = self.x_data[1:]
        ##self.x_data[-1] = self.x_data[-2] + 1
        # Obtener el tiempo actual en segundos
        current_time = time.time()

        # Añadir los nuevos valores a los datos del tiempo
        #self.x_data[:-1] = self.x_data[1:]
        #self.x_data[-1] = current_time

        # Crear valores para el tiempo en segundos
        time_range = 30  # Escala de tiempo en segundos
        time_step = time_range / len(self.x_data)
        self.x_data = np.arange(0, time_range, time_step)

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
        #with open('datos.csv', 'a', newline='') as archivo_csv:
            #escritor_csv = csv.writer(archivo_csv)
            #escritor_csv.writerow([values[0], values[1], values[2], values[3], values[4], values[5], values[6]])
    
        # Guardar los datos en un archivo CSV
        #data = list(zip(self.x_data, self.y_data_1, self.y_data_2, self.y_data_3, self.y_data_4, self.y_data_5, self.y_data_6, self.y_data_7))
        #with open('datos.csv', 'w', newline='') as csvfile:
            #writer = csv.writer(csvfile)
           # writer.writerow(['T', 'AceX', 'AceY', 'AceZ', 'GirX', 'GirY', 'GirZ', 'H'])
            #writer.writerows(data)
    
    def update_datetime(self):
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.pos_0_0.setText("Universidad Militar Nueva Granada" + " \nPrograma de ingeniería en Telecomunicaciones")
        self.pos_0_1.setText("Proyecto de telemetría"+ " Cohete: RocketDelta")
        self.pos_2_0.setText("Fecha: " + date_str +" Hora: " + time_str)
        self.pos_2_1.setText("Temperatura: "+"\nVelocidad: ")
        self.pos_2_2.setText("Altura: ")
        
        self.pos_0_0.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        self.pos_2_0.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        self.pos_0_1.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        self.pos_2_1.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        self.pos_0_2.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        self.pos_2_2.setStyleSheet("font-size: 20px; font-weight: normal; font-style: trebuchet")
        
        self.pos_0_0.setGeometry(50, 50, 100, 200)
        self.pos_2_0.setGeometry(50, 50, 100, 200)
        
        self.pos_0_1.setGeometry(50, 300, 100, 200)
        self.pos_2_1.setGeometry(50, 300, 100, 200)
        
        self.pos_0_2.setGeometry(50, 550, 100, 200)
        self.pos_2_2.setGeometry(50, 550, 100, 200)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    ex.update_datetime()
    sys.exit(app.exec_()) 