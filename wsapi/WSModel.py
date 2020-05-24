class WSModel:
    def __init__(self, altitude=None, luminosity=None, humidity=None, pressure=None, temperature=None, distance=None):
        self._altitude = altitude
        self._luminosity = luminosity
        self._humidity = humidity
        self._pressure = pressure
        self._temperature = temperature
        self._distance = distance

    @property
    def altitude(self) -> float:
        """
        :return: Высота точки измерения относительно места установки метеостанции, м
        """
        return self._altitude

    @altitude.setter
    def altitude(self, value: float):
        """
        :param value: Высота точки измерения относительно места установки метеостанции, м
        """
        self._altitude = value

    def is_altitude_empty(self):
        """
        :return: Признак наличия высоты точки измерения относительно места установки метеостанции
        """
        return True if not self._altitude else False

    @property
    def luminosity(self) -> float:
        """
        :return: Уровень освещенности, люмен
        """
        return self._luminosity

    @luminosity.setter
    def luminosity(self, value: float):
        """
        :param value: Уровень освещенности, люмен
        """
        self._luminosity = value

    def is_luminosity_empty(self):
        """
        :return: Признак наличия уровня освещенности
        """
        return True if not self._luminosity else False

    @property
    def humidity(self) -> float:
        """
        :return: Относительная влажность, %
        """
        return self._humidity

    @humidity.setter
    def humidity(self, value: float):
        """
        :param value: Относительная влажность, %
        """
        self._humidity = value

    def is_humidity_empty(self):
        """
        :return: Признак наличия относительной влажности
        """
        return True if not self._humidity else False

    @property
    def pressure(self) -> float:
        """
        :return: Давление, мм.рт.ст
        """
        return self._pressure

    @pressure.setter
    def pressure(self, value: float):
        """
        :param value: Давление, мм.рт.ст
        """
        self._pressure = value

    def is_pressure_empty(self):
        """
        :return: Признак наличия давления
        """
        return True if not self._pressure else False

    @property
    def temperature(self) -> float:
        """
        :return: Температура, *С
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        """
        :param value: Температура, *С
        """
        self._temperature = value

    def is_temperature_empty(self):
        """
        :return: Признак наличия температуры
        """
        return True if not self._temperature else False

    @property
    def distance(self):
        """
        :return: Расстрояние до ближайшего сотрудника, см
        """
        return self._distance

    @distance.setter
    def distance(self, value: float):
        """
        :param value: Расстрояние до ближайшего сотрудника, см
        """
        self._distance = value

    def is_distance_empty(self):
        """
        :return: Признак наличия высоты точки измерения относительно места установки метеостанции
        """
        return True if not self._altitude else False

    def is_empty(self) -> bool:
        """
        :return: Признак инициализации модели
        """
        return self.is_altitude_empty() and self.is_distance_empty() and self.is_luminosity_empty() and \
               self.is_pressure_empty() and self.is_humidity_empty() and self.is_temperature_empty()
