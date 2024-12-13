import paho.mqtt.client as mqtt
from xcom_proto import XcomP as param
from xcom_proto import XcomRS232
from xcom_proto import XcomC
import time
import argparse
import sys
import os
import json
import config

def load_config():
    config_file = os.path.expanduser("~/.config/xcom-protocol/config.py")
    if not os.path.exists(config_file):
        print("Erreur: Configuration non trouvée. Veuillez exécuter install.py d'abord.")
        sys.exit(1)
    
    sys.path.insert(0, os.path.dirname(os.path.abspath(config_file)))
    config_name = os.path.splitext(os.path.basename(config_file))[0]
    return __import__(config_name)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script de communication avec Studer via MQTT')
    parser.add_argument('--config', help='Module de configuration alternatif')
    return parser.parse_args()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print("Message Published...")

def main():
    args = parse_arguments()
    
    # Charger la configuration
    if args.config:
        sys.path.insert(0, os.path.dirname(os.path.abspath(args.config)))
        config_name = os.path.splitext(os.path.basename(args.config))[0]
        config = __import__(config_name)
    else:
        config = load_config()
    
    try:
        # Initialisation de la connexion série
        print(f"Tentative de connexion série sur {config.SERIAL_DEVICE} à {config.BAUDRATE} bauds")
        xcom = XcomRS232(serialDevice=config.SERIAL_DEVICE, baudrate=config.BAUDRATE)
        print("Connexion série initialisée.")

        # Configuration du client MQTT
        mqtt_client = mqtt.Client(config.MQTT_CLIENT_ID)
        mqtt_client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish

        # Connexion au broker MQTT
        print(f"Tentative de connexion au broker MQTT {config.MQTT_BROKER}:{config.MQTT_PORT}")
        mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT)
        mqtt_client.loop_start()
        print("Connexion MQTT initialisée.")

        while True:
            try:
                # Lecture des valeurs
                # Valeurs AC
                AC_power_out = round(float(xcom.getValue(param.AC_POWER_OUT)) * 1000)
                AC_POWER_IN = round(float(xcom.getValue(param.AC_POWER_IN)) * 1000)
                AC_ENERGY_IN_CURR_DAY = round(float(xcom.getValue(param.AC_ENERGY_IN_CURR_DAY)) * 1000)
                AC_ENERGY_IN_PREV_DAY = round(float(xcom.getValue(param.AC_ENERGY_IN_PREV_DAY)) * 1000)
                AC_ENERGY_OUT_CURR_DAY = round(float(xcom.getValue(param.AC_ENERGY_OUT_CURR_DAY)) * 1000)
                AC_ENERGY_OUT_PREV_DAY = round(float(xcom.getValue(param.AC_ENERGY_OUT_PREV_DAY)) * 1000)
                AC_FREQ_IN = float(xcom.getValue(param.AC_FREQ_IN))
                AC_FREQ_OUT = float(xcom.getValue(param.AC_FREQ_OUT))
                AC_VOLTAGE_IN = float(xcom.getValue(param.AC_VOLTAGE_IN))
                AC_VOLTAGE_OUT = float(xcom.getValue(param.AC_VOLTAGE_OUT))
                AC_CURRENT_IN = float(xcom.getValue(param.AC_CURRENT_IN))
                AC_CURRENT_OUT = float(xcom.getValue(param.AC_CURRENT_OUT))
                ENERGY_AC_IN_TOTAL = float(xcom.getValue(param.ENERGY_AC_IN_TOTAL))
                ENERGY_AC_OUT_TOTAL = float(xcom.getValue(param.ENERGY_AC_OUT_TOTAL))

                # État du système
                SYSTEM_STATE = float(xcom.getValue(param.SYSTEM_STATE))
                OPERATING_MODE = float(xcom.getValue(param.OPERATING_MODE))
                INPUT_ACTIVE = float(xcom.getValue(param.INPUT_ACTIVE))
                TRANSFER_RELAY_STATE = float(xcom.getValue(param.TRANSFER_RELAY_STATE))
                GRID_FEEDING_ACTIVE = float(xcom.getValue(param.GRID_FEEDING_ACTIVE))
                AUXILIARY_RELAY_1_STATE = float(xcom.getValue(param.AUXILIARY_RELAY_1_STATE))
                AUXILIARY_RELAY_2_STATE = float(xcom.getValue(param.AUXILIARY_RELAY_2_STATE))
                RUNNING_TIME = float(xcom.getValue(param.RUNNING_TIME))

                # Valeurs Batterie
                BATT_VOLTAGE = float(xcom.getValue(param.BATT_VOLTAGE))
                BATT_CURRENT = float(xcom.getValue(param.BATT_CURRENT))
                BATT_POWER = float(xcom.getValue(param.BATT_POWER))
                BATT_SOC = float(xcom.getValue(param.BATT_SOC))
                BATT_TEMP = float(xcom.getValue(param.BATT_TEMP))
                BATT_CYCLE_PHASE = float(xcom.getValue(param.BATT_CYCLE_PHASE))
                BATT_CHARGE = float(xcom.getValue(param.BATT_CHARGE))
                BATT_DISCHARGE = float(xcom.getValue(param.BATT_DISCHARGE))
                BATT_CHARGE_PREV_DAY = float(xcom.getValue(param.BATT_CHARGE_PREV_DAY))
                BATT_DISCHARGE_PREV_DAY = float(xcom.getValue(param.BATT_DISCHARGE_PREV_DAY))
                
                # État de santé batterie
                BATT_STATE_OF_HEALTH = float(xcom.getValue(param.BATT_STATE_OF_HEALTH))
                BATT_REMAINING_AUTONOMY = float(xcom.getValue(param.BATT_REMAINING_AUTONOMY))
                BATT_REMAINING_CAPACITY = float(xcom.getValue(param.BATT_REMAINING_CAPACITY))
                BATT_NUM_CYCLES = float(xcom.getValue(param.BATT_NUM_CYCLES))
                BATT_HISTORY_DEEPEST_DISCHARGE = float(xcom.getValue(param.BATT_HISTORY_DEEPEST_DISCHARGE))
                BATT_HISTORY_MAX_VOLTAGE = float(xcom.getValue(param.BATT_HISTORY_MAX_VOLTAGE))
                BATT_HISTORY_MIN_VOLTAGE = float(xcom.getValue(param.BATT_HISTORY_MIN_VOLTAGE))
                BATT_HISTORY_TOTAL_AH_CHARGED = float(xcom.getValue(param.BATT_HISTORY_TOTAL_AH_CHARGED))
                BATT_HISTORY_TOTAL_AH_DISCHARGED = float(xcom.getValue(param.BATT_HISTORY_TOTAL_AH_DISCHARGED))

                # Statistiques batterie
                NUM_BATTERY_UNDERVOLTAGES = float(xcom.getValue(param.NUM_BATTERY_UNDERVOLTAGES))
                NUM_BATTERY_CRITICALS = float(xcom.getValue(param.NUM_BATTERY_CRITICALS))
                NUM_BATTERY_LOW = float(xcom.getValue(param.NUM_BATTERY_LOW))

                # Valeurs Panneaux Solaires (VarioTrack)
                PV_VOLTAGE = float(xcom.getValue(param.PV_VOLTAGE))
                PV_CURRENT = float(xcom.getValue(param.PV_CURRENT))
                PV_POWER = float(xcom.getValue(param.PV_POWER))
                PV_ENERGY_CURR_DAY = float(xcom.getValue(param.PV_ENERGY_CURR_DAY))
                PV_ENERGY_PREV_DAY = float(xcom.getValue(param.PV_ENERGY_PREV_DAY))
                PV_ENERGY_TOTAL = float(xcom.getValue(param.PV_ENERGY_TOTAL))
                PV_SUN_HOURS_CURR_DAY = float(xcom.getValue(param.PV_SUN_HOURS_CURR_DAY))
                PV_SUN_HOURS_PREV_DAY = float(xcom.getValue(param.PV_SUN_HOURS_PREV_DAY))
                PV_OPERATING_MODE = float(xcom.getValue(param.PV_OPERATING_MODE))
                
                # Données techniques VarioTrack
                PV_CHARGING_CURRENT = float(xcom.getValue(param.PV_CHARGING_CURRENT))
                PV_CHARGING_POWER = float(xcom.getValue(param.PV_CHARGING_POWER))
                PV_INPUT_POWER_REDUCTION = float(xcom.getValue(param.PV_INPUT_POWER_REDUCTION))
                PV_TEMPERATURE_INTERNAL = float(xcom.getValue(param.PV_TEMPERATURE_INTERNAL))
                PV_TEMPERATURE_MAX_24H = float(xcom.getValue(param.PV_TEMPERATURE_MAX_24H))
                PV_TEMPERATURE_MAX_TOTAL = float(xcom.getValue(param.PV_TEMPERATURE_MAX_TOTAL))
                PV_NUM_OVERTEMP_TODAY = float(xcom.getValue(param.PV_NUM_OVERTEMP_TODAY))
                PV_NUM_OVERTEMP_TOTAL = float(xcom.getValue(param.PV_NUM_OVERTEMP_TOTAL))

                # VarioString
                VS_PV_POWER = float(xcom.getValue(param.VS_PV_POWER))
                VS_PV_VOLTAGE = float(xcom.getValue(param.VS_PV_VOLTAGE))
                VS_PV_CURRENT = float(xcom.getValue(param.VS_PV_CURRENT))
                VS_BATT_VOLTAGE = float(xcom.getValue(param.VS_BATT_VOLTAGE))
                VS_BATT_CURRENT = float(xcom.getValue(param.VS_BATT_CURRENT))
                VS_OPERATING_MODE = float(xcom.getValue(param.VS_OPERATING_MODE))
                VS_TEMPERATURE_INTERNAL = float(xcom.getValue(param.VS_TEMPERATURE_INTERNAL))
                VS_PV_PROD = float(xcom.getValue(param.VS_PV_PROD))
                VS_ENERGY_TODAY = float(xcom.getValue(param.VS_ENERGY_TODAY))
                VS_PV_ENERGY_PREV_DAY = float(xcom.getValue(param.VS_PV_ENERGY_PREV_DAY))
                VS_NUM_ERRORS_TODAY = float(xcom.getValue(param.VS_NUM_ERRORS_TODAY))
                VS_NUM_ERRORS_TOTAL = float(xcom.getValue(param.VS_NUM_ERRORS_TOTAL))

                # Publication des valeurs sur MQTT
                # AC
                mqtt_client.publish("home/sensor/ac_power_out", AC_power_out)
                mqtt_client.publish("home/sensor/ac_power_in", AC_POWER_IN)
                mqtt_client.publish("home/sensor/ac_energy_in_curr_day", AC_ENERGY_IN_CURR_DAY)
                mqtt_client.publish("home/sensor/ac_energy_in_prev_day", AC_ENERGY_IN_PREV_DAY)
                mqtt_client.publish("home/sensor/ac_energy_out_curr_day", AC_ENERGY_OUT_CURR_DAY)
                mqtt_client.publish("home/sensor/ac_energy_out_prev_day", AC_ENERGY_OUT_PREV_DAY)
                mqtt_client.publish("home/sensor/ac_freq_in", AC_FREQ_IN)
                mqtt_client.publish("home/sensor/ac_freq_out", AC_FREQ_OUT)
                mqtt_client.publish("home/sensor/ac_voltage_in", AC_VOLTAGE_IN)
                mqtt_client.publish("home/sensor/ac_voltage_out", AC_VOLTAGE_OUT)
                mqtt_client.publish("home/sensor/ac_current_in", AC_CURRENT_IN)
                mqtt_client.publish("home/sensor/ac_current_out", AC_CURRENT_OUT)
                mqtt_client.publish("home/sensor/energy_ac_in_total", ENERGY_AC_IN_TOTAL)
                mqtt_client.publish("home/sensor/energy_ac_out_total", ENERGY_AC_OUT_TOTAL)

                # État du système
                mqtt_client.publish("home/sensor/system_state", SYSTEM_STATE)
                mqtt_client.publish("home/sensor/operating_mode", OPERATING_MODE)
                mqtt_client.publish("home/sensor/input_active", INPUT_ACTIVE)
                mqtt_client.publish("home/sensor/transfer_relay_state", TRANSFER_RELAY_STATE)
                mqtt_client.publish("home/sensor/grid_feeding_active", GRID_FEEDING_ACTIVE)
                mqtt_client.publish("home/sensor/auxiliary_relay_1_state", AUXILIARY_RELAY_1_STATE)
                mqtt_client.publish("home/sensor/auxiliary_relay_2_state", AUXILIARY_RELAY_2_STATE)
                mqtt_client.publish("home/sensor/running_time", RUNNING_TIME)

                # Batterie
                mqtt_client.publish("home/sensor/batt_voltage", BATT_VOLTAGE)
                mqtt_client.publish("home/sensor/batt_current", BATT_CURRENT)
                mqtt_client.publish("home/sensor/batt_power", BATT_POWER)
                mqtt_client.publish("home/sensor/batt_soc", BATT_SOC)
                mqtt_client.publish("home/sensor/batt_temp", BATT_TEMP)
                mqtt_client.publish("home/sensor/batt_cycle_phase", BATT_CYCLE_PHASE)
                mqtt_client.publish("home/sensor/batt_charge", BATT_CHARGE)
                mqtt_client.publish("home/sensor/batt_discharge", BATT_DISCHARGE)
                mqtt_client.publish("home/sensor/batt_charge_prev_day", BATT_CHARGE_PREV_DAY)
                mqtt_client.publish("home/sensor/batt_discharge_prev_day", BATT_DISCHARGE_PREV_DAY)

                # État de santé batterie
                mqtt_client.publish("home/sensor/batt_state_of_health", BATT_STATE_OF_HEALTH)
                mqtt_client.publish("home/sensor/batt_remaining_autonomy", BATT_REMAINING_AUTONOMY)
                mqtt_client.publish("home/sensor/batt_remaining_capacity", BATT_REMAINING_CAPACITY)
                mqtt_client.publish("home/sensor/batt_num_cycles", BATT_NUM_CYCLES)
                mqtt_client.publish("home/sensor/batt_history_deepest_discharge", BATT_HISTORY_DEEPEST_DISCHARGE)
                mqtt_client.publish("home/sensor/batt_history_max_voltage", BATT_HISTORY_MAX_VOLTAGE)
                mqtt_client.publish("home/sensor/batt_history_min_voltage", BATT_HISTORY_MIN_VOLTAGE)
                mqtt_client.publish("home/sensor/batt_history_total_ah_charged", BATT_HISTORY_TOTAL_AH_CHARGED)
                mqtt_client.publish("home/sensor/batt_history_total_ah_discharged", BATT_HISTORY_TOTAL_AH_DISCHARGED)

                # Statistiques batterie
                mqtt_client.publish("home/sensor/num_battery_undervoltages", NUM_BATTERY_UNDERVOLTAGES)
                mqtt_client.publish("home/sensor/num_battery_criticals", NUM_BATTERY_CRITICALS)
                mqtt_client.publish("home/sensor/num_battery_low", NUM_BATTERY_LOW)

                # Panneaux Solaires (VarioTrack)
                mqtt_client.publish("home/sensor/pv_voltage", PV_VOLTAGE)
                mqtt_client.publish("home/sensor/pv_current", PV_CURRENT)
                mqtt_client.publish("home/sensor/pv_power", PV_POWER)
                mqtt_client.publish("home/sensor/pv_energy_curr_day", PV_ENERGY_CURR_DAY)
                mqtt_client.publish("home/sensor/pv_energy_prev_day", PV_ENERGY_PREV_DAY)
                mqtt_client.publish("home/sensor/pv_energy_total", PV_ENERGY_TOTAL)
                mqtt_client.publish("home/sensor/pv_sun_hours_curr_day", PV_SUN_HOURS_CURR_DAY)
                mqtt_client.publish("home/sensor/pv_sun_hours_prev_day", PV_SUN_HOURS_PREV_DAY)
                mqtt_client.publish("home/sensor/pv_operating_mode", PV_OPERATING_MODE)

                # Données techniques VarioTrack
                mqtt_client.publish("home/sensor/pv_charging_current", PV_CHARGING_CURRENT)
                mqtt_client.publish("home/sensor/pv_charging_power", PV_CHARGING_POWER)
                mqtt_client.publish("home/sensor/pv_input_power_reduction", PV_INPUT_POWER_REDUCTION)
                mqtt_client.publish("home/sensor/pv_temperature_internal", PV_TEMPERATURE_INTERNAL)
                mqtt_client.publish("home/sensor/pv_temperature_max_24h", PV_TEMPERATURE_MAX_24H)
                mqtt_client.publish("home/sensor/pv_temperature_max_total", PV_TEMPERATURE_MAX_TOTAL)
                mqtt_client.publish("home/sensor/pv_num_overtemp_today", PV_NUM_OVERTEMP_TODAY)
                mqtt_client.publish("home/sensor/pv_num_overtemp_total", PV_NUM_OVERTEMP_TOTAL)

                # VarioString
                mqtt_client.publish("home/sensor/vs_pv_power", VS_PV_POWER)
                mqtt_client.publish("home/sensor/vs_pv_voltage", VS_PV_VOLTAGE)
                mqtt_client.publish("home/sensor/vs_pv_current", VS_PV_CURRENT)
                mqtt_client.publish("home/sensor/vs_batt_voltage", VS_BATT_VOLTAGE)
                mqtt_client.publish("home/sensor/vs_batt_current", VS_BATT_CURRENT)
                mqtt_client.publish("home/sensor/vs_operating_mode", VS_OPERATING_MODE)
                mqtt_client.publish("home/sensor/vs_temperature_internal", VS_TEMPERATURE_INTERNAL)
                mqtt_client.publish("home/sensor/vs_pv_prod", VS_PV_PROD)
                mqtt_client.publish("home/sensor/vs_energy_today", VS_ENERGY_TODAY)
                mqtt_client.publish("home/sensor/vs_pv_energy_prev_day", VS_PV_ENERGY_PREV_DAY)
                mqtt_client.publish("home/sensor/vs_num_errors_today", VS_NUM_ERRORS_TODAY)
                mqtt_client.publish("home/sensor/vs_num_errors_total", VS_NUM_ERRORS_TOTAL)

                print("Valeurs publiées sur MQTT.")

                # Attendre avant de lire à nouveau
                time.sleep(10)

            except Exception as e:
                print(f"Erreur lors de la lecture ou de la publication des données : {e}")

    except Exception as e:
        print(f"Erreur lors de la communication avec le périphérique Xcom: {e}")

if __name__ == "__main__":
    main()