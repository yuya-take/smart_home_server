import bme680

from logger.logger import logger


class BmeSensor:
    def __init__(self):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        logger.debug("Calibration data:")
        for name in dir(self.sensor.calibration_data):
            if not name.startswith("_"):
                value = getattr(self.sensor.calibration_data, name)
                if isinstance(value, int):
                    logger.debug("{}: {}".format(name, value))

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        logger.debug("Initial reading:")
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)
            if not name.startswith("_"):
                logger.debug("{}: {}".format(name, value))

        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def get_sensor_data(self):
        # データを更新
        self.sensor.get_sensor_data()

        temperature = self.sensor.data.temperature
        pressure = self.sensor.data.pressure
        humidity = self.sensor.data.humidity
        output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(temperature, pressure, humidity)

        if self.sensor.data.heat_stable:
            gas_resistance = self.sensor.data.gas_resistance
            logger.debug("{0},{1} Ohms".format(output, gas_resistance))
        else:
            gas_resistance = None
            logger.debug(output)
        return temperature, pressure, humidity, gas_resistance
