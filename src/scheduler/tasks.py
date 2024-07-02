import schedule
import time
from slack import SlackManager
from bme import BmeSensor
from database import PostgresManager
from database.models import SensorDataModel
from logger.logger import logger
from utils import calculate_discomfort_index
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

try:
    postgres_manager = PostgresManager()
except Exception as e:
    logger.error(f"Failed to initialize PostgresManager: {e}")
    postgres_manager = None


def monitor_message_task():
    try:
        latest_message = slack_manager.get_latest_message()
        if latest_message:
            logger.info(f"New message: {latest_message['text']}")
            text = latest_message["text"]
            response_messages = []

            if "温度" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if temperature:
                    logger.info(f"Temperature: {temperature} C")
                    response_messages.append(f"🌡️ 温度: {temperature:.2f}℃")
                else:
                    response_messages.append("🌡️ 温度: データ取得失敗")

            if "湿度" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if humidity:
                    logger.info(f"Humidity: {humidity} %")
                    response_messages.append(f"💧 湿度: {humidity:.2f}%")
                else:
                    response_messages.append("💧 湿度: データ取得失敗")

            if "気圧" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if pressure:
                    logger.info(f"Pressure: {pressure} hPa")
                    response_messages.append(f"🌬️ 気圧: {pressure:.2f} hPa")
                else:
                    response_messages.append("🌬️ 気圧: データ取得失敗")

            if "ガス" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if gas_resistance:
                    logger.info(f"Gas Resistance: {gas_resistance} Ohms")
                    response_messages.append(f"🛠️ ガス抵抗: {gas_resistance:.2f} Ohms")
                else:
                    response_messages.append("🛠️ ガス抵抗: データ取得失敗")

            if "不快指数" in text or "不快" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                if temperature and humidity:
                    discomfort_index, feeling = calculate_discomfort_index(temperature, humidity)
                    response_messages.append(f"🥵 不快指数: {discomfort_index} ({feeling})")
                else:
                    response_messages.append("🥵 不快指数: データ取得失敗")

            if "すべて" in text:
                temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
                all_data = []
                if temperature:
                    all_data.append(f"🌡️ 温度: {temperature:.2f}℃")
                else:
                    all_data.append("🌡️ 温度: データ取得失敗")
                if humidity:
                    all_data.append(f"💧 湿度: {humidity:.2f}%")
                else:
                    all_data.append("💧 湿度: データ取得失敗")
                if pressure:
                    all_data.append(f"🌬️ 気圧: {pressure:.2f} hPa")
                else:
                    all_data.append("🌬️ 気圧: データ取得失敗")
                if gas_resistance:
                    all_data.append(f"🛠️ ガス抵抗: {gas_resistance:.2f} Ohms")
                else:
                    all_data.append("🛠️ ガス抵抗: データ取得失敗")
                if temperature and humidity:
                    discomfort_index, feeling = calculate_discomfort_index(temperature, humidity)
                    response_messages.append(f"🥵 不快指数: {discomfort_index} ({feeling})")
                else:
                    response_messages.append("🥵 不快指数: データ取得失敗")
                response_messages.append("\n".join(all_data))

            if response_messages:
                slack_manager.send_message("\n".join(response_messages))

    except Exception as e:
        logger.error(f"Failed to get latest message: {e}")


def monitor_sensor_to_save_data_task():
    try:
        temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()
        if temperature and pressure and humidity:
            logger.debug(f"Temperature: {temperature} C")
            logger.debug(f"Pressure: {pressure} hPa")
            logger.debug(f"Humidity: {humidity} %")
            if gas_resistance:
                logger.debug(f"Gas Resistance: {gas_resistance} Ohms")
            sensor_data_model = SensorDataModel(
                temperature=temperature, pressure=pressure, humidity=humidity, air_quality=gas_resistance
            )
            try:
                postgres_manager.create_record_in_sensor_data(sensor_data_model)
            except CreateRecordError as e:
                logger.error(str(e))
        else:
            logger.error("Failed to read sensor data")
    except Exception as e:
        logger.error(f"Failed to read sensor data: {e}")


def monitor_sensor_to_send_message_task():
    try:
        temperature, pressure, humidity, gas_resistance = bme_sensor.get_sensor_data()

        message = "🌡️ センサーデータ 📊\n"

        if temperature is not None:
            message += f"🌡️ 温度: {temperature:.2f}℃\n"
        else:
            message += "🌡️ 温度: データ取得失敗\n"

        if pressure is not None:
            message += f"🌬️ 気圧: {pressure:.2f} hPa\n"
        else:
            message += "🌬️ 気圧: データ取得失敗\n"

        if humidity is not None:
            message += f"💧 湿度: {humidity:.2f}%\n"
        else:
            message += "💧 湿度: データ取得失敗\n"

        if gas_resistance is not None:
            message += f"🛠️ ガス抵抗: {gas_resistance:.2f} Ohms\n"
        else:
            message += "🛠️ ガス抵抗: データ取得失敗\n"

        slack_manager.send_message(message)
        logger.info(f"Sent sensor data message: {message}")

    except Exception as e:
        logger.error(f"Failed to read sensor data: {e}")


def schedule_tasks():
    logger.info("Start Smart Home Scheduler")
    slack_manager.send_message("Starting the scheduler")
    schedule.every(5).seconds.do(monitor_message_task)
    schedule.every(30).seconds.do(monitor_sensor_to_save_data_task)
    schedule.every(1).hour.do(monitor_sensor_to_send_message_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
