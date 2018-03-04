import csv
import datetime

time = datetime.datetime.now()

a = 'Running...'
b = str(time)
a += b
output = a

print(output)

def writeMe():

    with open('test.csv', 'w', newline='') as csvfile:
        myCSVWriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        myCSVWriter.writerow(['Test','another','and another'])
        myCSVWriter.writerow(['Test'])

def readMe():
    
    with open('test.csv', newline='') as csvfile:
        myCSVFile = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in myCSVFile:
            print(', '.join(row))

writeMe()
readMe()