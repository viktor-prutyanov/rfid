#include <SPI.h>
#include "PN532_SPI.h"
#include "PN532.h"
#include "NfcAdapter.h"

PN532_SPI interface(SPI, 10); // create a PN532 SPI interface with the SPI CS terminal located at digital pin 10
NfcAdapter nfc = NfcAdapter(interface); // create an NFC adapter object
const int ledPinGreen = 2;      // the number of the LED pin

String uid_str;

void setup(void) {
    nfc.begin(); // begin NFC communication
    pinMode(ledPinGreen, OUTPUT);
    digitalWrite(ledPinGreen, LOW);
    Serial.begin(115200); // begin serial communication
}

void loop(void) {
    if (nfc.tagPresent()) { // Do an NFC scan to see if an NFC tag is present
        NfcTag tag = nfc.read(); // read the NFC tag into an object, nfc.read() returns an NfcTag object.
        uid_str = tag.getUidString(); // prints the NFC tags type, UID, and NDEF message (if available)
        Serial.println(uid_str);
        digitalWrite(ledPinGreen, HIGH);
        delay(1000);

    } else {
      digitalWrite(ledPinGreen, LOW);
    }
}
