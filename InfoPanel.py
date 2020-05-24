import datetime as dt

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication, QCheckBox, QPushButton, QSpinBox, QLineEdit, \
    QVBoxLayout, QHBoxLayout, QTextEdit
from numpy import mean
from pyqtgraph import PlotWidget
from MeasureService import MeasureService


class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.measurer = MeasureService(simulation_mode=True)
        self.temperature_history = list()
        self.humidity_history = list()
        self.pressure_history = list()
        self.timestamp_history = list()
        self.vva_temp_flag = False
        self.vva_humi_flag = False
        self.data_num = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather controller v1.1")
        self.setFixedSize(900, 500)
        self.label_general = QLabel("General settings")
        self.date_value = QLabel("")
        self.autoupdate = QCheckBox("Auto update")
        self.imitation = QCheckBox("Imitation")
        self.imitation.setChecked(True)

        self.label_min_t = QLabel("min")
        self.label_min_t.setAlignment(QtCore.Qt.AlignRight)
        self.label_min_h = QLabel("min")
        self.label_min_h.setAlignment(QtCore.Qt.AlignRight)
        self.label_max_t = QLabel("max")
        self.label_max_t.setAlignment(QtCore.Qt.AlignRight)
        self.label_max_h = QLabel("max")
        self.label_max_h.setAlignment(QtCore.Qt.AlignRight)

        self.label_interval = QLabel("Update interval (ms):")
        self.interval_line = QSpinBox()
        self.interval_line.setRange(0, 10000)
        self.interval_line.setValue(500)
        self.interval_line.setMaximumWidth(100)

        self.label_vva_temp = QLabel("Temperature VVA (C):")
        self.checkbox_vva_temp = QCheckBox()
        self.vva_temp_min = QSpinBox()
        self.vva_temp_min.setEnabled(False)
        self.vva_temp_max = QSpinBox()
        self.vva_temp_max.setEnabled(False)
        self.vva_temp_min.setMinimum(-273)
        self.vva_temp_max.setMinimum(-273)
        self.vva_temp_min.setValue(20)
        self.vva_temp_max.setValue(30)
        self.vva_temp_min.setMaximumWidth(100)
        self.vva_temp_max.setMaximumWidth(100)

        self.label_vva_humi = QLabel("Humidity VVA (%):")
        self.checkbox_vva_humi = QCheckBox()
        self.vva_humi_min = QSpinBox()
        self.vva_humi_min.setEnabled(False)
        self.vva_humi_max = QSpinBox()
        self.vva_humi_max.setEnabled(False)
        self.vva_humi_min.setMinimum(0)
        self.vva_humi_max.setMinimum(0)
        self.vva_humi_min.setMaximum(100)
        self.vva_humi_max.setMaximum(100)
        self.vva_humi_min.setValue(50)
        self.vva_humi_max.setValue(90)
        self.vva_humi_min.setMaximumWidth(100)
        self.vva_humi_max.setMaximumWidth(100)

        self.button_set_vva = QPushButton("Set VVA")
        self.button_set_vva.setEnabled(False)
        self.button_get_data = QPushButton("Get data")
        self.button_clear_plot = QPushButton("Clear plot")

        self.label_temperature = QLabel("Temperature (C):")
        self.label_humidity = QLabel("Humidity (%):")
        self.label_pressure = QLabel("Pressure (mmHg):")
        self.value_temperature = QLabel("N/A")
        self.value_humidity = QLabel("N/A")
        self.value_pressure = QLabel("N/A")

        self.plot_temperature = PlotWidget(labels={'left': 'Temperature, C'}, background=None)
        self.plot_humidity = PlotWidget(labels={'left': 'Humidity, %'}, background=None)
        self.plot_pressure = PlotWidget(labels={'left': 'Pressure, mmHg'}, background=None)
        self.plot_temperature.showGrid(x=True, y=True)
        self.plot_humidity.showGrid(x=True, y=True)
        self.plot_pressure.showGrid(x=True, y=True)

        self.curve_temperature = self.plot_temperature.plot(pen='b')
        self.curve_humidity = self.plot_humidity.plot(pen='b')
        self.curve_pressure = self.plot_pressure.plot(pen='b')

        self.curve_avg_temperature = self.plot_temperature.plot(pen='m')
        self.curve_avg_humidity = self.plot_humidity.plot(pen='m')
        self.curve_avg_pressure = self.plot_pressure.plot(pen='m')

        self.curve_min_temperature = self.plot_temperature.plot(pen='r')
        self.curve_min_humidity = self.plot_humidity.plot(pen='r')

        self.curve_max_temperature = self.plot_temperature.plot(pen='r')
        self.curve_max_humidity = self.plot_humidity.plot(pen='r')

        self.alarm_area = QTextEdit()
        self.alarm_area.setDisabled(True)

        self.button_get_data.clicked.connect(self.button_get_data_clicked)
        self.button_clear_plot.clicked.connect(self.button_clear_plot_clicked)
        self.button_set_vva.clicked.connect(self.button_set_vva_clicked
                                            )
        self.imitation.clicked.connect(self.imitation_changed)
        self.autoupdate.clicked.connect(self.auto_update_changed)

        self.checkbox_vva_temp.clicked.connect(self.vva_temp_changed)
        self.checkbox_vva_humi.clicked.connect(self.vva_humi_changed)

        self.timer.timeout.connect(self.get_data)

        main_layout = QGridLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addWidget(self.label_general, 0, 0)
        main_layout.addWidget(self.date_value, 0, 1, 1, 2)
        main_layout.addWidget(self.autoupdate, 1, 0)
        main_layout.addWidget(self.imitation, 1, 1)
        main_layout.addWidget(self.label_interval, 2, 0, 1, 2)
        main_layout.addWidget(self.interval_line, 2, 2)

        main_layout.addWidget(self.label_vva_temp, 3, 0, 1, 2)
        main_layout.addWidget(self.checkbox_vva_temp, 3, 2)
        main_layout.addWidget(self.label_min_t, 4, 1)
        main_layout.addWidget(self.vva_temp_min, 4, 2)
        main_layout.addWidget(self.label_max_t, 5, 1)
        main_layout.addWidget(self.vva_temp_max, 5, 2)

        main_layout.addWidget(self.label_vva_humi, 6, 0, 1, 2)
        main_layout.addWidget(self.checkbox_vva_humi, 6, 2)
        main_layout.addWidget(self.label_min_h, 7, 1)
        main_layout.addWidget(self.vva_humi_min, 7, 2)
        main_layout.addWidget(self.label_max_h, 8, 1)
        main_layout.addWidget(self.vva_humi_max, 8, 2)

        main_layout.addWidget(self.button_set_vva, 9, 0)
        main_layout.addWidget(self.button_get_data, 9, 1)
        main_layout.addWidget(self.button_clear_plot, 9, 2)

        main_layout.addWidget(self.label_temperature, 10, 0)
        main_layout.addWidget(self.value_temperature, 10, 1, 1, 2)
        main_layout.addWidget(self.label_humidity, 11, 0)
        main_layout.addWidget(self.value_humidity, 11, 1, 1, 2)
        main_layout.addWidget(self.label_pressure, 12, 0)
        main_layout.addWidget(self.value_pressure, 12, 1, 1, 2)

        main_layout.addWidget(self.alarm_area, 13, 0, 2, 3)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot_temperature)
        plot_layout.addWidget(self.plot_humidity)
        plot_layout.addWidget(self.plot_pressure)

        g_layout = QHBoxLayout()
        g_layout.addLayout(main_layout)
        g_layout.addLayout(plot_layout)
        self.setLayout(g_layout)
        self.show()

    def auto_update_changed(self):
        self.timer.start(int(self.interval_line.text())) if self.autoupdate.isChecked() else self.timer.stop()
        self.button_get_data.setEnabled(not self.button_get_data.isEnabled())
        self.button_clear_plot.setEnabled(not self.button_clear_plot.isEnabled())
        self.interval_line.setEnabled(not self.interval_line.isEnabled())
        self.imitation.setEnabled(not self.imitation.isEnabled())

    def button_get_data_clicked(self):
        self.get_data()

    def button_clear_plot_clicked(self):
        self.temperature_history.clear()
        self.humidity_history.clear()
        self.pressure_history.clear()
        self.timestamp_history.clear()
        self.update_main_lines()
        self.clear_avg_lines()
        self.clear_vva_temp()
        self.clear_vva_humi()

    def clear_avg_lines(self):
        self.curve_avg_temperature.setData([], [])
        self.curve_avg_humidity.setData([], [])
        self.curve_avg_pressure.setData([], [])

    def clear_vva_temp(self):
        self.curve_min_temperature.setData([], [])
        self.curve_max_temperature.setData([], [])

    def clear_vva_humi(self):
        self.curve_min_humidity.setData([], [])
        self.curve_max_humidity.setData([], [])

    def button_set_vva_clicked(self):
        if self.checkbox_vva_temp.isChecked() and self.vva_temp_is_valid():
            self.vva_temp_flag = True
        if self.checkbox_vva_humi.isChecked() and self.vva_humi_is_valid():
            self.vva_humi_flag = True

    def vva_temp_is_valid(self):
        return int(self.vva_temp_min.text()) <= int(self.vva_temp_max.text())

    def vva_humi_is_valid(self):
        return int(self.vva_humi_min.text()) <= int(self.vva_humi_max.text())

    def get_data(self):
        data = self.measurer.measure()
        if data.is_empty():
            return
        time = dt.datetime.now()
        self.date_value.setText(str(time))
        self.value_temperature.setText(str(data.temperature))
        self.value_humidity.setText(str(data.humidity))
        self.value_pressure.setText(str(data.pressure))
        self.analyse_data(data)
        self.fill_plot_data(data)

    def analyse_data(self, data):
        if self.vva_temp_flag and data.temperature > float(self.vva_temp_max.text()):
            self.alarm_area.setText("TEMP is higher than top of VVA!\n" + self.alarm_area.toPlainText())
        if self.vva_temp_flag and data.temperature < float(self.vva_temp_min.text()):
            self.alarm_area.setText("TEMP is lower than bottom of VVA!\n" + self.alarm_area.toPlainText())
        if self.vva_humi_flag and data.humidity > float(self.vva_humi_max.text()):
            self.alarm_area.setText("HUMI is higher than top of VVA!\n" + self.alarm_area.toPlainText())
        if self.vva_humi_flag and data.humidity < float(self.vva_humi_min.text()):
            self.alarm_area.setText("HUMI is lower than bottom of VVA!\n" + self.alarm_area.toPlainText())

    def fill_plot_data(self, data):
        if len(self.timestamp_history) >= 50:
            self.temperature_history.pop(0)
            self.humidity_history.pop(0)
            self.pressure_history.pop(0)
            self.timestamp_history.pop(0)
        self.update_data(data)
        self.update_main_lines()
        self.update_avg_lines()
        if self.vva_temp_flag:
            self.update_vva_temp()
        if self.vva_humi_flag:
            self.update_vva_humi()

    def update_data(self, data):
        self.temperature_history.append(float(data.temperature))
        self.humidity_history.append(float(data.humidity))
        self.pressure_history.append(float(data.pressure))
        self.timestamp_history.append(self.data_num)
        self.data_num += 1

    def update_main_lines(self):
        self.curve_temperature.setData(self.timestamp_history, self.temperature_history)
        self.curve_humidity.setData(self.timestamp_history, self.humidity_history)
        self.curve_pressure.setData(self.timestamp_history, self.pressure_history)

    def update_avg_lines(self):
        self.curve_avg_temperature.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [round(float(mean(self.temperature_history)), 2), round(float(mean(self.temperature_history)), 2)])
        self.curve_avg_humidity.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                        [mean(self.humidity_history), mean(self.humidity_history)])
        self.curve_avg_pressure.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                        [mean(self.pressure_history), mean(self.pressure_history)])

    def update_vva_temp(self):
        self.curve_min_temperature.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_temp_min.text()), float(self.vva_temp_min.text())])
        self.curve_max_temperature.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_temp_max.text()), float(self.vva_temp_max.text())])

    def update_vva_humi(self):
        self.curve_min_humidity.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_humi_min.text()), float(self.vva_humi_min.text())])
        self.curve_max_humidity.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_humi_max.text()), float(self.vva_humi_max.text())])

    def update_vva_temp(self):
        self.curve_min_temperature.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_temp_min.text()), float(self.vva_temp_min.text())])
        self.curve_max_temperature.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                           [float(self.vva_temp_max.text()), float(self.vva_temp_max.text())])

    def update_vva_humi(self):
        self.curve_min_humidity.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                        [float(self.vva_humi_min.text()), float(self.vva_humi_min.text())])
        self.curve_max_humidity.setData([min(self.timestamp_history), max(self.timestamp_history)],
                                        [float(self.vva_humi_max.text()), float(self.vva_humi_max.text())])

    def imitation_changed(self):
        self.measurer.set_simulation_mode(self.imitation.isChecked())

    def vva_temp_changed(self):
        self.vva_temp_min.setEnabled(not self.vva_temp_min.isEnabled())
        self.vva_temp_max.setEnabled(not self.vva_temp_max.isEnabled())
        self.button_set_vva.setEnabled(self.checkbox_vva_temp.isChecked() or self.checkbox_vva_humi.isChecked())
        if not self.checkbox_vva_temp.isChecked():
            self.vva_temp_flag = False
            self.clear_vva_temp()

    def vva_humi_changed(self):
        self.vva_humi_min.setEnabled(not self.vva_humi_min.isEnabled())
        self.vva_humi_max.setEnabled(not self.vva_humi_max.isEnabled())
        self.button_set_vva.setEnabled(self.checkbox_vva_temp.isChecked() or self.checkbox_vva_humi.isChecked())
        if not self.checkbox_vva_humi.isChecked():
            self.vva_humi_flag = False
            self.clear_vva_humi()


if __name__ == '__main__':
    app = QApplication([])
    info_panel = InfoPanel()
    app.exec()
