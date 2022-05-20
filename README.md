
# Web-scrapping-from-a-dynamic-website

We are using this website: https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Pune

The information we are extracting are: project name, location, bhk, floor, total floor, carpet area, super area, property type, furnishing, possessed by, status and price.



## Main problem
In a simple static website you can easily scrape data, because the data is already loaded in the website. But in case of dynamic websites we have to deal with the dynamically loaded content.
To solve this problem, we are first scrolling the website and then scrapping the data.

## Dependencies

This code requires following packages:

Selenium - https://selenium-python.readthedocs.io/

BeautifulSoup - https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Pandas - https://pandas.pydata.org/

time - https://docs.python.org/3/library/time.html


## Deployment

In this code, I am using different types of links according to area and localities to scrape more data.
As we run this file the extracted information is saved into a csv file.

# Demo data
![Capture](https://user-images.githubusercontent.com/100691826/169528589-50c9f25f-8628-4cfd-9473-f203f32d1143.PNG)
