import glob
import sys

import serial


class WSDriver:
    def __init__(self):
        self.stream = None

    def start_up(self, dev='', speed='9600'):
        if dev is None or dev == '':
            ports = self.get_serial_ports()
            if len(ports) == 0:
                return -1
            else:
                dev = ports[0]
        self.stream = serial.Serial(port=dev, baudrate=speed)
        return 1

    def get_serial_ports(self):
        ports = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        for device in result:
            if ('serial' in device) or ('USB' in device):
                tmp = device
                result.remove(device)
                result.insert(0, tmp)
                break
        return result

    def read_line(self):
        if self.stream:
            return self.stream.readline().decode("utf-8")[:-1]
        else:
            return None

    def get_port(self):
        return self.stream._port

    def close(self):
        self.stream.close()
