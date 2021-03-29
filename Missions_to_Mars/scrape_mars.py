import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    html = BeautifulSoup(html, 'html.parser')

    title1 = html.find_all('div', class_='content_title')[0].text
    paragraph1 = html.find_all('div', class_='article_teaser_body')[0].text
    
    # JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()
    soup_child = BeautifulSoup(browser.html, 'html.parser')
    featured_image_url = "https://spaceimages-mars.com/" + soup_child.find('img', class_='fancybox-image')['src']

    # Mars Facts
    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['Description', 'Mars','Earth']
    mars_df.set_index('Description', inplace=True)
    html_table_mars = mars_df.to_html().replace('\n', '')
    #print("Hola, hay un error")
    #print(html_table_mars)

    # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemispheres_image_urls = []

    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text

        link_found = browser.links.find_by_partial_text(title)
        link_found.click()
        soup2 = BeautifulSoup(browser.html, 'html.parser')

        download = soup2.find('div', class_='downloads')
        ul = download.find('ul')
        li_list = ul.find_all('li')
        for li in li_list:
            if "Sample" in li.text:
                hemisphere_image_dict = {"title": title, "img_url": url+li.a['href']}
                hemispheres_image_urls.append(hemisphere_image_dict)
        browser.back()
    
    browser.quit()

    mars_dict = {
    "title": title1,
    "paragraph": paragraph1,
    "featured_image_url": featured_image_url,
    "html_table": html_table_mars,
    "hemispheres": hemispheres_image_urls
    }
    return mars_dict   

