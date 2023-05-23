// Código A_TX (Móvil - Cohete)

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <RF24.h>

RF24 radio(8, 10); // CE, CSN
const byte address[6] = "00001";

Adafruit_BMP280 bmp;

float TEMPERATURA, ALTITUD;
float PRESION, P0;

const int MPU_addr=0x68;  // Direccion del sensor MPU6050 en el bus I2C
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

float datos[7] = {0}; // Arreglo para almacenar los datos

void setup()
{
  Serial.begin(9600);  // Inicializar la comunicación serial a 9600 baudios
  Wire.begin();        // Inicializar el bus I2C
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);     // PWR_MGMT_1 register
  Wire.write(0);        // Setear en 0 para activar el sensor
  Wire.endTransmission(true);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setChannel(110);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_LOW);

  if (!bmp.begin()){
    Serial.println("BMP280 no encontrado !");
    while (1);
  }
  P0 = bmp.readPressure()/100;
}

void loop()
{
  Wire.beginTransmission(MPU_addr); // Iniciar la comunicación con el MPU6050
  Wire.write(0x3B);                 // Direccion del registro donde comienza la lectura
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true); // Leer 14 bytes de datos

  AcX = Wire.read()<<8 | Wire.read();   // Leer los valores del acelerometro
  AcY = Wire.read()<<8 | Wire.read();
  AcZ = Wire.read()<<8 | Wire.read();
  Tmp = Wire.read()<<8 | Wire.read();   // Leer el valor de la temperatura
  GyX = Wire.read()<<8 | Wire.read();   // Leer los valores del giroscopio
  GyY = Wire.read()<<8 | Wire.read();
  GyZ = Wire.read()<<8 | Wire.read();

  ALTITUD = bmp.readAltitude(P0);

  datos[0] = AcX;
  datos[1] = AcY;
  datos[2] = AcZ;
  datos[3] = GyX;
  datos[4] = GyY;
  datos[5] = GyZ;
  datos[6] = ALTITUD;

  radio.write(datos, sizeof(datos));

  delay(10); // Esperar 50 milisegundos antes de tomar otra muestra
}