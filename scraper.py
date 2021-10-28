import re
from urllib.parse import urlparse, urldefrag
import urllib
from bs4 import BeautifulSoup

longest = 0

prev_crawled = set()
longest = {}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    answer = list()
    tokens = []
    parsed = urlparse(url)
    
    if not is_valid(url) or not if_crawled_before(url):
        return list()

    if 200 <= resp.status <= 202:
        html_doc = resp.raw_response.content
        soup = BeautifulSoup(html_doc, 'html.parser')

        with open("links.txt","a", encoding="utf-8") as urlFile:
            urlFile.write(url + "/n")

            for word in soup.text.split():
                if word.isalnum() and not word == "":
                    tokens.append(word)
            longest[url] = len(tokens)

            with open("question2.txt","a", encoding="utf-8") as longestFile:
                longestFile.write(url + "\n" + str(longest[url]) + "\n")
            longestFile.close()
            with open("question3.txt","a", encoding="utf-8") as contentFile:
                contentFile.write(url + "\n" + str(tokens) + "\n")
            contentFile.close()
            
            for i in soup.find_all('a', href = True):
                temp = i['href'] 
                link = urllib.parse.urljoin("https://" + parsed.netloc, temp)
                answer.append(urldefrag(link)[0])
                urlFile.write(urldefrag(link)[0] + "\n")
        urlFile.close()
    return answer

def if_crawled_before(url):
    if url[-1] == "/":
        url = url[:-1]
    if url not in prev_crawled:
        prev_crawled.add(url)
        return True
    else:
        return False


def is_valid(url):
    try:
        allowed = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]

        valid = False
        parsed = urlparse(url)
        domain = parsed.netloc

        if domain.startswith("www."):
            domain = domain.strip("www.")

        domainlist = domain.split(".")

        subdomain = ".".join(domainlist)

        if len(domainlist) >= 4:
            subdomain = ".".join(domainlist[1:])

        if domain == "today.uci.edu" and \
            "/department/information_computer_sciences" in parsed.path:
            valid = True

        if domain == "wics.ics.uci.edu":
            return False

        if domain == "archive.ics.uci.edu":
            return False
        
        if domain == "hack.ics.uci.edu":
            return False

        if domain == "grape.ics.uci.edu":
            return False

        if domain == "intranet.ics.uci.edu":
            return False

        if not parsed.params == "":
            return False

        for eachSite in allowed:
            if subdomain == eachSite:
                valid = True

        if valid == False:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if "calendar" in parsed.path or "calendar" in parsed.query:
            return False
        
        avoidCrawl = ["calendar","css","scm","js","bmp","data","ico","png",
                      "mid","mp2","mp3","mp4","wav","avi","mov","mpeg",
                      "m4v","mkv","ogg","ogv","pdf","ps","eps","tex","ppt",
                      "pptx","doc","docx","gif","xls","dat","exe","bz2",
                      "tar","msi","bin","7z","psd","dmg","iso","epub","DS_Store"
                      "cnf","tgz","sha1","thmx","mso","arff","rtf","jar",
                      "csv","rm","smil","wmv","swf","wma","zip","rar","gz",
                      "svg","txt","py","rkt","ss","json","pdf","jpeg", 
                      "wp-content","ical", "war", "img","tiff","ram","dll"]

        for everyfiletype in avoidCrawl:
            if everyfiletype in parsed.query or everyfiletype in parsed.path:
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma"
            + r"|zip|rar|gz|apk|img|jpeg|jpg)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise