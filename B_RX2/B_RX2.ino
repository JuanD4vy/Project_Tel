// Código B_RX (Estación Base)

#include <SPI.h>
#include <RF24.h>

RF24 radio(8, 53); // CE, CSN
const byte address[6] = "00001";

float datos[7] = {0}; // Arreglo para almacenar los datos

void setup()
{
  delay(1000);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setChannel(110);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();
  // Limpia el buffer del puerto serie
  Serial.flush();
}

void loop()
{
  if (radio.available())
  {
    radio.read(datos, sizeof(datos));

    for (int i = 0; i < sizeof(datos) / sizeof(datos[0]); i++)
    {
      Serial.print(datos[i]);
      if (i < sizeof(datos) / sizeof(datos[0]) - 1)
      {
        Serial.print(",");
      }
    }

    Serial.println(); // Saltar a la siguiente línea después de imprimir todos los datos
  }
  delay(10);
}