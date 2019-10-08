MQTT - INFLUXDB BRIDGE

Based on: https://github.com/Nilhcem/home-monitoring-grafana/tree/master/02-bridge

Configuration: Edit broker and InfluxDB parameters in main.py
Start: python3 main.py

Manage DB: influx / show databases / use gisai / show series / select * from "series name"

If some package is not included:
 try: 	sudo apt-get install python3 
	sudo apt install python3-pip
	pip3 install paho-mqtt python-etcd influxdb	
