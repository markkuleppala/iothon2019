# iothon2019
IoThon 2019 project

The project demonstrates proof of concept for creating a charging station out of Nokia LuxTurrim 5G light pole. The pole uses led lights instead of energy consuming traditional lights thus freeing electricity charging capacity to other use cases. Due to central location of the light poles, these could be harnessed into multiple use cases such as electronic scooter or bike charging stations or car heating sockets.

The proof of concept initializes connection with two Raspberry Pies that act as a client (LuxTurrim 5G) and server (cloud). Client has a RFID (MFRC522) reader implemented that recognizes the tags inserted and communicates the data to server that checks for matching credentials. Based on the response client either rings the buzzer (credintials ok, charging started) or does nothing in case of missing credentials. The server logs usage statistics to payment purposes.

RPi-RFD library (https://github.com/paguz/RPi-RFID) is used to support MFRC522 reader.
