import schedule
import time
from slack import SlackManager
from bme import BmeSensor
from database import PostgresManager
from database.models import SensorDataModel
from logger.logger import logger
from utils import calculate_discomfort_index, calculate_air_quality_index
from utils.error_types import CreateRecordError


class SmartHomeMonitor:
    def __init__(self):
        self.slack_manager = self.initialize_manager(SlackManager, "SlackManager")
        self.bme_sensor = self.initialize_manager(BmeSensor, "BmeSensor")
        self.postgres_manager = self.initialize_manager(PostgresManager, "PostgresManager")

    @staticmethod
    def initialize_manager(manager_class, manager_name):
        try:
            return manager_class()
        except Exception as e:
            logger.error(f"Failed to initialize {manager_name}: {e}")
            return None

    def monitor_message_task(self):
        try:
            latest_message = self.slack_manager.get_latest_message()
            if latest_message:
                logger.info(f"New message: {latest_message['text']}")
                response_messages = self.process_message(latest_message["text"])
                if response_messages:
                    self.slack_manager.send_message("\n".join(response_messages))
        except Exception as e:
            logger.error(f"Failed to get latest message: {e}")

    def process_message(self, text):
        response_messages = []
        if "温度" in text:
            response_messages.append(self.get_temperature_message())
        if "湿度" in text:
            response_messages.append(self.get_humidity_message())
        if "気圧" in text:
            response_messages.append(self.get_pressure_message())
        if "ガス" in text:
            response_messages.append(self.get_gas_message())
        if "不快指数" in text or "不快" in text:
            response_messages.append(self.get_discomfort_index_message())
        if "すべて" in text:
            response_messages.append(self.get_all_data_message())
        return response_messages

    def get_temperature_message(self):
        temperature, _, _, _ = self.bme_sensor.get_sensor_data()
        if temperature:
            logger.info(f"Temperature: {temperature} C")
            return f"🌡️ 温度: {temperature:.2f}℃"
        return "🌡️ 温度: データ取得失敗"

    def get_humidity_message(self):
        _, _, humidity, _ = self.bme_sensor.get_sensor_data()
        if humidity:
            logger.info(f"Humidity: {humidity} %")
            return f"💧 湿度: {humidity:.2f}%"
        return "💧 湿度: データ取得失敗"

    def get_pressure_message(self):
        _, pressure, _, _ = self.bme_sensor.get_sensor_data()
        if pressure:
            logger.info(f"Pressure: {pressure} hPa")
            return f"🌬️ 気圧: {pressure:.2f} hPa"
        return "🌬️ 気圧: データ取得失敗"

    def get_gas_message(self):
        temperature, _, humidity, gas_resistance = self.bme_sensor.get_sensor_data()
        if gas_resistance:
            if temperature and humidity:
                air_quality_index, feeling = calculate_air_quality_index(gas_resistance, temperature, humidity)
                return f"🛠️ ガス抵抗: {gas_resistance:.2f} Ohms\n🌫️ 空気質指数: {air_quality_index} ({feeling})"
            return "🌫️ 空気質指数: データ取得失敗"
        return "🛠️ ガス抵抗: データ取得失敗"

    def get_discomfort_index_message(self):
        temperature, _, humidity, _ = self.bme_sensor.get_sensor_data()
        if temperature and humidity:
            discomfort_index, feeling = calculate_discomfort_index(temperature, humidity)
            return f"🥵 不快指数: {discomfort_index} ({feeling})"
        return "🥵 不快指数: データ取得失敗"

    def get_all_data_message(self):
        temperature, pressure, humidity, gas_resistance = self.bme_sensor.get_sensor_data()
        messages = []
        messages.append(self.get_temperature_message())
        messages.append(self.get_humidity_message())
        messages.append(self.get_pressure_message())
        messages.append(self.get_gas_message())
        messages.append(self.get_discomfort_index_message())
        return "\n".join(messages)

    def monitor_sensor_to_save_data_task(self):
        try:
            temperature, pressure, humidity, gas_resistance = self.bme_sensor.get_sensor_data()
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
                    self.postgres_manager.create_record_in_sensor_data(sensor_data_model)
                except CreateRecordError as e:
                    logger.error(str(e))
            else:
                logger.error("Failed to read sensor data")
        except Exception as e:
            logger.error(f"Failed to read sensor data: {e}")

    def monitor_sensor_to_send_message_task(self):
        try:
            temperature, pressure, humidity, gas_resistance = self.bme_sensor.get_sensor_data()
            message = self.compose_sensor_message(temperature, pressure, humidity, gas_resistance)
            self.slack_manager.send_message(message)
            logger.info(f"Sent sensor data message: {message}")
        except Exception as e:
            logger.error(f"Failed to read sensor data: {e}")

    def compose_sensor_message(self, temperature, pressure, humidity, gas_resistance):
        message = "🌡️ 定期送信 📊\n"
        if temperature and humidity:
            discomfort_index, feeling = calculate_discomfort_index(temperature, humidity)
            message += f"🥵 不快指数: {discomfort_index} ({feeling})\n"
        else:
            message += "🥵 不快指数: データ取得失敗\n"
        message += f"🌡️ 温度: {temperature:.2f}℃\n" if temperature else "🌡️ 温度: データ取得失敗\n"
        message += f"🌬️ 気圧: {pressure:.2f} hPa\n" if pressure else "🌬️ 気圧: データ取得失敗\n"
        message += f"💧 湿度: {humidity:.2f}%\n" if humidity else "💧 湿度: データ取得失敗\n"
        if gas_resistance and temperature and humidity:
            air_quality_index, feeling = calculate_air_quality_index(gas_resistance, temperature, humidity)
            message += f"🛠️ ガス抵抗: {gas_resistance:.2f} Ohms\n🌫️ 空気質指数: {air_quality_index} ({feeling})\n"
        else:
            message += "🛠️ ガス抵抗: データ取得失敗\n" if not gas_resistance else "🌫️ 空気質指数: データ取得失敗\n"
        return message

    def schedule_tasks(self):
        logger.info("Start Smart Home Scheduler")
        self.slack_manager.send_message("Starting the scheduler")
        schedule.every(5).seconds.do(self.monitor_message_task)
        schedule.every(30).seconds.do(self.monitor_sensor_to_save_data_task)
        schedule.every(1).hour.do(self.monitor_sensor_to_send_message_task)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    monitor = SmartHomeMonitor()
    monitor.schedule_tasks()
