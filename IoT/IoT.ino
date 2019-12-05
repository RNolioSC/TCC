#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

#define RELE 7

int i = 0;
void setup() 
{
  Serial.begin(57600);   // Inicia a serial
  SPI.begin();      // Inicia  SPI bus
  mfrc522.PCD_Init();   // Inicia MFRC522
  pinMode(RELE, OUTPUT); // Configura o rele
}
 
void loop() 
{
  ler_cartao();
} 


void ler_cartao(){
  if ( ! mfrc522.PICC_IsNewCardPresent()) // procura por novos cartoes
  {
    return;
  }
 
  if ( ! mfrc522.PICC_ReadCardSerial())  // seleciona um cartao
  {
    return;
  }
 
  Serial.write(0x12); // delimitador inicial
  for (int i = 0; i < 4; i++) {
         if (mfrc522.uid.uidByte[i]<16) Serial.print("0");
         Serial.print(mfrc522.uid.uidByte[i], HEX);  // lendo dois bytes por vez e adicionando-os ao pacote
  }
  
   digitalWrite(RELE,HIGH);
   delay(2000);
   digitalWrite(RELE,LOW);

  Serial.println();
}
