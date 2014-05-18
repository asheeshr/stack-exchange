import urllib.request
import time
import datetime
from bs4 import BeautifulSoup

print("Started Scraping!")

#Get the web page 
baseURL = "http://area51.stackexchange.com/proposals/"
site_id = '58150'
PageBeta = urllib.request.urlopen( baseURL + site_id + "?phase=beta")
SoupBeta = BeautifulSoup(PageBeta)

#Process Page and Generate Output
site_days = SoupBeta.find_all("span", attrs={'class':"a51-vote-count-post"})
SiteStats = SoupBeta.find_all("div", attrs={'class':"site-health-value"})
site_quesperday = SiteStats[0].string
site_anspercent = SiteStats[1].string
site_avidusers = SiteStats[2].string
site_totalusers = SiteStats[3].string
site_answerratio = SiteStats[4].string
site_visitsperday = SiteStats[5].string

UserStats = SoupBeta.ul.find_all("span")
site_users2h = UserStats[0].string[:-6]
site_users2k = UserStats[1].string[:-6]
site_users3k = UserStats[2].string[:-6]

print("Scraping complete!")
print(str(datetime.date.today()), site_quesperday, site_anspercent, site_avidusers, site_totalusers, site_answerratio, site_visitsperday,
      site_users2h, site_users2k, site_users3k )


PropFile = open("../data/" + site_id + ".csv", 'a+')
PropFile.seek(0)
if(PropFile.read(10)=="") :
    PropFile.write("Date, QuestionsPerDay, AnsweredPercent, AvidUsers, TotalUsers, AnswerRatio," + 
                    "VisitsPerDay, Users200, Users2k, Users3k" + '\n')
else :
    PropFile.seek(0,2)

PropFile.write( '"' + str(datetime.date.today()) + '"' + ', ' +
                site_quesperday + ", " +
                site_anspercent + ", " + 
                site_avidusers + ", " + 
                site_totalusers + ", " +
                site_answerratio + ", " +
                site_visitsperday + ", " +
                site_users2h + ", " + 
                site_users2k + ", " +
                site_users3k + '\n')


PropFile.close()

