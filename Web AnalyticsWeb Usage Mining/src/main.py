"""
Author: Francisco Medel Molinero
Description of the script: Design a suitable data representation for the analysis - association rule mining, removing short and long visits, identifying main and micro conversions and extracting the principal statistics
Input of the function: data in csv format
Output of the function: processed_data.csv, statistics.csv, results.csv
"""

#Imports
import numpy as np
import pandas as pd
from collections import Counter

#Function to read the data
def read_data(file):
    df = pd.read_csv(file)
    return df

#this function debugs the "clicks.csv" file based on the time in seconds of the visit, if the time of the visit is too short (less than 300 seconds) or the time of the visit is too long (more than 600 seconds), then the visit is deleted
def file_cleaner(clicks, visitors):
    blackList = []
    for index, row in visitors.iterrows():
        if row['Length_seconds'] < 300 or row['Length_seconds'] > 600:
            blackList.append(row['VisitID'])
    for index, row in clicks.iterrows():
        if row['VisitID'] in blackList:
            clicks.drop(index, inplace=True)
    return clicks

#Function to extract the main statistics of the file
def GeneralStatistics(processed_data):
    #Num of visits
    num_visits=processed_data['PageName'].value_counts().sum()

    #Main conversions
    Application_conv=processed_data.PageName.value_counts().APPLICATION
    Catalog_conv = processed_data.PageName.value_counts().CATALOG

    #Micro conversions
    Discount_conv=processed_data.PageName.value_counts().DISCOUNT
    Howtojoin=processed_data.PageName.value_counts().HOWTOJOIN
    Insurance=processed_data.PageName.value_counts().INSURANCE
    Whoweare=processed_data.PageName.value_counts().WHOWEARE

    #Number of main conversions
    Num_main=Application_conv+Catalog_conv

    #Number of micro conversions
    Num_micro=Discount_conv+Howtojoin+Insurance+Whoweare

    #We save the data into a file
    with open("statistics.csv", "a") as o:
        o.write("Number of visits: "+str(num_visits)+'\n')
        o.write("Number of application: "+str(Application_conv)+'\n')
        o.write("Number of catalog: " + str(Catalog_conv) + '\n')
        o.write("Number of discount: " + str(Discount_conv) + '\n')
        o.write("Number of how to join: " + str(Howtojoin) + '\n')
        o.write("Number of insurance: " + str(Insurance) + '\n')
        o.write("Number of who we are: " + str(Whoweare) + '\n')
        o.write("Total number of main conversions: " + str(Num_main) + '\n')
        o.write("Total number of micro conversions: " + str(Num_micro) + '\n')

def frequentItems(transactions, support):
    counter = Counter()
    for trans in transactions:
        counter.update(frozenset([t]) for t in trans)
    return set(item for item in counter if counter[item]/len(transactions) >= support), counter

def generateCandidates(L, k):
    candidates = set()
    for a in L:
        for b in L:
            union = a | b
            if len(union) == k and a != b:
                candidates.add(union)
    return candidates

def filterCandidates(transactions, itemsets, support):
    counter = Counter()
    for trans in transactions:
        subsets = [itemset for itemset in itemsets if itemset.issubset(trans)]
        counter.update(subsets)
    return set(item for item in counter if counter[item]/len(transactions) >= support), counter

def apriori(transactions, support):
    result = list()
    resultc = Counter()
    candidates, counter = frequentItems(transactions, support)
    result += candidates
    resultc += counter
    k = 2
    while candidates:
        candidates = generateCandidates(candidates, k)
        candidates,counter = filterCandidates(transactions, candidates, support)
        result += candidates
        resultc += counter
        k += 1
    resultc = {item:(resultc[item]/len(transactions)) for item in resultc}
    return result, resultc

def main():
    #Load the data
    clicks = read_data('clicks.csv')
    visitors = read_data('visitors.csv')
    search_engine_map = read_data('search_engine_map.csv')

    #We remove the useless columns
    clicks= clicks.drop(['LocalID','PageID','CatName','CatID','ExtCatName','ExtCatID','TopicID','TimeOnPage','PageScore','SequenceNumber'], axis=1)
    visitors = visitors.drop(
        ['Referrer', 'Day', 'Hour','Length_pagecount'], axis=1)

    #Here we clean the data based on the duration of the visits
    processed_data=file_cleaner(clicks,visitors)

    #Report of the statistics
    GeneralStatistics(processed_data)

    #execution of the a priori algorithm
    frequentItemsets, supports = apriori(processed_data.values, 0.01)

    #Saving the results
    with open("processed_data.csv","a") as p:
        p.write(str(processed_data))

    with open("results.csv", "a") as o:
        for f in frequentItemsets:
            o.write("{} - {}".format(f, supports[f]) + '\n')

if __name__ == '__main__':
    main()