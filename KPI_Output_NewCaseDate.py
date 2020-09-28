from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import pandas as pd
import xlrd , os , sys , time 

new_df = []

class department:
    def __init__ (self , city , city_now , case_id , case_name , serviceuser , day1 , day4 , days , total , over30):
        self.city = city 
        self.city_now = city_now 
        self.case_id = case_id
        self.case_name = case_name 
        self.serviceuser = serviceuser
        self.day1 = day1
        self.day4 = day4
        self.days = days
        self.total = total
        self.over30 = over30 

    def make_dataframe (self):
        global new_df
        header = ['目前教會名稱' , '案號' , '個案名稱' , '複審審核人員' , '初審日期' , '決行日期' , '初審至決行天數']
        new_df.append ( pd.concat ([self.city_now , self.case_id , self.case_name , self.serviceuser , self.day1 , self.day4 , self.days] , axis = 1 , names = header))

    def print_result (self):
        print (self.city , ":" , str (self.total - self.over30) + "/" + str (self.total))
    
city_N = user_list1
city_W = user_list2
city_S1 = user_list3
city_S2 = user_list4
city_E1 = user_list5
city_E2 = user_list6

city_dict = { '北區服務中心':city_N , 
              '中區服務中心':city_W ,
              '南區服務中心':city_S1 ,
              '台南服務站':city_S2 , 
              '東區服務中心':city_E1 ,
              '台東服務站':city_E2  }

def make_sql_code (user_id , start_date , end_date):

    sql_code = """select A.DEPT_ID AS '目前教會代號'
, B.DEPT_DESC    AS '目前教會名稱'
, B.region       AS '目前區域'
, D.Department as '目前服務中心'
, A.createDate  AS '開案日'
, A.FAMILY_ID    AS '戶號'
, A.CASE_ID      AS '案號'
, A.CASE_NAME    AS '個案名稱'
, A.BIRTHDAY     AS '個案生日'
, A.CASESTATUS   AS '個案狀態'
, C.USER_NAME    AS '目前個管師'
, G.User_name AS '複審審核人員'
, F.USER_NAME AS '決行人員'
, E.初審日期
, F.決行日期
, DATEDIFF ( day , E.初審日期 , F.決行日期) as '初審至決行天數'
 FROM CASEDATA A, DEPT B, USERFILE C, USERFILE D , 
( select DISTINCT Object_id ,  CONVERT (DATE , Approve_Date ) AS '初審日期'
from workflow 
where app_code = 'casedata'
And workflow_order = '1'
) E , 
( select DISTINCT Object_id ,  CONVERT (DATE , Approve_Date ) AS '初審日期' , User_name , User_id
from workflow 
where app_code = 'casedata'
And workflow_order = '2'
) G , 
( select DISTINCT Object_id ,  CONVERT (DATE , Approve_Date ) AS '決行日期' , User_name , User_id
from workflow 
where app_code = 'casedata'
And workflow_order = '4'
) F
WHERE A.DEPT_ID = B.DEPT_ID
AND B.DEPT_TYPE = '院外服務'
AND B.CASE_SERVICEUSER  = C.USER_ID
AND B.CASE_SUPERVISOR2  = D.USER_ID
and G.user_id in """ + user_id + """
and A.CASESTATUS in ('認養中' , '待配對' , '結案審核' , '結案')
and A.case_id = F.object_id
And E.Object_id = F.Object_id
and G.Object_id = E.Object_id
and A.CreateDate between '""" + start_date + "' AND '" + end_date + """'
order by D.Department , C.USER_NAME , E.初審日期"""
    
    return sql_code 

def login_chrome ():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options , executable_path = ChromeDriverManager().install())
                              
    driver.get(main_url)

    username = driver.find_element_by_name('User_id').send_keys(account)
    password = driver.find_element_by_name('password').send_keys(pwd)
   
    driver.find_element_by_name('LoginBotton').click()
    print ("登入成功！")

    return driver

def process_sql (driver , sql_code):
    
    count = 0
    NofRows = 0

    target_url = 'target_url'

    driver.get (target_url)
