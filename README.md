# Interactive LoPy wildlife-camera
A wildlife-camera created for the IoT course (INF-3910-3) by:
- Sverre Coucheron (sverre.coucheron@gmail.com)
- Martin Stensen (martin.stensen92@gmail.com)
- Vebjørn Haugland (vha044@post.uit.no)

The camera sends information such as how much battery is left, if the device is tilted (has fallen down) and if it is covered in snow. It uses the LoRaWAN to send data to telenor-connexion (https://startiot.mic.telenorconnexion.com/login)

For more in-depth information, read the report.



## Information about the files
#### Sensors.py
Contains functions to use all the sensors on the wildcamera.

#### Main.py
Connects to LoRaWAN and acutally sends/stores data on the SD-card and telenor-connexion.

#### Boot.py
First file which is ran by the LoPy, boots everything and initializes the SD-card for use. Creates a folder ('/sd/') in the filesystem where pictures are to be saved.

#### Report.pdf
The written report from the course. Can be used to look up problems/questions with the code.

## Known problems
#### Camera
The camera itself is not working. Uncertain why, bugs when trying to send, write and receive data simultaneously (?). Borrowed a library for it which is not complete.  
- **Camera** : https://www.sparkfun.com/products/11610
- **User manual** : http://www.linksprite.com/upload/file/1291522825.pdf

There are two libraries now:
 - **safety_LSY201.py** -> This is the borrowed library as it was when it was received.
 - **LSY201.py** -> Removed things from the borrowed library to try stuff. Does not work either.

#### PIR-sensor
Has to 'boot' for ~1 minute the first time. Because of this expect a downtime for 30-60 minutes before it actually works.

#### Battery gauge
Uncertain if it works properly. Has not been tested 100%, might be buggy.

**Solution**: Use a battery gauge?
