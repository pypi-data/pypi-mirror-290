import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

domains = [RaplPackageDomain(0), RaplPackageDomain(1), RaplDramDomain(0), RaplDramDomain(1)]
devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)

def selection_sort(arr):
    # Traverse through all array elements
    for i in range(len(arr)):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

meter.start()
for n in range(1, 25000, 1000):
    meter.record(tag = 'array creation')
    a = [random.random() for i in range(n)]
    meter.record(tag = 'bubble')
    selection_sort(a)
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/selection-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()

