import time
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)

meter.start()
for i in range(0, 120, 5):
    time.sleep(5)
    meter.record()
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/stress-package1-2.csv')
trace = meter.get_trace()
csv_handler.process(trace)
csv_handler.save_data()
print("saved")

