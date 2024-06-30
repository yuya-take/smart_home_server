import schedule
import time
from slack import SlackManager
from bme import BmeSensor
from database import PostgresManager
from database.models import SensorDataModel
from logger.logger import logger
from utils.error_types import CreateRecordError


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

# try:
#     postgres_manager = PostgresManager()
# except Exception as e:
#     logger.error(f"Failed to initialize PostgresManager: {e}")
#     postgres_manager = None


def monitor_message_task():
    try:
        latest_message = slack_manager.get_latest_message()
        if latest_message:
            logger.info(f"New message: {latest_message['text']}")
            text = latest_message["text"]
            if "温度" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if temperature:
                    logger.info(f"Temperature: {temperature} C")
                    slack_manager.send_message(f"温度は{temperature}℃です。")
                else:
                    slack_manager.send_message("温度を取得できませんでした。")
            if "湿度" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if humidity:
                    logger.info(f"Humidity: {humidity} %")
                    slack_manager.send_message(f"湿度は{humidity}%です。")
                else:
                    slack_manager.send_message("湿度を取得できませんでした。")
            if "気圧" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if pressure:
                    logger.info(f"Pressure: {pressure} hPa")
                    slack_manager.send_message(f"気圧は{pressure}hPaです。")
                else:
                    slack_manager.send_message("気圧を取得できませんでした。")
            if "ガス" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if gas_resistance:
                    logger.info(f"Gas Resistance: {gas_resistance} Ohms")
                    slack_manager.send_message(f"ガス抵抗は{gas_resistance}Ohmsです。")
                else:
                    slack_manager.send_message("ガス抵抗を取得できませんでした。")
            if "すべて" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if temperature and pressure and humidity:
                    slack_manager.send_message(f"温度は{temperature}℃、湿度は{humidity}%、気圧は{pressure}hPaです。")
                else:
                    slack_manager.send_message("センサーデータを取得できませんでした。")
                if gas_resistance:
                    slack_manager.send_message(f"ガス抵抗は{gas_resistance}Ohmsです。")
                else:
                    slack_manager.send_message("ガス抵抗を取得できませんでした。")
    except Exception as e:
        logger.error(f"Failed to get latest message: {e}")


# def monitor_sensor_to_save_data_task():
#     try:
#         temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
#         if temperature and pressure and humidity:
#             logger.debug(f"Temperature: {temperature} C")
#             logger.debug(f"Pressure: {pressure} hPa")
#             logger.debug(f"Humidity: {humidity} %")
#             if gas_resistance:
#                 logger.debug(f"Gas Resistance: {gas_resistance} Ohms")
#             sensor_data_model = SensorDataModel(
#                 temperature=temperature, pressure=pressure, humidity=humidity, air_quality=gas_resistance
#             )
#             try:
#                 postgres_manager.create_record_in_sensor_data(sensor_data_model)
#             except CreateRecordError as e:
#                 logger.error(str(e))
#         else:
#             logger.error("Failed to read sensor data")
#     except Exception as e:
#         logger.error(f"Failed to read sensor data: {e}")


def monitor_sensor_to_send_message_task():
    try:
        temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
        if temperature:
            slack_manager.send_message(f"温度は{temperature}℃です。")
        if pressure:
            slack_manager.send_message(f"気圧は{pressure}hPaです。")
        if humidity:
            slack_manager.send_message(f"湿度は{humidity}%です。")
        if gas_resistance:
            slack_manager.send_message(f"ガス抵抗は{gas_resistance}Ohmsです。")
    except Exception as e:
        logger.error(f"Failed to read sensor data: {e}")


def schedule_tasks():
    logger.info("Start Smart Home Scheduler")
    slack_manager.send_message("Starting the scheduler")
    schedule.every(5).seconds.do(monitor_message_task)
    # schedule.every(30).seconds.do(monitor_sensor_to_save_data_task)
    schedule.every(1).hour.do(monitor_sensor_to_send_message_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
