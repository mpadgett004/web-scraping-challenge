from flask import Flask, render_template, redirect, jsonify
from flask.json import jsonify
from splinter import Browser
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
import time
import numpy as np
import json
from selenium import webdriver

app = Flask(__name__)

def init_browser():
    executable_path = {
        "executable_path": "/usr/local/bin/chromedriver" 
    }
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Mars News
    mars_info = {}
    url = 'https://mars.nasa.gov/news'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    mars_info["news_title"] = soup.find('div', class_='content_title').text
    mars_info["news_p"] = soup.find('div', class_='rollover_description_inner').text

    # Mars Featured Image
    url_feature_image = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url_feature_image)
    featured_response = browser.html
    featured_soup = BeautifulSoup(featured_response, 'html.parser')
    featured_image = featured_soup.find('a', class_="howimg fancybox-thumbs")["src"]
    img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+featured_image

    mars_info["featured_image_url"] = img_url

    # Mars 
    mars_facts_url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(mars_facts_url)
    df = facts_table[0]
    df.columns = ["Facts", "Value"]
    facts_html = df.to_html()
    facts_html = facts_html.replace("\n","")
    mars_info["fact_table"] = facts_html

    # Mars Hemispheres
    hemisphere_image_urls = []

    # Cerberus Hemisphere Enhanced
    cerberus_hemi_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')
    #cerberus_hemi_response = requests.get(cerberus_hemi_url)
    browser.visit(cerberus_hemi_url)
    cerberus_hemi_response = browser.html
    cerberus_hemi_soup = BeautifulSoup(cerberus_hemi_response.text, 'html.parser')
    cerberus_img = cerberus_hemi_soup.find_all('div', class_="wide-image-wrapper")
    
    for img in cerberus_img:
        cerberus_pic = img.find('li')
        cerberus_full_img = cerberus_pic.find('a')['href']
    cerberus_title = cerberus_hemi_soup.find('h2', class_='title').get_text()
    cerberus_hemi = {"Title": cerberus_title, "url": cerberus_full_img}

    # Schiaparelli Hemisphere Enhanced
    schiaparelli_hemi_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')
    #schiaparelli_hemi_response = requests.get(schiaparelli_hemi_url)
    browser.visit(schiaparelli_hemi_url)
    schiaparelli_hemi_response = browser.html
    schiaparelli_hemi_soup = BeautifulSoup(schiaparelli_hemi_response.text, 'html.parser')
    schiaparelli_img = schiaparelli_hemi_soup.find_all('div', class_="wide-image-wrapper")

    for img in schiaparelli_img:
        schiaparelli_pic = img.find('li')
        schiaparelli_full_img = schiaparelli_pic.find('a')['href'] 
    schiaparelli_title = schiaparelli_hemi_soup.find('h2', class_='title').get_text()
    schiaparelli_hemi = {"Title": schiaparelli_title, "url": schiaparelli_full_img}

    # Syrtis Major Hemisphere Enhanced
    syrtis_major_hemi_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')
    #syrtis_major_hemi_response = requests.get(syrtis_major_hemi_url)
    browser.visit(syrtis_major_hemi_url)
    syrtis_major_hemi_response = browser.html
    syrtis_major_hemi_soup = BeautifulSoup(syrtis_major_hemi_response.text, 'html.parser')
    syrtis_major_img = syrtis_major_hemi_soup.find_all('div', class_="wide-image-wrapper")

    for img in syrtis_major_img:
        syrtis_major_pic = img.find('li')
        syrtis_major_full_img = syrtis_major_pic.find('a')['href']
    syrtis_major_title = syrtis_major_hemi_soup.find('h2', class_='title').get_text()
    syrtis_major_hemi = {"Title": syrtis_major_title, "url": syrtis_major_full_img}

    # Valles Marineris Hemisphere Enhanced
    valles_marineris_hemi_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')
    #valles_marineris_hemi_response = requests.get(valles_marineris_hemi_url)
    browser.visit(valles_marineris_hemi_url)
    valles_marineris_hemi_response = browser.html
    valles_marineris_hemi_soup = BeautifulSoup(valles_marineris_hemi_response.text, 'html.parser')
    valles_marineris_img = valles_marineris_hemi_soup.find_all('div', class_="wide-image-wrapper")

    for img in valles_marineris_img:
        valles_marineris_pic = img.find('li')
        valles_marineris_full_img = valles_marineris_pic.find('a')['href']
    valles_marineris_title = valles_marineris_hemi_soup.find('h2', class_='title').get_text()
    valles_marineris_hemi = {"Title": valles_marineris_title, "url": valles_marineris_full_img}

    # Appending the list with the different dictionaries from the different hemispheres 
    hemisphere_image_urls.append(cerberus_hemi)
    hemisphere_image_urls.append(schiaparelli_hemi)
    hemisphere_image_urls.append(syrtis_major_hemi)
    hemisphere_image_urls.append(valles_marineris_hemi)

    mars_info["hemisphere_image"] = hemisphere_image_urls

    return mars_info


