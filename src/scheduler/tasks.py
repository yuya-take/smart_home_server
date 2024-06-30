import schedule
import time
from slack import SlackManager
from bme import BmeSensor
from logger.logger import logger


try:
    slack_manager = SlackManager()
except Exception as e:
    logger.error(f"Failed to initialize SlackManager: {e}")
    slack_manager = None

try:
    bme_sensor = BmeSensor()
except Exception as e:
    logger.error(f"Failed to initialize BmeSensor: {e}")
    bme_sensor = None


def monitor_message_task():
    try:
        latest_message = slack_manager.get_latest_message()
        if latest_message:
            logger.info(f"New message: {latest_message['text']}")
    except Exception as e:
        logger.error(f"Failed to get latest message: {e}")


def monitor_sensor_task():
    try:
        temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
        if temperature and pressure and humidity:
            logger.info(f"Temperature: {temperature} C")
            logger.info(f"Pressure: {pressure} hPa")
            logger.info(f"Humidity: {humidity} %")
            if gas_resistance:
                logger.info(f"Gas Resistance: {gas_resistance} Ohms")
        else:
            logger.error("Failed to read sensor data")
    except Exception as e:
        logger.error(f"Failed to read sensor data: {e}")


def schedule_tasks():
    logger.info("Start Smart Home Scheduler")
    slack_manager.send_message("Starting the scheduler")
    schedule.every(10).seconds.do(monitor_message_task)
    schedule.every(10).seconds.do(monitor_sensor_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