################輸入SQL碼後開始查詢###############
        
    driver.switch_to.frame("right")
    driver.find_element_by_name ("sql_cmd").send_keys (sql_code )   
   
    query = driver.find_element_by_name ('result')
    driver.execute_script ("arguments[0].click ();" , query)
    print ("開始查詢！")
    time.sleep (1)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    table_xpath = "//body[@class = 'tool']/table/tbody"
    WebDriverWait (driver , 10).until(EC.visibility_of_element_located ((By.XPATH , table_xpath)))
    print ("已取得資料")
    
    data = driver.find_element_by_xpath("//body[@class = 'tool']/table/tbody")

    #get number of rows
    rows = data.find_elements_by_xpath (".//tr")
    NofRows = (len (rows))
    print ("number of rows : " + str (NofRows))

    print ("資料下載中")
    th = data.text.split ('\n' , 1)
    th = ''.join(th [0]).split (' ')
    trs = data.text.split ('\n')
    j = 0
    list_of_tds = []
    for tr in trs:
        td = tr.split (' ')
        if j != 0:
            if td [0] == 'CC108110':
                td [1:3] = [' '.join (td [1:3])]
            list_of_tds.append (td)
        if j == 0: j += 1
        percent = j/NofRows 
        sys.stdout.write('#'*int(percent*10)+' '*(10-int(percent*10)) +'{:.1%}'.format(percent)+ '\r' )
        sys.stdout.flush()
        j += 1
    dataframe = pd.DataFrame (list_of_tds , columns = th , index = None)
    driver.quit ()

    df_list = []
    df_list.append (dataframe)
    return df_list
        

def count_over_30_days (f , citys):

    global new_df , result_all 
    sht = ['工作表1']
    print(f)
    wb = xlrd.open_workbook (f , on_demand = True)
    departments = {}
    for sht in wb.sheets ():
        df = pd.read_excel(f, sheet_name = sht.name) # "data" are all sheets as a dictionary
            
        print ("服務中心：    " , "達成數/總開案數")
        for city in citys:
            city_now = df[df.複審審核人員.isin (city_dict [city])].目前服務中心
            case_id = df[df.複審審核人員.isin (city_dict [city])].案號
            case_name = df[df.複審審核人員.isin (city_dict [city])].個案名稱
            serviceuser = df[df.複審審核人員.isin (city_dict [city])].複審審核人員 
            day1 = df[df.複審審核人員.isin (city_dict [city])].初審日期
            day4 = df[df.複審審核人員.isin (city_dict [city])].決行日期
            days = df[df.複審審核人員.isin (city_dict [city])].初審至決行天數
            days = pd.to_numeric (days)
            days_over30 = days[days > 30]
            departments.update ( {city : department (city , city_now , case_id , case_name , serviceuser , day1 , day4 , days , len (case_id) , len (days_over30))}  )
            departments [city].make_dataframe()
            departments [city].print_result ()

    list1 = []
    list2 = []
    for dept in departments:
        list1.append (dept)
        list2.append (str (departments[dept].total - departments[dept].over30) + "/" + str (departments[dept].total))
    data = {'服務中心' : list1 ,
            '達成數/總案量': list2}
    final =  pd.DataFrame (data = data , columns = ['服務中心' , '達成數/總案量'] )
    new_df.append (final)

    return new_df 

def output (df_list , f_path , sht_list):

    with pd.ExcelWriter (f_path , engine='xlsxwriter') as writer:
        for i in range (len (df_list)):
            sht_name = sht_list [i]
            df_list [i].to_excel (writer , sheet_name = sht_name , index = False )
    writer.save()


if __name__ == '__main__':

    id_list = []
    citys = ['北區服務中心' , '中區服務中心' , '南區服務中心' , '台南服務站' , '東區服務中心' , '台東服務站']
    sht = ['工作表1']

    print ("請輸入個管師工號：(^D 結束)")
    while True:
        try:
            id_list.append (input ())
        except EOFError:
            print ("開始處理sql_code！")
            break
    user_id = str (tuple (id_list))

    start_date = input ("請輸入查詢起始日期：")
    Y , M , D = start_date.split ('/')
    end_date = input ("請輸入查詢結束日期：")
    Y2 , M2 , D2 = end_date.split ('/')
    sql_code = make_sql_code (user_id , start_date , end_date)

    driver = login_chrome ()
    df = process_sql (driver , sql_code)
    sql_output_f_name = M + "到" + M2 + "月新案審核狀況.xlsx"
    f_path = os.path.join (os.getcwd () , sql_output_f_name)
    output (df , f_path , sht)

    result = count_over_30_days (f_path , citys)
    output_path = os.path.join (os.getcwd () , 'output.xlsx')
    citys.append ('計算結果')
    output (result , output_path , citys)
