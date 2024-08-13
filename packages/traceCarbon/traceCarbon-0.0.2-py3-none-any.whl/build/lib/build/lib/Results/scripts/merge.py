import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

domains = [RaplPackageDomain(0), RaplPackageDomain(1), RaplDramDomain(0), RaplDramDomain(1)]
devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)

def merge_sort(arr):
    if len(arr) > 1:
        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements into 2 halves
        L = arr[:mid]
        R = arr[mid:]

        # Sorting the first half
        merge_sort(L)

        # Sorting the second half
        merge_sort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

meter.start()
for n in range(1, 1000000, 10000):
    meter.record(tag = 'array creation')
    a= [random.random() for i in range(n)]
    meter.record('merge')
    merge_sort(a)
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/merge-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()
