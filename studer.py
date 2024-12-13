import paho.mqtt.client as mqtt
from xcom_proto import XcomP as param
from xcom_proto import XcomRS232
from xcom_proto import XcomC
import time

# Configuration du port série
SERIAL_DEVICE = "/dev/ttyUSB0"
BAUDRATE = 115200

# Configuration MQTT
MQTT_BROKER = "192.168.0.238"  # Adresse IP de votre broker MQTT
MQTT_PORT = 1883
MQTT_CLIENT_ID = "xcom-sensor-client"
MQTT_USERNAME = "ha-mqtt"
MQTT_PASSWORD = "ha-mqtt"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print("Message Published...")

def main():
    try:
        # Initialisation de la connexion série
        xcom = XcomRS232(serialDevice=SERIAL_DEVICE, baudrate=BAUDRATE)
        print("Connexion série initialisée.")

        # Initialisation de la connexion MQTT
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        
        # Connexion au broker MQTT
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            mqtt_client.loop_start()
            print("Connexion MQTT initialisée.")
        except Exception as e:
            print(f"Erreur de connexion au broker MQTT: {e}")
            return

        while True:
            try:
                # Lecture des valeurs
                ACpower_out = round(xcom.getValue(param.AC_POWER_OUT) * 1000)
                AC_POWER_IN = round(xcom.getValue(param.AC_POWER_IN) * 1000)
                AC_ENERGY_IN_CURR_DAY = round(xcom.getValue(param.AC_ENERGY_IN_CURR_DAY) * 1000)
                BATT_Voltage1 = round(xcom.getValueByID(3000, XcomC.TYPE_FLOAT), 1)
                BATT_Temperature = xcom.getValueByID(3001, XcomC.TYPE_FLOAT)
                BATT_Discharge = round(xcom.getValueByID(3078, XcomC.TYPE_FLOAT), 1)
                BATT_Discharge2 = round(xcom.getValueByID(3076, XcomC.TYPE_FLOAT), 1)

                # Publication des valeurs sur MQTT
                mqtt_client.publish("home/sensor/ac_power_out", ACpower_out)
                mqtt_client.publish("home/sensor/ac_power_in", AC_POWER_IN)
                mqtt_client.publish("home/sensor/batt_voltage", BATT_Voltage1)
                mqtt_client.publish("home/sensor/batt_temperature", BATT_Temperature)
                mqtt_client.publish("home/sensor/batt_discharge", BATT_Discharge)
                mqtt_client.publish("home/sensor/batt_discharge2", BATT_Discharge2)
                mqtt_client.publish("home/sensor/AC_POWER_IN_CURR_DAY", AC_POWER_IN)
                print("Valeurs publiées sur MQTT.")

                # Attendre avant de lire à nouveau
                time.sleep(10)

            except Exception as e:
                print(f"Erreur lors de la lecture ou de la publication des données : {e}")

    except Exception as e:
        print(f"Erreur lors de la communication avec le périphérique Xcom: {e}")

if __name__ == "__main__":
    main()