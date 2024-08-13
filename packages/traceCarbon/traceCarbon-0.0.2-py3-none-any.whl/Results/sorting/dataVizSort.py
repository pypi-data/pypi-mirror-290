import pandas as pd
import matplotlib.pyplot as plt

#Read files
plt.rcParams.update({'font.size':20})
bubble = pd.read_csv("sorting/bubble.csv", delimiter=";")
select = pd.read_csv("sorting/selection.csv", delimiter=";")
insert = pd.read_csv("sorting/insertion.csv", delimiter=";")
merge = pd.read_csv("sorting/merge.csv", delimiter=";")
quick = pd.read_csv("sorting/quick.csv", delimiter=";")

#Add emissions for each sort to a separate dataframe
df = pd.DataFrame()
df['bubble'] = bubble['emissions']
df['selection'] = select['emissions']
df['insertion'] = insert['emissions']
df['quick'] = quick['emissions']
df['merge'] = merge['emissions']

#Add input size column to dataframe
df['n'] = [i for i in range(0, 50000, 5000)]
print(df)

fig,ax = plt.subplots()
fig.set_figheight(12/2.54)
fig.set_figwidth(20/2.54)

df.plot(ax=ax, x='n', y='bubble', label="Bubble", linewidth=2.0)
df.plot(ax=ax, x='n', y='selection', label="Selection", linewidth=2.0)
df.plot(ax=ax, x='n', y='insertion', label="Insertion", linewidth=2.0)
df.plot(ax=ax, x='n', y='merge', label="Merge", linewidth=2.0)
df.plot(ax=ax, x='n', y='quick', label="Quick", linewidth=2.0)
plt.xlabel("Input Size")
plt.ylabel("Emissions (gCO2e)")
plt.title("Emissions for Sorting Algorithms")
plt.legend()
plt.tight_layout()
fig = plt.gcf()
fig.savefig('sorting',dpi=500)