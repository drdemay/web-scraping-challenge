#!/usr/bin/env python
# coding: utf-8
	
# ## Collect NASA Mars News
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
import datetime as dt

def scrape_info():
    #create and update the executable path to the chromedrv
    browser = Browser("chrome", executable_path="C:/chromedrv/chromedriver.exe", headless=True)
    news_title, news_text = mars_news(browser)

    # complete scraping and store in the dictionary
    mars = {
        "news_title": news_title,
        "news_text": news_text,
        "featured_image": featured_image(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser)
    }

    browser.quit()
    return mars

# ## Collect Mars news information from Nasa
def mars_news(browser):
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = bs(browser.html, 'html.parser')

    # results are returned as an iterable list
    results = news_soup.find_all("div", class_="slide")
    results


    # Loop through returned results
    for result in results:
    
        # Retrieve the title for each news story and description paragraph
        title = result.find("div", class_="content_title")
        p = result.find("div", class_="rollover_description_inner")
        news_title = title.a.text
        news_text = p.text

        try:
            print("\n-----------------------------\n")
            print(news_title)
            print(news_text)
            
        except AttributeError as e:
            print(e)

        return news_title, news_text

# ## Collect featured image from Nasa
def featured_image(browser):
    # URL for image to collect
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(url)

    #click for full image
    full_image = browser.find_by_id("full_image")
    full_image.click()

    #click for the more info
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()

    # parse results
    img_soup = bs(browser.html, "html.parser")

    featured_image = img_soup.find("img", class_="main_image")["src"]
    featured_image_url = f"{base_url}{featured_image}"

    # add featured URL
    return featured_image_url 

# ## Collect Mars Weather Information from Twitter
def twitter_weather(browser):
    # URL of page to be scraped
    url = "https://twitter.com/marswxreport"
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    weather_soup = bs(browser.html, "html.parser")

    # Find and display text of tweet
    mars_weather = weather_soup.find("div", class_="js-tweet-text-container").text.strip()

    # add Mars weather information to dictionary
    return mars_weather

# ## Gather Mars facts
def mars_facts():
    # We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
    # URL to scrape information from
    url = "https://space-facts.com/mars/"

    # Read the tables on the page
    mars_facts = pd.read_html(url)
    mars_facts

    # Put the Mars facts table specified into a dataframe 
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["0", "1"]

    # Generate HTML tables from the DataFrame.
    html_table = mars_facts_df.to_html(index=False, header=False)
   
    # Strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')

    return html_table

# ## Gather Mars Hemisphere Photos and Information
def mars_hemispheres(browser):
    # URL of page to be scraped
    hemisphere_url = "https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # visit url and determine length for loop
    browser.visit(hemisphere_url)
    time.sleep(2)
    hemisphere_image_urls=[]

    url_links = browser.find_by_css("a.product-item h3")
    url_links

    # Loop through to get hemisphere images and append to list
    for i in range(len(url_links)):
            
        #create dictionary for each hemisphere
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        
        # get title
        hemisphere["title"] = browser.find_by_css("h2.title").text
      
        # find the sample image scrape href
        sample_img = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_img["href"]
        
        #append images 
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()

    return hemisphere_image_urls