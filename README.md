# PlantPal

Smart Environment Sensor for Plant Monitoring

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
