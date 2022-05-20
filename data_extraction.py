#!/usr/bin/env python
# coding: utf-8

# In[1]:


name = []
loc = []
bh = []
flo = []
t_floor = []
carpet_area = []
super_area = []
property_type = []
furnishing = []
poss_by = []
status = []
prices = []
lf = 1.35
f = "Pune"


# In[2]:


from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium.webdriver import ActionChains
import time


chrome_path = r"G:/Chromedriver.exe"

option = webdriver.ChromeOptions() 

option.add_argument("--disable-infobars")
option.add_argument("--disable-popup-blocking")
option.add_argument("start-maximized")

option.add_argument("--disable-extensions")

option.add_experimental_option("prefs", 
{"profile.default_content_setting_values.notifications": 2
 })
driver = webdriver.Chrome(chrome_options=option, executable_path=chrome_path)
idx = ["Pune","West","East","North","South","Central","Wakad","Hinjewadi","Balewadi","Ravet","Bavdhan","NIBM Road",
      "Undri","Keshav Nagar","Magarpatta City","Pimple Saudagar","Baner","Hadapsar","Wagholi","Warje"]

m=0
for j in idx:
    print(j)
    try:
        link = ""
        if m==0:
            link = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Pune"
        if m<6:
            #this will activate the imediate below link when m is less than 3. This link depends on the attribute of area name and city.
            link = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={j}-area-{f}"
        else:
            link = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&Locality={j}&cityName={f}"
        
        m+=1
        
        driver.get(link)
        
        height = 0
        while True:
            #driver.execute_script("window.scroll(0, 0);")
            #sleep(5)
            n_height = driver.execute_script("return document.body.scrollHeight")
            #if height == n_height and not(driver.find_element_by_class('pageLoader')):
            if height == n_height:
                break
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            sleep(10)
            height = n_height
            
        
        #for manual scrolling increase the sleep time
        # time.sleep(50)
        fsoup = BeautifulSoup(driver.page_source, "html.parser")
        a = fsoup.find_all('div', class_="mb-srp__list")
        print(len(a))
        try:
            for anchor in a:
                carea = None
                sarea = None
                location= None
                society=None
                pro = None
                fur = None
                st = None
                floor = None
                total_floor = None
                money = None
                bhk = None
                poss=None

                try:
                    price = anchor.find('div', class_="mb-srp__card__price")
                    cost = price.find('div', class_="mb-srp__card__price--amount")
                    cost = cost.text
                    cost = cost.split(" ")
                    money = float(cost[0].replace("₹", ""))
                    currency = cost[1]
                    if currency == "Lac":
                        money *= 100000
                    elif currency == "Cr":
                        money *= 10000000
                    elif currency == "K" or currency == "k":
                        money *= 1000

                    money = round(money, 2)
                except:
                    money=None
                
                data = anchor.find('div', class_="mb-srp__card__info")
                try:
                    society = data.find('a', class_="mb-srp__card__society--name").text
                except:
                    society = None
                
                
                try:
                    line = data.find('h2', class_="mb-srp__card--title").text
                    #print(line)
                    if "BHK" in line:
                        bhk = line[0]
                        pro = line.split(' ')[2]
                    else:
                        bhk = None
                        
                    
                    if " in " in line:
                        line_list = line.split(" in ")
                        # print(line_list)
                        location = line_list[1]
                        # print(location)
                    elif "for Sale" in line:
                        line_list = line.split(" Sale ")

                        print(line_list)
                        location = line_list[1]
                    else:
                        location=None
                    
                except:
                    bhk = None
                    location = None
                
                
                try:
                    if society in location:
                        location = location.replace(society, "")
                        location = location.replace(",","")
                except:
                    None
                
                
                k = data.find('div', class_="mb-srp__card__summary__list")
                item = k.find_all('div', class_="mb-srp__card__summary__list--item")
                for l in item:
                    label = l.find('div', class_="mb-srp__card__summary--label").text
                    # print("l"+label)
                    try:
                        if label == "Carpet Area":
                            carea = l.find('div', class_="mb-srp__card__summary--value").text
                            ca = carea.split(" ")
                            carea = float(ca[0])
                            if ca[1] == "sqyrd":
                                carea = float(carea*9)
                            elif ca[1] == "sqm":
                                carea = float(carea*10.764)
                            
                    except:
                        carea=None
                    try:
                        if label == "Floor":
                            t = l.find('div', class_="mb-srp__card__summary--value").text
                            t = t.split(" ")
                            floor = t[0]
                            total_floor = t[3]
                            if total_floor=="of":
                                total_floor=None
                    except:
                        floor=None
                        total_floor=None
                        # print(floor, total_floor)
                    try:
                        if label == "Super Area":
                            sarea = l.find('div', class_="mb-srp__card__summary--value").text
                            sa = sarea.split(" ")
                            sarea = float(sa[0])
                            if sa[1] == "sqyrd":
                                sarea = float(sarea*9)
                            elif sa[1] == "sqm":
                                sarea = float(sarea*10.764)
                    except:
                        sarea=None
                        
                    try:
                        if label == "Status":
                            st = l.find('div', class_="mb-srp__card__summary--value").text
                    except:
                        st = None
                            
                    try:
                        if label == "Furnishing":
                            fur = l.find('div', class_="mb-srp__card__summary--value").text
                    except:
                        fur = None
                            
                    try:
                        if label == "Under Construction":
                            poss = l.find('div', class_="mb-srp__card__summary--value").text
                            poss = poss.split("by")[1]
                    except:
                        poss = None
                #if carea == None and floor ==None and total_floor == None:
                if k == None:
                    continue
                else:
                    carpet_area.append(carea)
                    property_type.append(pro)
                    super_area.append(sarea)
                    poss_by.append(poss)
                    flo.append(floor)
                    status.append(st)
                    furnishing.append(fur)
                    t_floor.append(total_floor)
                    prices.append(money)
                    loc.append(location)    
                    bh.append(bhk)
                    name.append(society)


        except Exception as e:
            print(e)
        time.sleep(1)
    except:
        None





print(len(name))
print(len(loc))
print(len(bh))
print(len(flo))
print(len(t_floor))
print(len(carpet_area))
print(len(prices))
print(len(property_type))
print(len(furnishing))
print(len(status))


# In[4]:


import pandas as pd
dic = {
    'Name' : name,
    'Location' : loc,
    'Property Type' : property_type,
    'Price' : prices,
    'Raw Carpet Area' : carpet_area,
    'Raw Super Area' : super_area,
    'Furnishing':furnishing,
    'Status' : status,
    'Possesed by' : poss_by,
    'bhk' : bh,
    'Floor' : flo,
    'Total Floor' : t_floor
}
df = pd.DataFrame(dic)


print(df.duplicated().sum())

df = df.drop_duplicates(keep='last')

df.to_csv(f'a) {f} magicbricks data.csv', index=False)
