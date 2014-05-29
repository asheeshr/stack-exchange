#!/usr/bin/python3

import urllib.request
import time
import datetime
from bs4 import BeautifulSoup
import csv


def scrape_proposal(site_id) :
    
    print("Started Scraping!")
    
    users = {}
    #Get the web page 
    baseURL = "http://area51.stackexchange.com/proposals/"
    #site_id = '58150'
    PageBeta = urllib.request.urlopen( baseURL + site_id + "?phase=beta")
    SoupBeta = BeautifulSoup(PageBeta)

    #Process Page and Generate Output
    print(SoupBeta.title.string)
    PropStat = SoupBeta.find_all('div', attrs={'class':'module'})[2].contents
    if 'public' in PropStat[1].string:

        for i in PropStat[23:-2]:
            if i=='\n': continue
            users[i.a.attrs['href'].split('/')[2]]= i.string.split()[0][:-1]



    elif 'private' in PropStat[1].string:
        pass
    '''
        for i in PropStat[19:-2]:
            if i=='\n': continue
            users[PropStat[19].a.attrs['href'].split('/')[2]]= i.string.split()[0][:-1]
    '''
    usersExcl = PropStat[-2].string.split()[0][:-1]

    print("Scraping complete!")
    return (usersExcl, users)


def update_csv(PropFile, site_id, data) :
    
    usersExcl, users = data

    PropFile.write( site_id + ',' + usersExcl)
    for i,j in data[1].items():
        PropFile.write(',')
        PropFile.write( i + ',' + j )

    PropFile.write('\n')
        
        


def get_betas() :

    SiteList = open("../data/sitelist.csv", 'r', newline = '')
    BetaList = csv.reader(SiteList)
    SiteIdNameList = [(s[0],s[1]) for s in BetaList if s[2] == "Beta"]
#    print(SiteIdNameList)
    SiteList.close()
    return SiteIdNameList

    #for s in BetaList :
    #    print(s[2])
    #    if s[2] == 'Beta' :
    #        print(s[0])
    #        yield(s[0])
    

def main() :
    site_list = get_betas()
    #print(site_list)
    PropFile = open("../data/" + 'useroverlap' + ".csv", 'w')
    PropFile.write( 'SiteId' + ',' + 'Exclusive' + ',' +
                    'OverlapId1' + ',' + 'OverlapPercent1' + ',' +
                    'OverlapId2' + ',' + 'OverlapPercent2' + ',' +
                    'OverlapId3' + ',' + 'OverlapPercent3' + ',' +
                    'OverlapId4' + ',' + 'OverlapPercent4' + '\n' )
                    

    for site_id in site_list[:5]:
        print(site_id[1])
        print(site_list.index(site_id) + 1) #Print Request Number
        data = scrape_proposal(site_id[0])
        print(data[0], data[1])
        
        update_csv(PropFile, site_id[0], data)

    PropFile.close()


#if __name__ == "__main__":
#    print("Running standalone")
#    guitest.main()
main()
input("Execution complete. Press any key to exit.")
#else :
 #   print("Running in terminal")
 #   main()
