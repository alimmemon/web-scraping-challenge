#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from splinter import Browser
from selenium import webdriver
import splinter
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs


# In[2]:


#get_ipython().system('which chromedriver')


# In[3]:

def scrape():
    # URL of page to be scraped
    url= 'https://mars.nasa.gov/news/'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    time.sleep(2)

    html= browser.html
    news_parser = BeautifulSoup(html, 'html.parser')


    # In[4]:


    ### NASA Mars News

    var= news_parser.find_all('div', class_='content_title')
    var2= news_parser.find_all('div', class_='article_teaser_body')


    article_title=var[1].text
    # article_title
    news_para= var2[0].text
    news_para


    # In[5]:


    ### JPL Mars Space Images - Featured Image retrieval process 
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    url2= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url2)

    time.sleep(1)
    full_image= browser.find_by_id('full_image')
    full_image.click()

    time.sleep(1)
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info=browser.find_link_by_partial_text('more info')
    more_info.click()


    html=browser.html
    var4= BeautifulSoup(html, 'html.parser')


    main_image= var4.select_one('figure.lede a img').get('src')
    main_image



    # In[6]:


    # Adds the image url to the featured_image var
    featured_image_url= f'https://www.jpl.nasa.gov{main_image}'
    print(featured_image_url)


    # In[7]:


    # ### Mars Weather looks and prints out the top tweet.

    import tweepy 
    from credentials import apikey
    from credentials import apisecret

    import pprint


    auth = tweepy.OAuthHandler(apikey, apisecret)
    auth.set_access_token('1169515964-UJ9zn1reclLmBIpFDhJjco0mTgoKP69bug6kWpL'
    ,'P3TZC9S7ndFwwAfYwzZdZGAMrcqGkYLCsRlxD8NQ8H6QL')

    api = tweepy.API(auth)
    public_tweets = api.get_user('MarsWxReport')


    pp = pprint.PrettyPrinter(indent=4)
    mars_weather=public_tweets._json['status']['text']
   


    # In[8]:


    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(public_tweets._json)


    # In[9]:


    ### Mars Facts goes to the page, then prints the table for us.
    url4= 'https://space-facts.com/mars/'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url4)
    time.sleep(2)
    table= pd.read_html(url4)
    table_df = pd.DataFrame(data=table[1])
    mars_facts=table_df.to_html()


    # In[10]:


    ### Mars Hemispheres

    website= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(website)

    # soup = BeautifulSoup(website.text, 'lxml')
    hemisphere_image_urls = []
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        # Navigate Backwards
        browser.back()


    # In[11]:



    


    mars_scrape_data = {
        "aritcle_title": article_title,
        "news_para": news_para,
        "main_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    return mars_scrape_data


# In[ ]:




