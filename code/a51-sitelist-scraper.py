import urllib.request
import time
from bs4 import BeautifulSoup

print("Started Scraping!")

CompleteList = []
Status = {'beta-days':'Beta',
          'graduated-success':'Graduated',
          'failed-rip':'Closed',
          'commitment-votes':'Commitment'
          }

#Get the web page 
baseURL = "http://area51.stackexchange.com"
PageBeta = urllib.request.urlopen( baseURL + "/search?q=committers%3a200" + "&pagesize=50")
SoupBeta = BeautifulSoup(PageBeta)

#Process Page and Generate Output
SiteList = SoupBeta.find_all("div", attrs={'class':'proposal-summary narrow'})
for i in SiteList : 
    site_id = i.attrs['id'][17:]
    site_status = Status[i.contents[1].div.attrs['class'][1]]
    site_name = i.contents[3].a.string
    CompleteList.append((site_id, site_name, site_status)) #Site Id, Site Name, Status
    print(site_id, site_name, site_status)

#Go to next page
#'''
nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})

while nextPage : #Iterate till pages remain
    time.sleep(2)#Throttle requests
    PageBeta = urllib.request.urlopen( baseURL + nextPage[0].parent.attrs['href'] + "&pagesize=50")
    SoupBeta = BeautifulSoup(PageBeta)

    #Process Page and Generate Output
    SiteList = SoupBeta.find_all("div", attrs={'class':'proposal-summary narrow'})
    for i in SiteList : 
        site_id = i.attrs['id'][17:]
        site_status = Status[i.contents[1].div.attrs['class'][1]]

        if site_status == 'Commitment' : continue #Skip proposals in commitment

        site_name = i.contents[3].a.string
        CompleteList.append((site_id, site_name, site_status)) #Site Name, Status
        print(site_id, site_name, temp_status)

    nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})
#'''

print("Scraping complete!")


CompleteListFile = open("../data/sitelist.csv", 'w')
CompleteListFile.write("Id, Site, Status" + '\n')
for i in CompleteList :
    CompleteListFile.write(i[0] + ', ' + '"' + i[1][1:-1] + '"' + ', ' + i[2] + '\n')

CompleteListFile.close()
