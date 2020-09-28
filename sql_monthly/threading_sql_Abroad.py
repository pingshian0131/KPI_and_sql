from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

import os
#coding:utf-8
import time
import sys
import pandas as pd
import time
import datetime
import re 
import sql_code_maker as maker 

import threading
import time

#### 海外服務 COUNTRY_CODE = 2 
COUNTRY_CODE = 2
SHEET_NUM = 7

# 子執行緒類別
class MyThread(threading.Thread):
    def __init__(self, num, start_date, end_date):
        threading.Thread.__init__(self)
        self.start_date=start_date
        self.end_date=end_date 
        self.num=num

    def run(self):
        print("Thread", self.num)
        driver = login_chrome ()
        code = maker.code (num=self.num+1, 
                country=COUNTRY_CODE, 
                start_date=self.start_date, 
                end_date=self.end_date
        )
        code.data ()
        process_datadataframe (driver, self.start_date, self.end_date, code.sql, self.num+1)
        time.sleep(1)

def login_chrome ():
    '''
        login 
    '''

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options, executable_path = ChromeDriverManager().install())

    driver.get(main_url)

    username = driver.find_element_by_name('User_id').send_keys(account)
    password = driver.find_element_by_name('password').send_keys(pwd)
     
    driver.find_element_by_name('LoginBotton').click()
#    print ("登入成功！")

    return driver 

SheetName = ['當月新開個案' , '當月新開個案（含認養人）' , '當月認養中個案（含認養人資料）' , '當月認養中個案' , '認養中個案_認養人終止認養' , '當月結案個案' , '社區認養']
df_dict = {}

def process_datadataframe (driver, start_date, end_date, sql_code, num):
    '''
        input sql code and download data into dataframe 
    '''
    
    global SheetName, df_dict 

    target_url = 'target_url'

    driver.get (target_url)
#    print (sql_code)
#    print ("SheetName_Index: {}".format (i-1))
    
################輸入SQL碼後開始查詢###############
    
    driver.switch_to.frame("right")
    driver.find_element_by_name ("sql_cmd").send_keys (sql_code )   

    query = driver.find_element_by_name ('result')
    driver.execute_script ("arguments[0].click ();", query)
#    print ("開始查詢！")
    time.sleep (1)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    table_xpath = "//body[@class = 'tool']/table/tbody"
    WebDriverWait (driver, 10).until(EC.visibility_of_element_located ((By.XPATH, table_xpath)))
#    print ("已取得資料")
    
    data = driver.find_element_by_xpath("//body[@class = 'tool']/table/tbody").get_attribute ("innerHTML")
    pattern = r'<th nowrap="">(.*?)</th>'
    head = re.findall (pattern, data)
    
    pattern = r'<tr bgcolor="#FFFFFF" onmouseover="this.bgColor=&quot;#E2F1FF&quot;" onmouseout="this.bgColor=&quot;#FFFFFF&quot;">(.*?)</tr>'
    rows = re.findall (pattern, data)
    
    pattern2 = r'<td>(.*?)</td>'
    result = {}
    a = [[] for i in range (len (head))]
    for row in rows:
        tr = re.findall (pattern2, row)
    #    print (tr)
        for i,col in enumerate (tr):
    #        print (col)
            a[i].append (col)
    for i in range (len (head)):
        result.update ({head[i]:a[i]})
    dataframe = pd.DataFrame (result, columns=head, index=None)
#        print (dataframe)
    df_dict.update ({SheetName[num-1]:dataframe})
#        print (SheetName_2[num-1] + " 下載完成！")
    driver.quit ()

def output (SheetName, month):
    '''
        output result
    '''

    global df_dict
    print ("開始輸出")
    date = datetime.datetime.now().strftime("%Y%m%d")
    f_name = "海外" + month + "月資料_" + date + ".xlsx"
    f_path = os.getcwd() + os.sep + f_name 
    print (f_path)

    with pd.ExcelWriter (f_path, engine='xlsxwriter') as writer:
        for i, sht in enumerate (SheetName):
            df = df_dict[sht]
            df.to_excel (writer, sheet_name=sht, header=True, index=False)
    print ("海外" + month + "月資料已輸出完成！")

def main (start_date, end_date):
    '''
        making 7 threadings
    '''

    threads = []
    start_time = time.time ()
    year, month, day = start_date.split ('/')

    for i in range(SHEET_NUM):
        threads.append(MyThread(i, start_date, end_date))
        threads[i].start()
    
    # 等待所有子執行緒結束
    for i in range(SHEET_NUM):
        threads[i].join()
    
    print("Done.")
    # 主執行緒繼續執行自己的工作
    output (SheetName, month)
    
    print("--- execution time of Abroad : %s  ---" % (time.time() - start_time))

if __name__ == '__main__':
    main (start_date, end_date)
