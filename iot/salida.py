#!bin/python3
import paho.mqtt.publish as publish
import os, sys

publish.single("240ac45957b8/out", 
		sys.argv[1],
		hostname=os.getenv("ABSOLUTE_URI"),
		port=8883,
		client_id="",
		keepalive=60,
		auth={'username':"gax", 'password':os.getenv("MOSQUITTO_PASS")},
		tls={'ca_certs':"/etc/ssl/certs/DST_Root_CA_X3.pem"},
		transport="tcp")
