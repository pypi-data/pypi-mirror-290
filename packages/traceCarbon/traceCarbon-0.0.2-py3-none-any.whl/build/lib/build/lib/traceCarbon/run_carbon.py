"""Run PyJoules from a given path and add emissions"""
import click
import importlib.util
import sys

import runpy
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter

from traceCarbon.get_data import load_intensity_data, load_historical_intensity_data
from traceCarbon.carbon_trace import CarbonTrace
from traceCarbon.csv_handler import emissionsCSVHandler

def import_module_from_path(path):
    module_name = path.split("/")[-1].split(".")[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def load_intensities_from_regions(region):
    carbon_intensity_dict = {}
    for reg in region:
        intensity = load_intensity_data(reg)
        carbon_intensity_dict[reg] = intensity
    return carbon_intensity_dict 

@click.group()
def traceCarbon():
    pass

@traceCarbon.command()
@click.option('--remove_idles', default=True, help='Generate idles and remove from trace, doubles execution time')
@click.option('-r', '--region', default=['none'],multiple=True, help='Specify a region for carbon intensity, should be string representing zone identifier following electricity maps api documentation e.g. GB, DE, DE-DK1. If none is specified defaults to using ip to find location')
@click.option('-h', '--history', is_flag=True, default=False, help='Get estimate for emissions if you ran the code at different hours in the past 24 hours')
@click.option('--csv', is_flag=False, flag_value='emissions.csv', default = 'none')
@click.option('--filepath', required=True)
@click.argument('args', nargs=-1)
def emissions(filepath,remove_idles,region,history,csv,args):
    """
    Measures total energy and emissions for inputted program
    Returns a CarbonTrace object
    """
    #create meter using all domains visible to pyJoules
    devices = DeviceFactory.create_devices()
    meter = EnergyMeter(devices)
    initial_carbon_intensity = load_intensities_from_regions(region)

    try:
        meter.start(tag='user_script')
        user_module = import_module_from_path(filepath) 
        print("Running User Code")
        if hasattr(user_module, "__main__"):
            print("running as import nicely")
            user_module.__main__()
        else:
            runpy.run_path(filepath, {}, "__main__")
    
        meter.stop()
        print("User code finished running")
        #generate trace from readings
        trace = meter.get_trace()
        #generate and remove idles
        if remove_idles==True:
            print("removing idles")
            idles = meter.gen_idle(trace)
            trace.remove_idle(idles)
        
        #Get live carbon intensity data
        final_carbon_intensity = load_intensities_from_regions(region)
        
        for reg in region:
            carbon_intensity = (initial_carbon_intensity[reg]+final_carbon_intensity[reg])/2
            carbon_trace = CarbonTrace(trace, carbon_intensity, reg)
            if history:
                history_dict = load_historical_intensity_data(reg)
                carbon_trace.add_history(history_dict)
            
            if csv == 'none':
                carbon_trace.print()
            else:
                csv_handler = emissionsCSVHandler(csv)
                csv_handler.process(carbon_trace)
                csv_handler.save_data()
                print(f'Saved to {csv}') 


    except Exception as e:
        print(f"An error occurred while executing the script {filepath}:")
        print(e)
        sys.exit(1)
    

