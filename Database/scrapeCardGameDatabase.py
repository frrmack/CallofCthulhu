from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import urllib2
import sys
import re
import time

#-- TOOLS --#


def decode(htmlStr):
    return BeautifulStoneSoup(htmlStr, 
                              convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]


def connect(url):
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
        except:
            print >> sys.stderr, "\n\n%s FAIL\n" % url
            sys.exit(1)
        
        return soup


def download(url, filename=None):

    if filename is None:
        filename = url.split('/')[-1]

    page = urllib2.urlopen(url)
    local = open(filename,'w')
    local.write(page.read())
    local.close()
    print >> sys.stderr, '%s downloaded.' % filename


#-- SCRAPER FUNCTIONS --#


def getCardLinksFromGallery(cardsListPage):
    soup = connect(cardListPage)
    links = []

    page_names = soup.findAll('h1', {"style":"width:100%;height:100%;text-indent:0px;font-weight:bold"})
    for h1 in page_names:
        print >> sys.stderr, decode(h1.a.string)
        links.append(h1.a['href'])

    print>> sys.stderr,  len(page_names), 'links scraped.'
    return links


def getCardLinksFromAdvancedSearch(searchPage):
    soup = connect(searchPage)
    links = []

    pages = soup.findAll('div', {"class":"mobileheight"})
    for div in pages:
        print >> sys.stderr, decode(div.a.string)
        links.append(div.a['href'])

    print>> sys.stderr,  len(pages), 'links scraped.'
    return links


           
def recordLinksFromGallery(cardListPage, filename):
    links = getCardLinksFromGallery(cardListPage)
    f = open(filename, 'w')
    for link in links:
        print >> f, link
    f.close()


def recordLinksFromAdvancedSearch(searchPage, filename):
    links = getCardLinksFromAdvancedSearch(searchPage)
    f = open(filename, 'w')
    for link in links:
        print >> f, link
    f.close()
    

def downloadCardImage(cardPage):
    soup = connect(cardPage)

    # name
    name = decode(soup.find('h3').string)

    # image
    imgComment = soup.find(text=re.compile('<img id="cardimg"'))
    srcString = filter(lambda s: 'src=' in s, imgComment.split())[0]
    imgSource = srcString.split("'")[1]

    print >> sys.stderr, name
    download(imgSource)
    print >> sys.stderr


#-- SPECIFIC JOBS --#


# Retrive links to each card in the Core set
def scrapeCoreSetLinks():
    CoreSetPage = "http://www.cardgamedb.com/index.php/CoC/CoCCards.html/_/core-set/?search_value=&sort_col=field_60&sort_order=asc&per_page=200&st=0"
    recordLinksFromGallery(CoreSetPage, "LinkLists/Core_Set_links.txt")

def downloadCoreSetImages():
    f = open("core_set_card_links.txt", 'r')
    for line in f.readlines():
        downloadCardImage(line.strip())
        # wait a bit to avoid getting banned
        time.sleep(10)
        
def scrapeOtherSetsLinks():
    expansions = {
        'Secrets_of_Arkham' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&set=82&',
        'The_Order_of_the_Twilight' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&set=115&',
        'Forgotten_Lore' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?set=80%2C81%2C142%2C143%2C162%2C172&faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&',
        'Summons_of_the_Deep' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?set=66%2C67%2C68%2C69%2C70%2C71&faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&',
        'Dream_Lands' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&set=73%2C74%2C75%2C76%2C77%2C78&',
        'The_Yuggoth_Contract' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&set=84%2C85%2C86%2C87%2C88%2C89&',
        'The_Rituals_Of_The_Order' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?set=118%2C119%2C120%2C121%2C122%2C123&faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&',
        'Ancient_Relics' : 'http://www.cardgamedb.com/index.php/CoC/coccardsearch.html?faction=ct%2Cha%2Cmi%2Csh%2Csi%2Csy%2Cag%2Cyo%2Cne&set=145%2C146%2C147%2C148%2C149%2C150&'
        }
    for filename, url in expansions.items():
        print filename, 'Expansion \n'
        filename = 'LinkLists/'+ filename + '_links.txt'
        recordLinksFromAdvancedSearch(url, filename)        
        time.sleep(8)


def downloadAllOtherImages():
    expansions = (
        'Secrets_of_Arkham_links.txt', 
        'The_Order_of_the_Twilight_links.txt', 
        'Forgotten_Lore_links.txt', 
        'Summons_of_the_Deep_links.txt', 
        'Dream_Lands_links.txt', 
        'The_Yuggoth_Contract_links.txt', 
        'The_Rituals_Of_The_Order_links.txt', 
        'Ancient_Relics_links.txt'
        )
    for filename in expansions:
        f = open('LinkLists/' + filename, 'r')
        for line in f.readlines():
            downloadCardImage(line.strip())
            time.sleep(10)

downloadAllOtherImages()

