import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

domains = [RaplPackageDomain(0), RaplPackageDomain(1), RaplDramDomain(0), RaplDramDomain(1)]
devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)

def insertion_sort(a):
    for i in range(1, len(a)):
        value = a[i]
        j = i-1
        while j>=0 and value<a[j]:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = value
    return a

meter.start()
for n in range(1, 25000, 1000):
    meter.record(tag = 'array creation')
    a= [random.random() for i in range(n)]
    meter.record('insertion')
    insertion_sort(a)
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/insertion-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()

