import random
from wsapi.WSModel import WSModel
from wsapi.WSService import WSService


class MeasureService:
    def __init__(self, port="/dev/ttyS1", simulation_mode=False):
        self.simulation_mode = simulation_mode
        self.port = port
        self.ws_service = WSService()

    def measure(self):
        if self.simulation_mode:
            temp = 20 + 10 * random.random()
            humi = 70 + 10 * random.random()
            pres = 750 + 20 * random.random()
            return WSModel(temperature=temp, humidity=humi, pressure=pres)
        else:
            return self.ws_service.get_model()

    def set_simulation_mode(self, simulation):
        self.simulation_mode = simulation
