import tldextract
import requests 

###########################################
# Customize these parameters!             #
###########################################
WEB_CRAWLER_START_URL="http://github.com"
DOMAIN_NAME_LOG_FILE="visited_domains.log"
MAXIMUM_VISITS_TO_A_SINGLE_DOMAIN_NAME=10
###########################################

visitedURLs=set()
visitedDomains={}

def getDomain(url):
    ex=tldextract.extract(url)
    return ex.domain+'.'+ex.suffix

def findNextDifferentURL(content,start):
    while True:
        match_open=content.find("a href=\"http",start)
        if(match_open!=-1):
            match_close=content.find('"',match_open+8)
            url=content[match_open+8:match_close]
            domain=getDomain(url)
            if (not url in visitedURLs) and (not domain in visitedDomains or visitedDomains[domain]<MAXIMUM_VISITS_TO_A_SINGLE_DOMAIN_NAME) and (not '?' in url):
                return [match_open+8,match_close]
            start=match_close;
        else:
            return None

if __name__ == "__main__":
    ff=open(DOMAIN_NAME_LOG_FILE,'w');
    pageStack=[[WEB_CRAWLER_START_URL,0]]
    print("Starting web crawl at URL "+WEB_CRAWLER_START_URL+"!\n----------")
    while True:
        try:
            resp=requests.get(pageStack[-1][0])
            visitedURLs.add(pageStack[-1][0])
            domain=getDomain(pageStack[-1][0])
            if not domain in visitedDomains:
                visitedDomains[domain]=0
                ff.write(domain+'\n')
            visitedDomains[domain]+=1
            content=str(resp.content)
            rangePair=findNextDifferentURL(content,pageStack[-1][1])
            if(rangePair==None):
                print("Backtracking ...")
                pageStack.pop()
                continue
            pageStack[-1][1]=rangePair[0]
            s=content[rangePair[0]:rangePair[1]]
            print(s)
            pageStack.append([s,0])
        except Exception as e:
            print(e)
            pageStack.pop()
    ff.close();
