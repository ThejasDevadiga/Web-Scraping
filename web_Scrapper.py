# ----------------------------------------------------------------
# THEJAS DEVADIGA
# 09-08-2022
# mrdevadigatj@gmail.com

# ----------------------------------------------------------------

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
import re


options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome("../chromedriver.exe"  ,options=options)
 
def collect_Data(item):
    # Declaring the items
    products=[] 
    prices=[]  
    ratings=[] 
    brands=[] 
    specifications=[]
    
    # Find the number of items Available in the product list
    driver.get(f"https://www.flipkart.com/search?q={item}")
    content = driver.page_source
    
    soup = BeautifulSoup(content,features="html.parser")
    length_Of_data = soup.find('span', attrs={'class': '_10Ermr'}).text
    
    # Extract the number
    beg = length_Of_data.find("f")
    end = length_Of_data.find("r")
    length_Of_data = int(length_Of_data[beg+1:end].replace(',', ""))
    
    #If the length_Of_data is greater than 1000 set that to 1000
    if(length_Of_data>1000):
        length_Of_data = 1080

    #  Calculate the number of page
    number_of_page = int(length_Of_data/24)
    
    # Iterate over each page_source 
    for page in range(number_of_page):
        # extract the page_source  data
        driver.get(f"https://www.flipkart.com/search?q={item}&page={page+1}")
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")
        
        # Iterate over each of the items in the source
        for a in soup.findAll('a',href=True, attrs={'class':'_1fQZEK'}):  
            name=a.find('div', attrs={'class':'_4rR01T'})
            price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
            rating=a.find('div', attrs={'class':'_3LWZlK'})
            
            # IF no data is available then set that to 0
            if(name!=None):
                products.append(name.text)
            else:
                products.append("LAPTOP")
            if(price!=None):
                prices.append(price.text)
            else:
                prices.append(0)
            
            if(rating!=None):
                ratings.append(rating.text) 
            else:
                ratings.append(0)
    # Extract the specifications and brand names from the product list
    index = 0
    for product in products:
        # Extract the brand name
        prod_brand = product.split(' ',1)
        brands.append(prod_brand[0])
        product =  prod_brand[1]
        beg = product.find("(")
        end = product.find(")")
        # Extract the product specifications
        specifications.append(product[beg+1:end])
        product= product.replace(product[beg+1:end], " ") 
        products[index]= re.sub(r"[\(\)]",'',product)
        index+=1
        
    print("Length of product list"+len(products))
    print("Length of brand list"+len(brands))
    print("Length of product specifications"+len(specifications))
    print("Length of product prices"+len(prices))
    print("Length of product rating list"+len(ratings))
    df = pd.DataFrame({'brand':brands,'Product Name':products,'specifications':specifications,'Price':prices,'Rating':ratings}) 
    df.to_csv(f'../COLLECTED_DATA/{item}.csv', index=False, encoding='utf-8')




# --------------------------------
# Set the items whose details you want to scrape
items = ["laptop", "mobile","iphone"]

# --------------------------------
# Collect the data of each item in the list
for item in items:
    collect_Data(item)