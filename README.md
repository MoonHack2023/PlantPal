# PlantPal

PlantPal is a  compact and innovative plant sensor - the ultimate solution for optimizing growing conditions for any type of fruit or plant.
Check out the marketing website for a full product overview and demo! https://plantpal24.wixsite.com/plantpal 
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

Suitable for any plant:

![Scalable](https://github.com/MoonHack2023/PlantPal/assets/93931659/46949615-34cb-4ae9-b87a-1b9ae08c3a0b)



Real-time and historical data view:

![Real_Time_Measurement](https://github.com/MoonHack2023/PlantPal/assets/93931659/a99f4502-21ef-42dd-aba1-ea21f0f64497)



Live performance monitoring and tips:

![Plantpal_sco](https://github.com/MoonHack2023/PlantPal/assets/93931659/a1f82bb1-b496-48f2-b2e7-f9b6566f70b0)



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
