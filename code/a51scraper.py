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
    temp_status = Status[i.contents[1].div.attrs['class'][1]]
    name = i.contents[3].a.string
    CompleteList.append((name, temp_status)) #Site Name, Status
    print(name, temp_status)

#Go to next page

nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})

while nextPage : #Iterate till pages remain
    time.sleep(1)#Throttle requests
    PageBeta = urllib.request.urlopen( baseURL + nextPage[0].parent.attrs['href'] + "&pagesize=50")
    SoupBeta = BeautifulSoup(PageBeta)

    #Process Page and Generate Output
    SiteList = SoupBeta.find_all("div", attrs={'class':'proposal-summary narrow'})
    for i in SiteList : 
        temp_status = Status[i.contents[1].div.attrs['class'][1]]

        if temp_status == 'Commitment' : continue #Skip proposals in commitment

        name = i.contents[3].a.string
        CompleteList.append((name, temp_status)) #Site Name, Status
        print(name, temp_status)

    nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})


print("Scraping complete!")

CompleteListFile = open("../data/sitelist.csv", 'w')
CompleteListFile.write("Site, Status" + '\n')
for i in CompleteList :
    CompleteListFile.write('"' + i[0][1:-1] + '"' + ', ' + i[1] + '\n')

CompleteListFile.close()
