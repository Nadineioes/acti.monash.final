import datetime


import time
import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import Image
f = open("sleepindex.csv")
counter = -1
bluelightCol = -1

for header in f.readline().split(","):
    counter += 1
    if header == "time":
        timeCol = counter
    if header == "date":
        dateCol = counter
    if header == "activity" or header == "activity\n":
        actCol = counter
    if header == "sleepindex":
        sleepIndCol = counter
    if header == "bluelight":
        bluelightCol = counter



firstRow = f.readline().split(",")
firstTime = firstRow[timeCol]  # must remove this from CSV entirely
firstDate = firstRow[dateCol]  # must remove this from CSV entirely

s = firstDate + " " + firstTime
# FIRST TIME/DATE print(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S").timetuple()))
unixTimes = []
allTheRows = []
actList = []
sleepIndList = []
datetimes = []
bluelight = []
filedata = f.readlines()
for row in filedata:
    row = row.split(",")
    tim = row[timeCol]
    dat = row[dateCol].split("/")
    dat = str(dat[2]+"-"+dat[1]+"-"+dat[0])
    smth = dat + " " + tim
    actList.append(row[actCol].strip("\n"))
    datetimes.append(smth)
    sleepIndList.append(int(row[sleepIndCol]))

    if bluelightCol != -1:
        bluelight.append(row[bluelightCol])



for act in range(0, len(actList)):
    if actList[act] == "nan":
        actList[act] = 0
    else:
        actList[act]=float(actList[act])

activity = go.Scatter(
    x=datetimes,
    y=actList,
    fill='tozeroy',

)
colorList = []

for sleepindex in sleepIndList:
    #   str((((thing - 1) * (255 - 0)) / (5000 - 1)) + 0)
    colorList.append('rgba(' + str((sleepindex) * 255 / 10) + "," + str((sleepindex) * 255 / 10)+',255,1)')

maxact=max(actList)
sleepIndList = [maxact+10] * len(datetimes)

sleepindex = go.Bar(
            x=datetimes,
            y=sleepIndList,
    marker=dict(
        color=colorList)
)

data = [sleepindex, activity]

margin = go.Margin(l=50,r=50,t=10,b=10, pad=0)

if bluelightCol!=-1:
    light = go.Scatter(
            x=datetimes,
            y=bluelight,
            yaxis = "y2"
    )
    data.append(light)
    layout = go.Layout(autosize = False, width = 20000, height = 700, title="Actigraph Over Full Time Period", showlegend=False,
                       xaxis=dict(dtick=10800000, tickwidth=1, ticklen=8, showgrid=True),
                       yaxis=dict(zeroline=False, showticklabels=False),
                       yaxis2=dict(overlaying="y", rangemode="tozero", showgrid=True),
                       yaxis3=dict(overlaying="y2", anchor = "free", side="left", rangemode="tozero"))
    layout2 = go.Layout(showlegend=False, margin=margin, autosize = False, width=2500, height=500,
                           xaxis=dict(gridcolor="#999",autotick=False, showticklabels=False, showgrid=True, dtick=1800000, gridwidth=2),
                           yaxis=dict(zeroline=False, showticklabels=False),
                           yaxis2=dict(overlaying="y", title="Activity", rangemode="tozero", side="left", showgrid=True),
                           yaxis3=dict(title="Light (photons per square m)", overlaying="y2", side="right", rangemode="tozero"))
else:
    layout = go.Layout(showlegend=False, autosize = False, width = 20000, height = 700,title="Actigraph Over Full Time Period",
                   xaxis=dict(dtick=10800000, tickwidth=1, ticklen=8, showgrid=True))
    layout2 = go.Layout(showlegend=False, margin=margin, autosize = False, width=2500, height=500,
                           xaxis=dict(gridcolor="#999",autotick=False, showticklabels=False, dtick=1800000 ,showgrid=True, gridwidth=2),
                           yaxis=dict(zeroline=False, showticklabels=False),
                            yaxis2=dict(overlaying="y", showgrid=True, title="Activity"))


print('plotting')
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename="full.png")

Image("full.png")
print("plotted full length")
# day by day images

going = True
n=0
totalmin = (time.mktime(datetime.datetime.strptime(datetimes[-1], "%Y-%m-%d %H:%M:%S").timetuple())- time.mktime(datetime.datetime.strptime(datetimes[0], "%Y-%m-%d %H:%M:%S").timetuple()))/60


if bluelightCol!=-1:
    while going:
        if n+1440<totalmin:
            fig = go.Figure(data=[go.Bar(
                x=datetimes[n:n+1440],
                y=[max(actList[n:n+1440])+10]*len(datetimes[n:n+1440]),
                marker=dict(color=colorList[n:n+1440]))
            ,go.Scatter(
                x=datetimes[n:n+1440],
                y=actList[n:n+1440],
                fill='tozeroy', yaxis="y2"),
            go.Scatter(
                x=datetimes[n:n+1440],
                y=bluelight[n:n+1440],
                yaxis="y3"
                )], layout=layout2)
        else:
            fig = go.Figure(data=[go.Bar(
                x=datetimes[n:],
                y=[max(actList[n:])+10]*len(datetimes[n:]),
                marker=dict(
                color=colorList[n:])
            )
            ,go.Scatter(
                x=datetimes[n:],
                y=actList[n:],
                fill='tozeroy', yaxis="y2"),
            go.Scatter(
                x=datetimes[n:],
                y=bluelight[n:],
                yaxis = "y3"
                )], layout=layout2)
            going = False
        name = "day"+str(int(n/1440))+".png"
        py.image.save_as(fig,filename = name)
        Image(name)
        print("plotted "+ str(int(n/1440)))
        n += 1440

else:
    while going:
        if n+1440<totalmin:
            fig = go.Figure(data=[go.Bar(
                x=datetimes[n:n+1440],
                y=[max(actList[n:n+1440])]*len(datetimes[n:n+1440]),
                marker=dict(color=colorList[n:n+1440]))
            ,go.Scatter(
                x=datetimes[n:n+1440],
                y=actList[n:n+1440],
                fill='tozeroy',
                yaxis="y2")], layout=layout2)
        else:
            fig = go.Figure(data=[go.Bar(
                x=datetimes[n:],
                y=[max(actList[n:])]*len(datetimes[n:]),
                marker=dict(
                color=colorList[n:])
            )
            ,go.Scatter(
                x=datetimes[n:],
                y=actList[n:],
                fill='tozeroy',
                yaxis="y2")],layout=layout2)
            going = False
        name = "day"+str(int(n/1440))+".png"
        py.image.save_as(fig,filename = name)
        Image(name)
        print("plotted "+ str(int(n/1440)))
        n += 1440

f.close()

time=filedata[0].split(",")[timeCol]
date=filedata[0].split(",")[dateCol]
out = open("starttime.txt", "w")
out.write(filedata[0].split(",")[timeCol])
for i in range(len(filedata)):
    ndate = filedata[i].split(",")[dateCol]
    if ndate != date:
        date = ndate
        out.write(date)
out.close()
