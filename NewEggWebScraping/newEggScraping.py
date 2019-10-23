import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

newegg_url = "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card"
uClient = uReq(newegg_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')

videocards = page_soup.findAll("div", {"class":"item-container"})

for videocard in videocards:
    brand = videocard.find("div", {"class":"item-branding"}).img["title"]
    prodName = videocard.find("img",{"class":"lazy-img"})["title"]
    print("Brand: " + brand)
    print("Product: " + prodName )
    print()