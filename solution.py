'''Input format: UTF-8 or UTF-16 CSV file (with any kind of line endings), with columns:


date (MM/DD/YYYY), state name, number of impressions and CTR percentage. 


Output format: UTF-8 CSV file with Unix line endings, with columns: 


date (YYYY-MM-DD), three letter country code (or XXX for unknown states), number of impressions, number of clicks (rounded, assuming the CTR is exact). 


Rows are sorted lexicographically by date followed by the country code. '''

import csv, sys, pycountry, datetime
from collections import defaultdict, Counter

#example of Country(alpha_2='PL', alpha_3='POL', name='Poland', numeric='616', official_name='Republic of Poland')
#pycountry.countries

def inWhichCountryIsRegion(check_region):
    for region in list(pycountry.subdivisions):
        if region.name == check_region:
            return pycountry.countries.get(alpha_2=region.country_code).alpha_3
def evalPercentString(percent_string):
    return eval(percent_string[0:-1])/100

def howManyClicks(impression, CTR):
    CTR_number = evalPercentString(CTR)
    return round(impression*CTR_number)

def changeDateFormat(date):
    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

data = []

def writeRow(row):
    with open('unsorted_output.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeRow(row)

def read_data():
    with open('input.csv', 'r', encoding='utf8', newline='') as csv_file: #can be UTF-8 or UTF-16, new line can be either Unix or ???
        csv_reader = csv.reader(csv_file)
        try:
            for row in csv_reader:
                data.append(row) 
                    
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format("idontunderstand", csv_reader.line_num, e)) 


read_data()


for instance in data:
    instance[0]= changeDateFormat(instance[0]) 
    instance[1]= inWhichCountryIsRegion(instance[1])
    if instance[1] == None:
        instance[1]= "XXX"
    instance[2]= eval(instance[2])
    instance[3]= howManyClicks(instance[2],instance[3])


new_data = sorted(data, key = lambda x: (x[0],x[1]))

counter = Counter()
counter2 = Counter()
for date, country_code, impression, CTI in new_data:
    counter[(date, country_code)] += impression
    counter2[(date,country_code)] += CTI

outputdata = [[date, country_code, impression] for (date,country_code), impression in counter.items()]
extra_data = [[date, country_code, CTI] for (date, country_code), CTI in counter2.items()]
for i in range(len(outputdata)):
    outputdata[i].append(extra_data[i][2])


with open('output.csv', mode='w') as writer:
    writer = csv.writer(writer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in outputdata:
        writer.writerow(row)



#for region in pycountry.subdivisions.get(country_code='CZ'):
    
#sys.stderr.write("An error has occured!") or sys.exit("Error!")
