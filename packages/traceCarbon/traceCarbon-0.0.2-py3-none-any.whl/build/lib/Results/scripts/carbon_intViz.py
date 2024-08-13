from get_data import load_historical_intensity_data
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime
import numpy as np

regions = ['IN','JP','GB','NO']
plt.rcParams.update({'font.size':20})
fig,ax=plt.subplots()
fig.set_figheight(10/2.54)
fig.set_figwidth(20/2.54)
ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
for region in regions:
    intensity = load_historical_intensity_data(region)
    keys = []
    for key in intensity.keys():
        key = datetime.datetime.fromisoformat(key)
        keys.append(key)
    ax.plot(keys, intensity.values(),label=region)

plt.xticks(rotation=45)
plt.xlabel("24 Hour Period 07/08/24 - 08/08/24")
plt.ylabel("CI (gCO2e/kWh)")
plt.yticks(np.arange(0,900,200))
plt.title("CI Variation by Time of Day")
plt.legend(bbox_to_anchor = (1.02,1),loc = 'upper left')
plt.tight_layout()
plt.show()

