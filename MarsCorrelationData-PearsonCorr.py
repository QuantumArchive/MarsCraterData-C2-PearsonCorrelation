# -*- coding: utf-8 -*-
"""
Created on Tue June 9 07:49:05 2016

@author: Chris
"""
import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn
import statsmodels.formula.api as smf
import scipy.stats

#from IPython.display import display
%matplotlib inline

#bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

#Set Pandas to show all columns in DataFrame
pandas.set_option('display.max_columns', None)
#Set Pandas to show all rows in DataFrame
pandas.set_option('display.max_rows', None)

#data here will act as the data frame containing the Mars crater data
data = pandas.read_csv('D:\\Coursera\\marscrater_pds.csv', low_memory=False)

#convert the latitude and diameter columns to numeric and ejecta morphology is categorical
data['LATITUDE_CIRCLE_IMAGE'] = pandas.to_numeric(data['LATITUDE_CIRCLE_IMAGE'])
data['DIAM_CIRCLE_IMAGE'] = pandas.to_numeric(data['DIAM_CIRCLE_IMAGE'])
data['MORPHOLOGY_EJECTA_1'] = data['MORPHOLOGY_EJECTA_1'].astype('category')

#Any crater with no designated morphology will be replaced with NaN
data['MORPHOLOGY_EJECTA_1'] = data['MORPHOLOGY_EJECTA_1'].replace(' ',numpy.NaN)

print('First we will take the naive solution and look at the correlation between Mars Crater Latitude and Mars Crater Diameter')
print(scipy.stats.pearsonr(data['LATITUDE_CIRCLE_IMAGE'],data['DIAM_CIRCLE_IMAGE']))

print('We then look at the correlation assuming the inverse relationship')
print(scipy.stats.pearsonr(data['DIAM_CIRCLE_IMAGE'],data['LATITUDE_CIRCLE_IMAGE']))

print('This plots out the naive plot of looking purely at the Crater latitude vs. Crater diameter without filtering any data.')
seaborn.lmplot(x='LATITUDE_CIRCLE_IMAGE',y='DIAM_CIRCLE_IMAGE',data=data,hue=None)
plt.xlabel('CRATER LATITUDE (Degrees)')
plt.ylabel('CRATER DIAMETER (km)')
plt.title('MARS CRATER DATA: LATITUDE vs. DIAMETER')

print('We now look at the correlations assuming just the 3 most recurring types of craters given ejecta morphology.')
morphofinterest = ['Rd', 'SLEPS', 'SLERS']
data2 = data.loc[data['MORPHOLOGY_EJECTA_1'].isin(morphofinterest)]

#again, I'm having this weird issue where data that I filter out sitll shows up in the plot
diameter = numpy.array(data2['DIAM_CIRCLE_IMAGE'])
latitude = numpy.array(data2['LATITUDE_CIRCLE_IMAGE'])
morphology = numpy.array(data2['MORPHOLOGY_EJECTA_1'])
data3 = pandas.DataFrame({'LATITUDE':latitude,'DIAMETER':diameter,'MORPHOLOGY_EJECTA_1':morphology})

seaborn.lmplot(x='LATITUDE',y='DIAMETER',data=data3,hue='MORPHOLOGY_EJECTA_1')
plt.xlabel('CRATER LATITUDE (Degrees)')
plt.ylabel('CRATER DIAMETER (km)')
plt.title('MARS CRATER DATA: LATITUDE vs. DIAMETER')

print('We look at the correlation for just the craters with the three morphologies we were interested in.')
print(scipy.stats.pearsonr(data3['LATITUDE'],data3['DIAMETER']))

#Pearson correlation for different crater types types which will be summarized into one data table

summarycorrelations = pandas.DataFrame(columns=('MORPHOLOGY_EJECTA_1','R','R**2','P-VALUE'))

#Each loop will create a row for the newly made data frame 
for a0 in morphofinterest:
    templist = []
    templist.append(a0)
    #subset out data for specific correlation
    tempdata = data3.loc[data3['MORPHOLOGY_EJECTA_1'].isin([a0])]
    tempcor = scipy.stats.pearsonr(tempdata['LATITUDE'],tempdata['DIAMETER'])
    tempcorlist = list(tempcor)
    templist.append(tempcorlist[0])
    #add square of R to the list
    templist.append(tempcorlist[0]**2)
    #add p-value to temporary list
    templist.append(tempcorlist[1])
    #append the temporary list containing a row of data to our empty dataframe
    summarycorrelations.loc[morphofinterest.index(a0)] = templist
    
summarycorrelations