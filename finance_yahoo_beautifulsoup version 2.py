# -*- coding: utf-8 -*-
import time
from importlib import reload
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

#reload(sys)
#sys.setdefaultencoding('utf-8')

with open('links.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["Date","Url"])

while True:
    print ('Please enter date range (GGGG/MM/DD-GGGG/MM/DD):')
    date_range=input()

    try:
        year=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(1)
        month=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(2)
        day=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(3)
        year1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(4)
        month1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(5)
        day1=re.search('(.*)/(.*)/(.*)-(.*)/(.*)/(.*)',date_range).group(6)
        data_for_csv_name=date_range
    except:
        print ('Please enter correct date range!')
        continue

    if year!=year1:
        print ('Please enter correct date range!')
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
        print ('Please enter correct date range!')
        continue

    if month1=='01' or month1=='03' or month1=='05' or month1=='07' or month1=='10' or month1=='12':
        day_all1='31'
    elif month1=='04' or month1=='06' or month1=='08' or month1=='09' or month1=='11':
        day_all1='30'
    elif month1=='02' and ((int(year)%4==0 and int(year)%100!=0) or int(year)%400==0):
        day_all1='29'
    elif month1=='02':
        day_all1='28'
    else:
        print ('Please enter correct date range!')
        continue


    if int(day)>int(day_all) or int(day1)>int(day_all1):
        print ('Please enter correct date range!')
        continue
    else:
        break


date_start=year+'-'+month+'-01'
date_end=year+'-'+month1+'-'+day_all1

c = 1
while True:

    if len(month)==1:
        month='0'+month
    if month=='01' or month=='03' or month=='05' or month=='07' or month=='10' or month=='12':
        day_all='31'
    elif month=='04' or month=='06' or month=='08' or month=='09' or month=='11':
        day_all='30'
    elif month=='02' and ((int(year)%4==0 and int(year)%100!=0) or int(year)%400==0):
        day_all='29'
    elif month=='02':
        day_all='28'
    if month==month1:
        for i in range(int(day),int(day1)+1): #get links per day
            d=i
            if d<10:
                d='0'+str(d)
            date=year+'-'+month+'-'+str(d)

            url='https://finance.yahoo.com/calendar/earnings?from='+str(date_start)+'&to='+str(date_end)+'&day='+str(date)
            page = requests.get(url)
            soup = BeautifulSoup(page.text,'lxml')

            more_for_100=100

            while True:
                if len(soup.find_all("a", class_="Fw(600)"))==0:
                    break
                for url2 in soup.find_all("a", class_="Fw(600)"):
                    link='https://finance.yahoo.com/'+url2.get('href')
                    print (c)
                    print (link)
                    c+=1
                    with open('links.csv', 'a', newline='') as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow([date,link])

                page = requests.get(url+'&offset='+str(more_for_100)+'&size=100')
                soup = BeautifulSoup(page.text,'lxml')
                more_for_100+=100
        break
    else:
        for i in range(int(day),int(day_all)+1): #get links per day
            d=i
            if d<10:
                d='0'+str(d)
            date=year+'-'+month+'-'+str(d)

            url='https://finance.yahoo.com/calendar/earnings?from='+str(date_start)+'&to='+str(date_end)+'&day='+str(date)
            page = requests.get(url)
            soup = BeautifulSoup(page.text,'lxml')

            more_for_100=100

            while True:
                if len(soup.find_all("a", class_="Fw(600)"))==0:
                    break
                for url2 in soup.find_all("a", class_="Fw(600)"):
                    link='https://finance.yahoo.com/'+url2.get('href')
                    print (c)
                    print (link)
                    c+=1
                    with open('links.csv', 'a', newline='') as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow([date,link])

                page = requests.get(url+'&offset='+str(more_for_100)+'&size=100')
                soup = BeautifulSoup(page.text,'lxml')
                more_for_100+=100
        day='01'
        month=str(int(month)+1)

columns = defaultdict(list)
with open('links.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            columns[k].append(v)

dates = columns["Date"]
urls = columns["Url"]
data_for_csv_name=data_for_csv_name.replace('/','.')
with open('finance_yahoo '+data_for_csv_name+'.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["Date","Company","Symbol","Current Day Stock Value","Actual $ Day Change","Percentage Day Change","Previous Close","Open","Bid","Ask","Day's Range","52 Week Range","Volume","Avg. Volume",
                 "Market Cap","Beta (3Y Monthly)","PE Ratio (TTM)","EPS (TTM)","Earnings Date","Forward Dividend & Yield","Ex-Dividend Date","1y Target Est","Url"])

c=1
for date,url in zip(dates,urls): #get data from link

    page = requests.get(url)
    soup = BeautifulSoup(page.text,'lxml',from_encoding="utf-8")
    #print (soup.prettify())
    try:
        name=soup.find('h1',class_='D(ib) Fz(16px) Lh(18px)').text
    except:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text,'lxml',from_encoding="iso-8859-8")
            name=soup.find('h1',class_='D(ib) Fz(16px) Lh(18px)').text
        except:
            continue

    company_name=re.search('(.*?) - (.*)',name).group(2)
    symbol=re.search('(.*?) - (.*)',name).group(1)

    current_day_stock_value=soup.find(class_='Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)').text

    try:
        number2=soup.find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($dataRed)').text
    except:
        try:
            number2=soup.find(class_='Trsdu(0.3s) Fw(500) Fz(14px) C($dataGreen)').text
        except:
            number2=soup.find(class_='Trsdu(0.3s) Fw(500) Fz(14px)').text
    try:
        actual_day_change=re.search('(.*)[(](.*)[)]',number2).group(1)
        percentage_day_change=re.search('(.*)[(](.*)[)]',number2).group(2)
    except:
        actual_day_change=''
        percentage_day_change=''

    previous_close=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "PREV_CLOSE-value"}).text
    open1=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "OPEN-value"}).text
    bid=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "BID-value"}).text
    ask=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "ASK-value"}).text
    days_range=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "DAYS_RANGE-value"}).text
    week_range_52=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "FIFTY_TWO_WK_RANGE-value"}).text
    volume=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "TD_VOLUME-value"}).text
    avg_volume=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "AVERAGE_VOLUME_3MONTH-value"}).text

    market_cap=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "MARKET_CAP-value"}).text
    beta_3y_monthly=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "BETA_3Y-value"}).text
    pe_ratio_ttm=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "PE_RATIO-value"}).text
    eps_ttm=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "EPS_RATIO-value"}).text
    earnings_date=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "EARNINGS_DATE-value"}).text
    forward_dividend_yield=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "DIVIDEND_AND_YIELD-value"}).text
    ex_dividend_date=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "EX_DIVIDEND_DATE-value"}).text
    target_est_1y=soup.find('td',class_='Ta(end) Fw(600) Lh(14px)',attrs={"data-test" : "ONE_YEAR_TARGET_PRICE-value"}).text


    print (c)
    print (date)
    print (company_name)
    #print symbol
    #print '------------'
    #print current_day_stock_value
    #print actual_day_change
    #print percentage_day_change
    #print '------------'
    #print previous_close
    #print open1
    #print bid
    #print ask
    #print days_range
    #print week_range_52
    #print volume
    #print avg_volume
    #print '------------'
    #print market_cap
    #print beta_3y_monthly
    #print pe_ratio_ttm
    #print eps_ttm
    #print earnings_date
    #print forward_dividend_yield
    #print ex_dividend_date
    #print target_est_1y

    #print url
    c+=1

    with open('finance_yahoo '+data_for_csv_name+'.csv', 'a', newline='',encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([date,company_name,symbol,current_day_stock_value,actual_day_change,percentage_day_change,previous_close,open1,bid,ask,days_range,week_range_52,volume,avg_volume,
                     market_cap,beta_3y_monthly,pe_ratio_ttm,eps_ttm,earnings_date,forward_dividend_yield,ex_dividend_date,target_est_1y,url])

os.remove("links.csv")