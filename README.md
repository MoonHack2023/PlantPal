# PlantPal

PlantPal is a  compact and innovative plant sensor - the ultimate solution for optimizing growing conditions for any type of fruit or plant.
Using the 4 sensors below, 
- Air temperature and humidity sensor (Si7021)
- Spectral light (AS7262)
- Gas Sensor (CCS811)
- Air velocity sensor (D6F-V03A1)

PlantPal effectively measures the surroundings of any plant in any environment.
## Running the web app with sensors

First clear the database with `./clear.sh` or `python3 manage.py clear`

Inside PlantPalApp run following

```
python3 manage.py runserver
```

Open 2 Raspberry Pi terminals and run the following:

```
python3 PI_publisher.py
python3 PI_subscriber.py
python3 sensors.py
```

Inside PlantPalApp run following

```
python3 mqtt_publisher.py
python3 mqtt_subscriber.py
python3 manage.py updatemodels
```
Running `mqtt_publisher.py` will send score and automation data to Raspberry Pi. 
Running `mqtt_subscriber.py` will recieve the data from the Raspberry Pi sensors.
