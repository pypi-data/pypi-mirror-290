import time
import subprocess
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)

print("start subprocess")
subprocess.Popen(["python3.7", "bubble2.py"])

#start meter and take readings every 5 secnods
meter.start()
for i in range(0, 120, 5):    
    time.sleep(5)
    meter.record()
meter.stop()

#process and save  data
csv_handler = CSVHandler('/home/dermot/sorting/bubble-RAPL2.csv')
trace = meter.get_trace()
csv_handler.process(trace)
csv_handler.save_data()
print("saved")

