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

#### 院外服務 COUNTRY_CODE = 1 
COUNTRY_CODE = 1

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
        code = maker.code (self.num+1, 
                COUNTRY_CODE, 
                self.start_date, 
                self.end_date
        )
        code.data ()
        process_datadataframe (driver, self.start_date, self.end_date, code.sql, self.num+1)
        time.sleep(1)

def login_chrome ():
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

#### 0 to 7, total: 8
SheetName_1 = ['當月新簽約教會', '打過卡機構', '當月解約教會', '當月新開個案', '當月結案個案', '當月合作教會', '當月認養中個案', '當月有認養個案教會','當月無認養個案教會']
#### 0 to 4, total: 5
SheetName_2 = ['新增教會數', '新增個案數', '合作教會數', '認養個案數', '有認養個案教會數']
SheetName_3 = ['當月認養中個案']
df_dict = {}

### i=1 to 13 
def process_datadataframe (driver, start_date, end_date, sql_code, num):
    '''
        download data 
    '''
    
    global SheetName_1, SheetName_2, df_dict 
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
    if num == 6 or num == 7:
        time.sleep (2)
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
    if num < 9:
        df_dict.update ({SheetName_1[num-1]:dataframe})
#        print (SheetName_1[num-1] + " 下載完成！")
    else:
        num -= 8
        df_dict.update ({SheetName_2[num-1]:dataframe})
#        print (SheetName_2[num-1] + " 下載完成！")
    driver.quit ()

def output (SheetName, month):
    '''
        output data 
    '''

    global df_dict
    if SheetName == SheetName_1:
#        print ("開始輸出")
        date = datetime.datetime.now().strftime("%Y%m%d")
        f_name = "救助處" + month + "月資料_" + date + ".xlsx"
    elif SheetName == SheetName_2:
#        print ("start to output data for PowerBI")
        f_name = "救助處統計" + month + "月.xlsx"
    elif SheetName == SheetName_3:
#        print ("")
        f_name = "個案分析" + month + "月.xlsx"
    f_path = os.getcwd() + os.sep + f_name
    print (f_path)
    with pd.ExcelWriter(f_path, engine='xlsxwriter') as writer:
        for i, sht in enumerate (SheetName):
            df = df_dict[sht]
            df.to_excel (writer, sheet_name=sht, header=True, index=False)

    if SheetName == SheetName_1:
        print ("救助處 " + month + " 月報表已輸出完成！")
    elif SheetName == SheetName_2:
        print ("救助處統計_" + month + " 已輸出完成！")
    elif SheetName == SheetName_3:
        print ("個案分析" + month + " 已輸出完成！")

def process_no_case_church (month):
    '''
        processing df with no_case_church
    '''

    global df_dict
    date = datetime.datetime.now().strftime("%Y%m%d")
    f_name = "救助處" + month + "月資料_" + date + ".xlsx"
    f_path = os.getcwd() + os.sep + f_name
    
    df1 = df_dict['當月合作教會']
    df2 = df_dict['當月有認養個案教會']
    
    #### target = df1 - df2
    alldata = df2['DEPT_ID'].values.tolist()
    mask = ~df1['教會代號'].str.lower().isin([x.lower() for x in alldata])
    
    df = df1[mask]
    df_dict.update({'當月無認養個案教會':df})

def main (start_date, end_date):
    '''
     建立 13 個子執行緒
    '''
    
    threads = []
    start_time = time.time ()
    year, month, day = start_date.split ('/')
    for i in range(13):
        threads.append(MyThread(i, start_date, end_date))
        threads[i].start()
    
    # 等待所有子執行緒結束
    for i in range(13):
        threads[i].join()
    
    process_no_case_church(month)

    print("Done.")
    # 主執行緒繼續執行自己的工作
    threads = []
    SheetName_list = [SheetName_1, SheetName_2, SheetName_3]
    for i in range (3):
        threads.append(threading.Thread (target=output, args=(SheetName_list[i],month)))
        threads[i].start()

    for i in range (3):
        threads[i].join()


    print("--- execution time of Taiwan : %s  ---" % (time.time() - start_time))

if __name__ == '__main__':
    start_date='2020/08/01'
    end_date='2020/08/31'
    main (start_date, end_date)
