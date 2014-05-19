import urllib.request
import time
import datetime
from bs4 import BeautifulSoup
import csv

def scrape_proposal(site_id) :
    
    print("Started Scraping!")
    
    #Get the web page 
    baseURL = "http://area51.stackexchange.com/proposals/"
    #site_id = '58150'
    PageBeta = urllib.request.urlopen( baseURL + site_id + "?phase=beta")
    SoupBeta = BeautifulSoup(PageBeta)

    #Process Page and Generate Output
    print(SoupBeta.title)
    site_days = SoupBeta.find_all("span", attrs={'class':"a51-vote-count-post"}) #This needs to handle commas?
    SiteStats = SoupBeta.find_all("div", attrs={'class':"site-health-value"})
    site_quesperday = SiteStats[0].string.replace(",","")
    site_anspercent = SiteStats[1].string.replace(",","")
    site_avidusers = SiteStats[2].string.replace(",","")
    site_totalusers = SiteStats[3].string.replace(",","")
    site_answerratio = SiteStats[4].string.replace(",","")
    site_visitsperday = SiteStats[5].string.replace(",","")
    
    UserStats = SoupBeta.ul.find_all("span")
    site_users2h = UserStats[0].string[:-6].replace(",","")
    site_users2k = UserStats[1].string[:-6].replace(",","")
    site_users3k = UserStats[2].string[:-6].replace(",","")

    print("Scraping complete!")
    return (str(datetime.date.today()), site_quesperday, site_anspercent, site_avidusers, site_totalusers, site_answerratio, 
            site_visitsperday, site_users2h, site_users2k, site_users3k)


def update_csv(site_id, data) :
    today, site_quesperday, site_anspercent, site_avidusers, site_totalusers, site_answerratio, site_visitsperday, site_users2h, site_users2k, site_users3k = data #Unpack the tuple

    PropFile = open("../data/betas" + site_id + ".csv", 'a+')

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


def get_betas() :

    SiteList = open("../data/sitelist.csv", 'r', newline = '')
    BetaList = csv.reader(SiteList)
    SiteIdList = [s[0] for s in BetaList if s[2] == "Beta"]
    SiteList.close()
    return SiteIdList
    #for s in BetaList :
    #    print(s[2])
    #    if s[2] == 'Beta' :
    #        print(s[0])
    #        yield(s[0])
    

def main() :
    site_list = get_betas()
    for site_id in site_list:
        print(site_list.index(site_id) + 1) #Print Request Number
        data = scrape_proposal(site_id)
        print(data)
        update_csv(site_id, data)


#if __name__ == "__main__":
main()
