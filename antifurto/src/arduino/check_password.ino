#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

const byte PASSWD_LEN = 5;
char passwd[PASSWD_LEN] = "1234";
char data[PASSWD_LEN];

int counter = 0;

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte pinRows[ROWS] = {9, 8, 7, 6};
byte pinCols[COLS] = {5, 4, 3, 2};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), pinRows, pinCols, ROWS, COLS);

void setup() {
  Serial.begin(9600);
}


void loop() {
  char customKey = customKeypad.getKey();
    
  if (customKey) {  
    data[counter] = customKey;
    counter++;

    if (counter == PASSWD_LEN - 1) {
      data[counter] = '\0';
      
      if (strcmp(data, passwd))
        Serial.print("y");    
    
      counter = 0;
    }//counter
  }//customkey

}
