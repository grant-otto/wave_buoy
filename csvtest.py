import csv
from datetime import datetime

date = datetime.strftime(datetime.now(),'%Y%m%d')

filename = '/home/grant/Documents/2018_schoolyear/MAST632/wave_buoy/'+date+'wave_data.csv'




open(filename,"w+")
line=['hello', 'how are you', 'hunter is a little bitch']
for i in range(0,5):
    with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)