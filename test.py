import logging
from xcom_proto import XcomP as param
from xcom_proto import XcomRS232
from xcom_proto import XcomC


# Configuration du port série
SERIAL_DEVICE = "/dev/ttyUSB0"
BAUDRATE = 115200

# Configurez le journal pour afficher les messages de débogage
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("XcomTest")

def main():
    try:
        # Initialisation de la connexion série
        logger.debug(f"Initialisation de la connexion série sur {SERIAL_DEVICE} à {BAUDRATE} bps.")
        xcom = XcomRS232(serialDevice=SERIAL_DEVICE, baudrate=BAUDRATE)
        logger.info("Connexion série initialisée.")

        # Test de lecture de la tension de la batterie
        logger.debug("Tentative de lecture")
        ACpower_out = xcom.getValue(param.AC_POWER_OUT)*1000
        logger.info(f"valeur: {ACpower_out} W")
        BATT_Voltage1 = xcom.getValueByID(3092, XcomC.TYPE_FLOAT)
        logger.info(f"valeur: {BATT_Voltage1} V")



    except Exception as e:
        logger.error(f"Erreur lors de la communication avec le périphérique Xcom: {e}")

if __name__ == "__main__":
    main()
