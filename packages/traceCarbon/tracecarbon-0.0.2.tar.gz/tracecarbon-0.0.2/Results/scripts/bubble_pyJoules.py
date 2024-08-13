import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

devices = DeviceFactory.create_devices()
meter = EnergyMeter(devices)

def bubble_sort(a):
    for i in range(len(a)):
        swapped = False
        for j in range(len(a)-1-i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if swapped == False:
            break
    return

meter.start()
for n in range(1, 25000, 1000):
    print(n)
    meter.record(tag = 'bubble')
    a= [random.random() for i in range(n)]
    bubble_sort(a)
meter.stop()

csv_handler = CSVHandler('../bubble-pJ-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()

