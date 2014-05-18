import urllib.request
from bs4 import BeautifulSoup

CompleteList = []

#Get the web page 
baseURL = "http://area51.stackexchange.com"
PageBeta = urllib.request.urlopen( baseURL + "/search?q=committers%3a200" )
SoupBeta = BeautifulSoup(PageBeta)

#Process Page and Generate Output
SiteList = SoupBeta.find_all("a", attrs={'class':'proposal-hyperlink'})
for i in SiteList : 
    CompleteList.append(i.string)
    print(i.string)

#Go to next page
'''
nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})

while nextPage : #Iterate till pages remain
    PageBeta = urllib.request.urlopen( baseURL + nextPage[0].parent.attrs['href'] )
    SoupBeta = BeautifulSoup(PageBeta)

    #Process Page and Generate Output
    SiteList = SoupBeta.find_all("a", attrs={'class':'proposal-hyperlink'})
    for i in SiteList : 
        CompleteList.append(i.string)
        print(i.string)
    
    nextPage = SoupBeta.find_all("span", attrs={'class':'page-numbers next'})
'''

CompleteListFile = open("./SiteList.csv", 'w')
for i in CompleteList :
    CompleteListFile.write(i + '\n')

CompleteListFile.close()
