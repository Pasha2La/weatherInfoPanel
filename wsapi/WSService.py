import re
from wsapi.WSDriver import WSDriver
from wsapi.WSModel import WSModel


class WSService:
    def __init__(self, speed='9600'):
        # инициализируем загрузку драйвера при подключении устройства
        self.driver = WSDriver()
        self.driver.start_up(speed=speed)
        self._model = WSModel()

    def _sync(self):
        """
        Синхронизирует данные модели с данными от датчиков
        """
        # все ошибки принтим
        line = self.driver.read_line()
        if not line:
            return
        # определяем формат посылки

        # экземпляр № 1
        if re.match('LUM:[\d\.]* TMP:[\d\.]* PRS:[\d\.]* ATT:[\d\.]*', line):
            values = line.split(' ')
            try:
                self._model.luminosity = float(values[0].split(':')[-1])
                self._model.temperature = float(values[1].split(':')[-1])
                self._model.humidity = float(values[2].split(':')[-1])
                self._model.pressure = float(values[3].split(':')[-1])
                self._model.altitude = float(values[4].split(':')[-1])
                self._model.distance = None
                return
            except IndexError as e:
                print("Данные от датчиков представлены не в полном объеме")
                print(e)
        # экземпляр № 2
        elif 'Light' in line:
            self._model.luminosity = float(re.search('Light:(\d+) lux', line).group(1))
            temp_hum_line = self.driver.read_line()
            result = re.search('Temp:([-\d\.]+) °C Hum:([\d\.]+) %', temp_hum_line)
            self._model.temperature = float(result.group(1))
            self._model.humidity = float(result.group(2))
            dist_line = self.driver.read_line()
            self._model.distance = float(re.search('Dist:([\d\.]+) cm', dist_line).group(1))
            press_alt_line = self.driver.read_line()
            result = re.match('Pres:([\d\.]+) Att:([-\d\.]+)', press_alt_line)
            self._model.pressure = float(result.group(1))
            self._model.altitude = float(result.group(2))
            self.driver.read_line()
            return
        # экземпляр № 3
        elif 'Влажность' in line:
            self._model.humidity = float(re.search('Влажность:([\d\.]+)%', line).group(1))
            temp_line = self.driver.read_line()
            self._model.temperature = float(re.search('Температура:([-\d\.]+)°C', temp_line).group(1))
            # не доделано со стороны группы
            self.driver.read_line()
            lum_line = self.driver.read_line()
            self._model.luminosity = float(re.search('Свет:([-\d\.]+) lux', lum_line).group(1))
            press_line = self.driver.read_line()
            self._model.pressure = float(re.search('Давление:([-\d\.]+)мм.рт.ст.', press_line).group(1))
            alt_line = self.driver.read_line()
            self._model.altitude = float(re.search('Высота:([-\d\.]+)м.', alt_line).group(1))
            self.driver.read_line()
            return
        if len(line.split(' ')) > 0:
            if 'ERROR' in line.split(' ')[1]:
                print(line)
                return

    def get_model(self):
        """
        :return: Модель с данными из датчиков
        """
        self._sync()
        return self._model