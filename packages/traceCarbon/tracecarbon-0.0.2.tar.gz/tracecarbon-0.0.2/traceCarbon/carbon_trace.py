"""
Contains CarbonTrace class to deal with PyJoules meter output and add carbon emissions
"""
import copy
from functools import reduce
from operator import add
from datetime import datetime

from pyJoules.energy_trace import EnergyTrace

class CarbonTrace:
    """
    Trace EnergyTrace and add carbon emissions
    """
    def __init__(self, trace: EnergyTrace, carbon_intensity, region):
        self._samples = []
        for sample in trace._samples:
            # Add carbon emissions data to each sample
            sample = copy.deepcopy(sample)
            carbon_emissions = sample.energy.copy()
            total = 0
            for key in carbon_emissions:
                #convert to gCO2eq
                if "package" in key or "dram" in key:
                    carbon_emissions[key] *= carbon_intensity/3600/10**3/10**6
                    total += carbon_emissions[key]
            sample.total_emissions = total
            #convert the timestamp to datetime ISO format
            dt_object = datetime.fromtimestamp(sample.timestamp)
            sample.timestamp = dt_object.isoformat()
            sample.region = region
            self._samples.append(sample)

    def print(self):
        """Print the time, tag, duration, energy, and carbon emissions for each sample"""
        for sample in self._samples:
            begin_string = f'begin timestamp : {sample.timestamp}; tag : {sample.tag}; duration : {sample.duration}'
            energy_strings = [f'; {domain} : {value}' for domain, value in sample.energy.items()]
            emissions_string = f';total emissions : {sample.total_emissions}'
            region_string = f';region : {sample.region}'
            return_string = reduce(add, energy_strings, begin_string) + emissions_string + region_string
            print(return_string)
    
    def add_history(self, history_dict):
        """Add the carbon intensity history from the dictionary of datetimes and carbon intensities"""
        first_sample = self._samples[0]
        for dtime, carbon_intensity in history_dict.items():
            sample = copy.deepcopy(first_sample)
            sample.timestamp = dtime
            #add total carbon emissions
            carbon_emissions = sample.energy.copy()
            total = 0
            for key in carbon_emissions:
                #convert to gCO2eq
                if "package" in key or "dram" in key:
                    carbon_emissions[key] *= carbon_intensity/3600/10**3/10**6
                    total += carbon_emissions[key]

            sample.total_emissions = total
            self._samples.append(sample)

