# -*- coding: utf-8 -*-
import time
import sys
import re
import csv
from collections import defaultdict
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import itertools
import os
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

with open('links.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["Date","Url"])


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\Users\Krsto\Desktop\chromedriver.exe")
browser.wait = WebDriverWait(browser, 10)
while True:
    print 'Please enter date range (GGGG/MM/DD-GGGG/MM/DD):'
    date_range=raw_input()

    try:
        year=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(1)
        month=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(2)
        day=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(3)
        year1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(4)
        month1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(5)
        day1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(6)
        data_for_csv_name=year+' '+month+' '+day+'-'+day1
    except:
        print 'Please enter correct date range!'
        continue

    if month!=month1 or year!=year1:
        print 'Please enter the same year and month!'
        continue

    if month=='01' or month=='03' or month=='05' or month=='07' or month=='10' or month=='12':
        day_all='31'
    elif month=='04' or month=='06' or month=='08' or month=='09' or month=='11':
        day_all='30'
    elif month=='02' and ((int(year)%4==0 and int(year)%100!=0) or int(year)%400==0):
        day_all='29'
    elif month=='02':
        day_all='28'
    else:
        print 'Please enter correct date!'
        continue
    if int(day)>int(day_all) or int(day1)>int(day_all) or int(day)>int(day1):
        print 'Please enter correct date!'
        continue
    else:
        break


date_start=year+'-'+month+'-01'
date_end=year+'-'+month+'-'+day_all

for i in range(int(day),int(day1)+1):
    d=i
    if d<10:
        d='0'+str(d)
    date=year+'-'+month+'-'+str(d)
    browser.get('https://finance.yahoo.com/calendar/earnings?from='+str(date_start)+'&to='+str(date_end)+'&day='+str(date))
    time.sleep(5)

    c = 1
    while True:
        for i in range(1,101):
            try:
                link=browser.find_element_by_xpath('//*[@id="fin-cal-table"]/div[2]/div/table/tbody/tr['+str(i)+']/td[2]/a').get_attribute('href')
            except:
                break

            print c
            print link
            c=c+1

            with open('links.csv', 'ab') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow([date,link])
        try:
            next1=browser.find_element_by_xpath('//*[@id="fin-cal-table"]/div[2]/div[2]/button[3]').get_attribute('outerHTML')
            if 'disabled' in next1:
                break
            next=browser.find_element_by_xpath('//*[@id="fin-cal-table"]/div[2]/div[2]/button[3]').click()
            time.sleep(4)
        except:
            break

columns = defaultdict(list)
with open('links.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            columns[k].append(v)

dates = columns["Date"]
urls = columns["Url"]

with open('finance_yahoo_'+data_for_csv_name+'.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["Date","Company","Symbol","Current Day Stock Value","Actual $ Day Change","Percentage Day Change","Previous Close","Open","Bid","Ask","Day's Range","52 Week Range","Volume","Avg. Volume",
                 "Market Cap","Beta (3Y Monthly)","PE Ratio (TTM)","EPS (TTM)","Earnings Date","Forward Dividend & Yield","Ex-Dividend Date","1y Target Est","Url"])

c=1
for date,url in itertools.izip(dates,urls):
    browser.get(url)
    time.sleep(3)
    while True:
        try:
            name=browser.find_element_by_css_selector('h1').text
            company_name=re.search('(.*)([(].*[)])',name).group(1)
            break
        except:
            browser.get(url)
            time.sleep(3)

    symbol=re.search('(.*) [(](.*)[)]',name).group(2)

    current_day_stock_value=browser.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').text
    number2=browser.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]').text
    actual_day_change=re.search('(.*)[(](.*)[)]',number2).group(1)
    percentage_day_change=re.search('(.*)[(](.*)[)]',number2).group(2)


    table=browser.find_element_by_xpath('//*[@id="quote-summary"]').text

    previous_close=re.search('Previous Close (.*)',table).group(1)
    open1=re.search('Open (.*)',table).group(1)
    bid=re.search('Bid (.*)',table).group(1)
    ask=re.search('Ask (.*)',table).group(1)
    days_range=re.search('Day\'s Range (.*)',table).group(1)
    week_range_52=re.search('52 Week Range (.*)',table).group(1)
    volume=re.search('Volume (.*)',table).group(1)
    avg_volume=re.search('Avg. Volume (.*)',table).group(1)

    market_cap=re.search('Market Cap (.*)',table).group(1)
    beta_3y_monthly=re.search('Beta [(]3Y Monthly[)] (.*)',table).group(1)
    pe_ratio_ttm=re.search('PE Ratio [(]TTM[)] (.*)',table).group(1)
    eps_ttm=re.search('EPS [(]TTM[)] (.*)',table).group(1)
    earnings_date=re.search('Earnings Date (.*)',table).group(1)
    forward_dividend_yield=re.search('Forward Dividend [&] Yield (.*)',table).group(1)
    ex_dividend_date=re.search('Ex[-]Dividend Date (.*)',table).group(1)
    target_est_1y=re.search('1y Target Est (.*)',table).group(1)

    print c
    print date
    print company_name
    print symbol
    print '------------'
    print current_day_stock_value
    print actual_day_change
    print percentage_day_change
    print '------------'
    print previous_close
    print open1
    print bid
    print ask
    print days_range
    print week_range_52
    print volume
    print avg_volume
    print '------------'
    print market_cap
    print beta_3y_monthly
    print pe_ratio_ttm
    print eps_ttm
    print earnings_date
    print forward_dividend_yield
    print ex_dividend_date
    print target_est_1y

    print url
    c+=1

    with open('finance_yahoo_'+data_for_csv_name+'.csv', 'ab') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([date,company_name,symbol,current_day_stock_value,actual_day_change,percentage_day_change,previous_close,open1,bid,ask,days_range,week_range_52,volume,avg_volume,
                     market_cap,beta_3y_monthly,pe_ratio_ttm,eps_ttm,earnings_date,forward_dividend_yield,ex_dividend_date,target_est_1y,url])

os.remove("links.csv")
browser.quit()
