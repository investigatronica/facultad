#!bin/python3
import paho.mqtt.client as mqtt
import json, pymysql.cursors, os

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    mqttc.subscribe("#", 0)

def on_message(mqttc, obj, msg):
    datos=json.loads(msg.payload.decode('utf8'))
    # print (msg.topic)
    connection = pymysql.connect(host='localhost',
                             user='sensores',
                             password=os.getenv("MYSQL_SENS_PASSWORD"),
                             database='sensores_remotos',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `mediciones` (`sensor_id`, `temperatura`, `humedad`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (msg.topic, datos['temperatura'], datos['humedad']))
            connection.commit()

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.username_pw_set("gax",os.getenv("MOSQUITTO_PASS"))
mqttc.tls_set(ca_certs="/etc/ssl/certs/DST_Root_CA_X3.pem")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect(os.getenv("ABSOLUTE_URI"), 8883, 60)


mqttc.loop_forever()
