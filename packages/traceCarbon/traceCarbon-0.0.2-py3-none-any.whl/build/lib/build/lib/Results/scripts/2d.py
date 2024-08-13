import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

domains = [RaplPackageDomain(0), RaplPackageDomain(1), RaplDramDomain(0), RaplDramDomain(1)]
devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)

#iterates with a[0][0], a[0][1], a[0][2] etc.
def loop(a,sum1):
    for i in range(n):
        for j in range(n):
            sum1 = sum1 + a[i][j]
    return sum1

#iterates wtih a[0][0], a[1][0], a[2][0]
def loop2(a,sum1):
    for j in range(n):
        for i in range(n):
            sum1 = sum1 + a[i][j]
    return sum1

meter.start()
for n in range(1, 7000, 100):
    meter.record(tag = 'array creation')
    a= [[random.random() for i in range(n)] for j in range(n)]
    meter.record('more-cache-hits')
    loop(a,0)
    meter.record(tag = 'less-cache-hits')
    loop2(a,0)
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/2d-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()
