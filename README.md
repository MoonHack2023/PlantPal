# PlantPal

Smart Environment Sensor for Plant Monitoring

## Running the web app

First clear the database with `bash clear.sh` or `python3 manage.py clear`

Then use the following commands.
```
python3 manage.py runserver
python3 tcp_server.py
python3 tcp_client.py
python3 manage.py updatemodels
```

Change the data of the graph by changing `temphum.txt`
