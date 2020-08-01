# -*- coding: utf-8 -*-
from underthesea import word_tokenize
import re

import pickle

from sklearn.svm import LinearSVC

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from time import sleep

abbr_dict={
    "ko":"không",
    "hok":"không",
    "hông":"không",
    "mn":"bạn",
    "ae":"bạn",
    "bợn":"bạn",
    "vs":"với",
    "sr":"xin lỗi",
    "help":"giúp",
    "thank":"cảm ơn",
    "thanks":"cảm ơn",
    "cám ơn":"cảm ơn",
    "tks":"cảm ơn",
    "kq":"kết quả",
    "kqua":"kết quả",
    "nhe":"nhé",
    "nhá":"nhé",
    "nha":"nhé",
    "h":"giờ",
    "s":"sao",
    "pls":"",
    "plz":"",
    "me":"mình",
    "mị":"mình",
    "đc":"được",
    "dc":"được",
    "tgian": "thời gian"
}

def replace_abbr(t):
    if t in abbr_dict:
        return abbr_dict[t]
    else:
        return t

def removeConsecutiveDuplicates(S): 
    S = list(S.rstrip()) 
    
    n = len(S)  
    
    if (n < 2) : 
        return S[0]
           
    j = 0
       
    for i in range(n):  
        if (S[j] != S[i]): 
            j += 1
            S[j] = S[i]  
      
    j += 1
    S = S[:j]
    return "".join(S)

def preprocessing(s, show_stepbystep=False):
    if show_stepbystep:
        print("original:")
        print(s)
        print()
    
    # remove 'Xem thêm'
    s = re.sub('Xem thêm', '', s)
    if show_stepbystep:
        print("remove 'Xem thêm':")
        print(s)
        print()

    # convert to lower case
    s = s.lower()
    if show_stepbystep:
        print("lowercase:")
        print(s)
        print()
    
    # abbreviate some names
    s = re.sub('kỹ thuật phần mềm', 'ktpm', s)
    s = re.sub('công nghệ phần mềm', 'cnpm', s)
    s = re.sub('khoa học máy tính', 'khmt', s)
    s = re.sub('hệ thống thông tin', 'httt', s)
    s = re.sub('kỹ thuật máy tính', 'ktmt', s)
    s = re.sub('thương mại điện tử', 'tmđt', s)
    s = re.sub('công nghệ thông tin', 'cntt', s)
    s = re.sub('an toàn thông tin', 'attt', s)
    s = re.sub('công tác sinh viên', 'ctsv', s)
    s = re.sub('ban học tập', 'bht', s)
    if show_stepbystep:
        print("abbreviate faculty name:")
        print(s)
        print()
    
    # remove urls and hashtags
    s = re.sub(r'http\S+', '', s)
    s = re.sub(r'#\S+', '', s)
    if show_stepbystep:
        print('remove urls and hashtags:')
        print(s)
        print()
    
    # remove email address
    s = re.sub(r'\S*@\S*\s?', '', s)
    if show_stepbystep:
        print('remove email addresses:')
        print(s)
        print()
    
    # split into words
    tokens = word_tokenize(s)
    if show_stepbystep:
        print('tokenize:')
        print(tokens)
        print()
    
    # remove punctuation and number
    words = [word for word in tokens if re.sub(r"\s+", "", word).isalpha()]
    if show_stepbystep:
        print('remove punctuation:')
        print(words)
        print()
    
    # remove consecutive duplicates character
    words = [removeConsecutiveDuplicates(word) for word in words]
    if show_stepbystep:
        print('remove consecutive duplicates character:')
        print(words)
        print()
    
    # replace abbreviation of word
    words = [replace_abbr(word) for word in words]
    if show_stepbystep:
        print('replace abbreviation:')
        print(words)
        print()
        
    # replace " " with "_"
    words = [re.sub(r"\s+", "_", word) for word in words]
    if show_stepbystep:
        print('replace space with "_" :')
        print(words)
        print()
    
    # remove single character
    words = [word for word in words if len(word)>1]
    if show_stepbystep:
        print('remove single character:')
        print(words)
        print()
    
    return ' '.join(words)

model_name = 'finalized_model.sav'
vec_name = 'tfidf.pickle'
model = pickle.load(open(model_name, 'rb'))
tfidf = pickle.load(open(vec_name, "rb"))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('chromedriver', options=chrome_options)
K = input("Chọn khóa (vd: K2019): ")
browser.get(f"https://www.facebook.com/groups/UIT.{K}/")

SCROLL_NUM = 5
for i in range(SCROLL_NUM):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    if i%2==0:
      sleep(1)

posts = browser.find_elements_by_xpath("//div[@class='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _7cqq _4-u8']")

print("""Danh mục các chủ đề:
  1. Thông báo các thông báo của trường, của khoa, của các câu lạc bộ, của lớp (thông báo mở lớp); thông báo về học bổng.
  2. Tìm đồ thất lạc: viết về việc thất lạc đồ hoặc tìm thấy đồ thất lạc.
  3. Hỏi đáp, nhờ giúp đỡ (chủ yếu liên quan đến vấn đề cá nhân): hỏi về trường, nhờ điền form khảo sát, nhờ điền form đăng kí mở lớp, bán lại đồ dùng, thiếu tín chỉ,...
  4. Khác: các hoạt động của cơ quan, tổ chức bên ngoài như tuyển dụng, quảng cáo khóa học, chương trình bốc thăm, ngày hội công nghệ, tham quan doanh nghiệp,...; các bài không rõ chủ đề hoặc nội dung không đáng quan tâm.
""")
chosen_class = int(input("Chọn một trong các chủ đề trên: "))
print()
print("Kết quả tìm kiếm:")

i = 1
for post in posts:
    text = post.find_element_by_xpath("./div/div[2]/div[1]/div[3]/div[2]").text
    pred = model.predict(tfidf.transform([preprocessing(text)]))[0]
    if pred == chosen_class:
        print(i)
        datetime = post.find_element_by_xpath("./div/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a/abbr[1]").get_attribute('title')
        print(datetime)

        print(text)
    
        link = post.find_element_by_xpath("./div/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a[1]").get_attribute("href")
        print(f"Link to post: {link}")

        print()
        i += 1

browser.close()
