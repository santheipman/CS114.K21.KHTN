from lxml.html import fromstring
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import csv

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


"""Choose a proxy"""
proxies = get_proxies()
proxy = proxies[0]

webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy": proxy,
    "ftpProxy": proxy,
    "sslProxy": proxy,
    "proxyType": "MANUAL",
}


"""File to save data"""
csv_file = open('posts.csv', 'w')
csv_writer = csv.writer(csv_file)


"""Request the page"""
browser = webdriver.Firefox(executable_path='./geckodriver')
browser.get("https://www.facebook.com/groups/UIT.K2018/")


"""Initialize parameters for scrolling"""
jump_count = 0
running = True
TOTAL_JUMP = 500


"""Scroll down to load posts"""
while running:
    try:
        if jump_count > TOTAL_JUMP:
            break
        jump_count += 1
        print(jump_count)

        scroll_rand = random.randint(1,100)
        # print("rand =", scroll_rand)
        if scroll_rand < 15:
            print("jump 1")
            length = str(scroll_rand*3 + 300)
            browser.execute_script(f"window.scrollBy(0,{length})")            
        elif scroll_rand < 30:
            print("jump 2")
            length = str(scroll_rand*3 + 600)
            browser.execute_script(f"window.scrollBy(0,{length})")
        else:
            print("jump 3 (end)")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep_rand = random.randint(6,11)
        print("sleep :", sleep_rand)
        sleep(sleep_rand)
    except:
        print("Proxy dieee!")
        break


"""Parse post content and save to csv file"""
post_links = browser.find_elements_by_xpath("//div[@class='_5pbx userContent _3576']")
for post in post_links:
    # print(post.text)
    csv_writer.writerow([post.text])
    post_text_list.append(post.text)
    # print()


print(len(post_text_list))
csv_file.close()
browser.close()
