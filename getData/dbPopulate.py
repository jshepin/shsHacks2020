## script to populate database of zipcodes and relevant carbon emisions data, given various csv files of us census data and irs tax data
## written by johnny burrer, except for the noted function written by iyad hamid

import csv
from math import ceil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbSetup import Base,Zipcode

## stuff to access database

#engine=create_engine('mysql+pymysql://garageapp:nega5897@localhost/shshacks2020')
engine=create_engine('mysql+pymysql://root:R0man5 0416@localhost/zipcodeDB')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

## function to calculate carbon emssions given population and average monthly income
## written by iyad hamid

def getEmissions(people,income,unit='tons'):
    total=.039548*income+8.61582
    total*=ceil(people)
    if unit=='mtons':
        return total/2204.62262
    elif unit=='lbs':
        return total*2000.0
    return total

## reads various csv files, builds 2d array in which each item contains:
## [zip code,population,population density,average annual income]

#accesses file to read zip codes and population
zipReader=csv.reader(open('zipData.csv'),delimiter=',')
zipcodes=[]
for row in zipReader:
    if row[6]=='IL':
        #population figure uses 2015 census data, updates figure using average population growth rate of illinois
        zipcodes.append([row[0],int(float(row[14])*(1.0362**5))])
#accesses file to read square mileage of zip code, used to calculate population density 
zipPopReader=csv.reader(open('popData.csv'),delimiter=',')
for row in zipPopReader:
    for i in range(len(zipcodes)):
        if row[0]==zipcodes[i][0]:
           temp=zipcodes[i]
           temp.append(int(temp[1]/float(row[2])))
           zipcodes[i]=temp
#accesses file to read amount of people per tax bracket within zip code, used to determine average annual income 
incomeReader=csv.reader(open('irs.csv'),delimiter=',')
rows=[]
for row in incomeReader:
    temp=[]
    for col in row:
        if col!='' and col!='Total':
            temp.append(col)
    if len(temp)!=0:
        rows.append(temp)
for i in range(7):
    del rows[0]
for i in range(18):
    del rows[-1]
chunks=[]
temp=[]
for i in range(len(rows)):
    if i%7==0:
        chunks.append(temp)
        temp=[]
    temp.append(rows[i])
del chunks[0]
#average income per tax bracket
incomes=[12500,37500,62500,87500,150000,225000]
zipIncomes=[]
for chunk in chunks:
    numPeople=int(chunk[0][1].replace(',',''))
    totalMoney=0
    for row in range(1,len(chunk)):
        totalMoney+=int(chunk[row][2].replace(',','').replace('**','0'))*incomes[row-1]
    zipIncomes.append([chunk[0][0],int(totalMoney/numPeople)])
for item in zipIncomes:
    for i in range(len(zipcodes)):
        if item[0]==zipcodes[i][0]:
            temp=zipcodes[i]
            temp.append(item[1])
            zipcodes[i]=temp

zipCoordinates=open('zipCoordinates.csv','r').read().split('\n')
del zipCoordinates[0]
coords=[]
zipCoordinates=[i for i in zipCoordinates if i]
for row in zipCoordinates:
    row=row.split(',')
    coords.append([row[3],row[-3],row[-2]])
for zipcode in zipcodes:
    for coord in coords:
        if zipcode[0]==coord[0]:
            zipcode.append(coord[1])
            zipcode.append(coord[2])

## uses collected data to build database, determines carbon emissions for each zip code with getEmissions function and collected data

for i in zipcodes:
    if len(i)==6:
        session.add(Zipcode(zipcode=i[0],emissions=int(getEmissions(i[1],int(i[3]/52))),pop=i[1],popDensity=i[2],income=i[3],latitude=i[4],longitude=i[5]))
session.commit()
