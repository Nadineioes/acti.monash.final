import sys
import os
import traceback

class MyError(Exception):
    pass

try:
    ef = open("Error_Log.txt", "w")
    ef.write("")
    ef.close()

    import ExtractSections
    name = "data"
    extension = ""

    for file in os.listdir('.'):
        if file == name+".csv" or file == name+".txt":
            extension = file.split(".")[-1]
            break

    f = open(name+"."+extension)

    fatalerror = False

    import details  # extracts details to file "details.txt"
    details.details(f)

    ExtractSections.error_gateway(name+"."+extension, "crashes.txt","Mode.txt","sleepfile.csv")
    error = open("crashes.txt").readline()
    if error!="None":
        raise MyError
    import Validate
    error = open("crashes.txt").readline()
    if error != "None":
        raise MyError
    if open("Mode.txt").readline() == "Light":
        import LightData

    # writes to "sleepindex.csv" with a copy of data from "sleepfile.csv"
    # adds the columns "sleepindex" and "movingaverages" to this. (movingaverages is the average of ACTIVITY)
    import CalculateSleepIndex
    CalculateSleepIndex.full_csv_second("sleepfile.csv")

    import summary
    summary.summary(name+"."+extension)

    # uses "sleepindex.csv" to plot
    import plotter

    f.close()
    f = open("worked.txt", "w")
    f.write("True")
    f.close()

except MyError:
    pass
except Exception:
    exc_type, exc_obj, exc_tb = sys.exc_info()

    ef = open("Error_Log.txt","w")
    traceback.print_exc(file = ef)
    ef.close()

