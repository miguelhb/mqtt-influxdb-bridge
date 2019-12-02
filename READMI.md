MQTT - INFLUXDB BRIDGE

Based on: https://github.com/Nilhcem/home-monitoring-grafana/tree/master/02-bridge

Configuration: Edit broker and InfluxDB parameters in main.py
Start: python3 main.py

Manage DB: influx / show databases / use gisai / show series / select * from "series name"

If some package is not included:
 try: 	sudo apt-get install python3 
	sudo apt install python3-pip
	pip3 install paho-mqtt python-etcd influxdb	

Hyperledger: (edit chaincode version)
	./startFabric.sh
	./createPeerAdminCard.sh
	composer network install --card PeerAdmin@hlfv1 --archiveFile sensor-network@0.0.6.bna
	composer network start --networkName sensor-network --networkVersion 0.0.6 --networkAdmin admin --networkAdminEnrollSecret adminpw --card PeerAdmin@hlfv1 --file networkadmin.card 
	composer-rest-server -c admin@sensor-network -n never -u true -w true
