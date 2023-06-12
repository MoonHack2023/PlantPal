# PlantPal

PlantPal is a  compact and innovative plant sensor - the ultimate solution for optimizing growing conditions for any type of fruit or plant.
Using the 4 sensors below, 
- Air temperature and humidity sensor (Si7021)
- Spectral light (AS7262)
- Gas Sensor (CCS811)
- Air velocity sensor (D6F-V03A1)

PlantPal effectively measures the surroundings of any plant in any environment by capturing the following measurements in real-time:
- Temperature 
- TVOC
- Humidity
- CO2
- Spectral Light 
- Average Light Intensity 
- Air Velocity

## Key Features

Extensive data-processing and an incredible user-interface make PlantPal a must for seasoned and noivce plant enthusiasts. 
![image](https://github.com/MoonHack2023/PlantPal/assets/93931659/97fdcfdd-faa4-4ce1-a549-42f896446fd7)
![image](https://github.com/MoonHack2023/PlantPal/assets/93931659/73c3657b-abaf-48b3-8974-25e47fe2741a)

## Key Features 

For a complete product overview and demonstration check out the marketing website:
https://plantpal24.wixsite.com/plantpal


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
