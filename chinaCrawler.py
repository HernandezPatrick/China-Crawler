from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import re, csv, bs4, os, sys
import os.path as Path

allAnnouncements = []
itinerary = []
keyOrder = ['uscc','party','brands','address','pubDate','legalRep','title','file']

def validatePath(path):
    path = Path.normpath(path)
    if Path.exists(path) is True:
        return
    else:
        print('Please enter a valid path to continue.')
        sys.exit()

regexGroups = {
    'party':[re.compile(r"""(当事人|当事人姓名/名称|当  事 人|当事人名称)([：\s ]+)([^A-Za-z0-9，：、\n]{5,15})([\s，：、])"""), 3, re.search],
    'address':[re.compile(r"""(地址|址|住址/地址|址)([：\s]{1,2})([^\s 一，\n：]{5,}([\r\n\s一]{1,}))"""), 3, re.search],
    'uscc':[re.compile(r"""(9[A-Z0-9]{17})"""), 0, re.search],
    'legalRep':[re.compile(r"""(法定代表人)([： ]+)([^\s 地址\n\d，一]{2,4})"""), 3, re.search],
    'pubDate':[re.compile(r"""\d{4}-\d{2}-\d{2}"""), 0, re.search],
    'brands':[re.compile(r"""([^a-zA-Z0-9])([a-zA-Z]{4,})([^a-zA-Z0-9])"""), 2, re.findall]
    }

ignore = ['logo','loading','english']
quitText = 'The site is loading too slowly right now- this happens occasionally. Please try again later.'

def waiter(driver, seconds, expath):
    try:
        WebDriverWait(driver, seconds).until(EC.presence_of_element_located((By.XPATH, expath)))
    except:
        return

def parse(html, csvPath):
    validatePath(csvPath)
    with open(html, mode='r', encoding='utf-8') as file:
        soup = bs4.BeautifulSoup(file, 'html.parser')
        cleanedText = re.sub(r"\u3000","\n",soup.get_text())
        
        if (soup.select('h2')):
            details = {}
            details['title'] = soup.select('h2')[0].getText()
            details['file'] = html
            
            for key, value in regexGroups.items():
                if value[2] == re.search:
                    data = value[2](value[0], cleanedText)
                    if data:
                        details[key] = data.group(value[1]).strip()
                elif value[2] == re.findall:
                    matchesList = [i[1].lower() for i in value[2](value[0], cleanedText)]
                    if matchesList:
                        filtered = [i for i in matchesList if (i in ignore) is False]
                        if bool(filtered) is True:
                            distinct = set(filtered)
                            details[key] = distinct
                            print(distinct)

            with open(Path.join(csvPath, 'parserOutput.csv'), 'a', newline='', encoding='utf-8') as file:
                myWriter = csv.writer(file, dialect='excel', delimiter='|')
                myWriter.writerow(details.get(i,'') for i in keyOrder)
                file.close()
        else:
            pass

def savePage(path, driver):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

def visitAnnouncement(url, path):
        with webdriver.Firefox() as driver:
            driver.get(url)
            waiter(driver,120,"//*[@id='easysiteText']")
            pageLinks = driver.find_elements_by_css_selector(r"div > ul > li > a")
            savePage(Path.join(path, url.split('/')[-2]) + '.html', driver)

def saveAnnouncementsList(driver, path):
    pageLinks = driver.find_elements_by_css_selector(r"div > ul > li > a")
    for element in pageLinks:
        if element.get_attribute("href"): 
            url = element.get_attribute("href")
            if 'xzcf6660' in url and url != "http://shenzhen.customs.gov.cn/shenzhen_customs/zfxxgk15/2966748/sgs62/xzcf6660/hgzscqxzcfajxxgk77/index.html":
                allAnnouncements.append(url)
                with open(Path.join(path, 'sourceURLs.txt'), mode='a+', encoding='utf-8', newline='') as f:
                    f.write(url + '\n')

def start(path, firstPage=1): 
    validatePath(path)
    base = "http://shenzhen.customs.gov.cn/eportal/ui?pageId=2967256&currentPage="
    end = "&moduleId=0d3bf877e16741e09baf6034b22ad16d"
    
    with webdriver.Firefox() as driver: 
        driver.get(base + str(firstPage) + end)
        try:
            waiter(driver,60, "//*[contains(@class,'listcontent clearfix column')]")
            lastPage = driver.find_element_by_xpath("//div/span/b").text
        except:
            print(quitText)
            sys.exit()
        print(f"The website has {lastPage} total pages. The next time you run this crawler, you can set the optional firstPage argument to {int(lastPage) + 1} to crawl from where you left off.")
        saveAnnouncementsList(driver, path)
        
        for i in range(firstPage + 1, (int(lastPage) + 1)):
            itinerary.append(base + str(i) + end)
        for url in itinerary:
            driver.get(url)
            try:
               waiter(driver,60, "//*[contains(@class,'listcontent clearfix column')]")
            except:
                print(quitText)
                sys.exit()
            saveAnnouncementsList(driver,path)
    
    for url in allAnnouncements:
        visitAnnouncement(url, path)

def runParser(path):
    validatePath(path)
    with open(Path.join(path, 'parserOutput.csv'), 'w', newline='', encoding='utf-8') as file:
        myWriter = csv.DictWriter(file, dialect='excel', delimiter='|', fieldnames=keyOrder)
        myWriter.writeheader()
        file.close()
    for root, dirs, files in os.walk(path):
        for name in files:
            if '.html' in name:
                betterPath = Path.normpath(Path.join(root, name))
                parse(betterPath, path)

if len(sys.argv) == 2:
    start(sys.argv[1])
    runParser(sys.argv[1])
elif len(sys.argv) == 3:
    if sys.argv[2] == 'parse':
        runParser(sys.argv[1])
    else:
        start(sys.argv[1], int(sys.argv[2]))
        runParser(sys.argv[1])

# To run without CLI commands, use start() to crawl the site and runParser() to parse collected HTMLs.