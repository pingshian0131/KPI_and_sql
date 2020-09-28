class code ():
    def __init__ (self, num, country, start_date, end_date):
        self.num=num
        self.country=country
        self.start_date=start_date
        self.end_date=end_date 
        self.sql=None 

    def data (self):
    
        if self.country == 1:
        ###################新教會合約
        
            sql_code_1 = """select B.DEPT_ID AS '教會代號'
        , F.DEPT_DESC          AS '教會名稱'
        , F.region             AS '區域'
        , B.CONTRACT_BEGINDATE AS '合約起始日'
        , B.CONTRACT_ENDDATE   AS '合約到期日'
        , A.APPROVE_DATE       AS '決行日'
        , B.AGENT_NAME         AS '專管員'
        , E.USER_NAME    AS '個案管理師'
        , C.USER_NAME    AS '社區工作師'
        , D.USER_NAME    AS '組長'
        FROM WORKFLOW A, CONTRACT B , DEPT F, USERFILE C, USERFILE D, USERFILE E
        WHERE A.OBJECT_ID = B.CONTRACT_ID 
        AND A.APP_CODE = 'CONTRACT' 
        AND A.WORKFLOW_TYPE = '決行'
        AND CONVERT(CHAR(8),A.APPROVE_DATE,112) BETWEEN '""" + self.start_date.replace ('/','') + "' AND '" + self.end_date.replace ('/','') + """' 
        AND B.DEPT_ID = F.DEPT_ID
        AND B.Renew IS NULL
        AND F.DEPT_TYPE = '院外服務'
        AND F.CASE_SERVICEUSER2 = C.USER_ID 
        AND F.CASE_SUPERVISOR2  = D.USER_ID 
        AND F.CASE_SERVICEUSER  = E.USER_ID
        ORDER BY B.CONTRACT_BEGINDATE """
        
        ###################打過卡教會
          
            sql_code_2 = """select A.DEPT_ID AS '打卡教會代號'
        , A.DEPT_DESC    AS '教會名稱'
        , A.region       AS '區域'
        , D.USER_NAME    AS '個案管理師'
        , C.USER_NAME    AS '社區工作師' 
        FROM DEPT A, 
        (select distinct 
        F.dept_id 
        from services F
        where F.longitude is not null) B, USERFILE C, USERFILE D
        WHERE A.DEPT_ID = B.DEPT_ID
        AND A.CASE_SERVICEUSER2 = C.USER_ID 
        AND A.CASE_SERVICEUSER  = D.USER_ID
        ORDER BY A.DEPT_ID"""
        
        ###################新解約教會
        
            sql_code_3 = """select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , A.CONTRACT_BeginDate AS '合約起始日'
        , A.CONTRACT_EndDate   AS '合約到期日'
        , A.Quit_Date AS '解約日'
        , A.AGENT_NAME   AS '專管員'
        , C.USER_NAME    AS '社區工作師'
        , D.USER_NAME    AS '組長'
        FROM CONTRACT A, DEPT B, USERFILE C, USERFILE D
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND CONVERT(CHAR(8),A.Quit_Date,112) BETWEEN """ + self.start_date.replace ('/','') + " AND " + self.end_date.replace ('/','') + """ 
        AND B.CASE_SERVICEUSER2 = C.USER_ID 
        AND B.CASE_SUPERVISOR2  = D.USER_ID """
        ####################新個案
        
            sql_code_4 = """select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , A.createDate  AS '開案日'
        , A.FAMILY_ID    AS '戶號'
        , A.CASE_ID      AS '案號'
        , A.CASE_NAME    AS '個案名稱'
        , A.BIRTHDAY     AS '個案生日'
        , A.CASESTATUS   AS '個案狀態'
        , C.USER_NAME    AS '個案管理師'
        , D.USER_NAME    AS '組長'
         FROM CASEDATA A, DEPT B, USERFILE C, USERFILE D
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND CONVERT(CHAR(8),A.CREATEDate,112) BETWEEN """ + self.start_date.replace ('/','') + " AND " + self.end_date.replace ('/','') + """ 
        AND A.CASESTATUS IN ('待配對','認養中')
        AND B.CASE_SERVICEUSER  = C.USER_ID
        AND B.CASE_SUPERVISOR2  = D.USER_ID """
        
        ###################新結案個案
        
            sql_code_5 = """select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , A.CLOSEDATE    AS '結案日'
        , A.FAMILY_ID    AS '戶號'
        , A.CASE_ID      AS '案號'
        , A.CASE_NAME    AS '個案名稱'
        , A.BIRTHDAY     AS '個案生日'
        , A.CASESTATUS   AS '個案狀態'
        , C.USER_NAME    AS '個案管理師'
        , D.USER_NAME    AS '組長'
         FROM CASEDATA A, DEPT B, USERFILE C, USERFILE D
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND CONVERT(CHAR(8),A.CLOSEDate,112) BETWEEN """ + self.start_date.replace ('/','') + " AND " + self.end_date.replace ('/','') + """ 
        AND B.CASE_SERVICEUSER  = C.USER_ID
        AND B.CASE_SUPERVISOR2  = D.USER_ID """
        
        #####################當月合作教會
        
            sql_code_6 = """select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , D.DEPARTMENT   AS '服務中心'
        , A.CONTRACT_BeginDate AS '合約起始日'
        , A.CONTRACT_EndDate AS   '合約到期日'
        , F.APPROVE_DATE    AS '決行日'
        , A.CONTRACT_STATUS AS '合約狀態'
        , A.AGENT_NAME   AS '專管員'
        , E.USER_NAME    AS '個案管理師'
        , C.USER_NAME    AS '社區工作師'
        , D.USER_NAME    AS '組長'
         FROM CONTRACT A, DEPT B, USERFILE C, USERFILE D, USERFILE E, WORKFLOW F
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND A.QUIT_DATE is null
        AND CONVERT(CHAR(8),A.CONTRACT_EndDate,112) = '20991231' 
        AND A.CONTRACT_STATUS IN('已通過')
        AND B.CASE_SERVICEUSER2 = C.USER_ID 
        AND B.CASE_SUPERVISOR2  = D.USER_ID 
        AND B.CASE_SERVICEUSER  = E.USER_ID
        AND A.CONTRACT_ID = F.OBJECT_ID  
        AND F.APP_CODE = 'CONTRACT'
        AND CONVERT(CHAR(8),F.APPROVE_DATE,112) <= """ + self.end_date.replace ('/','') + """
        and F.workflow_type = '決行'
        AND F.APPROVED = '已核准'
        UNION
        select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , D.DEPARTMENT   AS '服務中心'
        , A.CONTRACT_BeginDate AS '合約起始日'
        , A.CONTRACT_EndDate AS   '合約到期日'
        , F.APPROVE_DATE    AS '決行日'
        , A.CONTRACT_STATUS AS '合約狀態'
        , A.AGENT_NAME   AS '專管員'
        , E.USER_NAME    AS '個案管理師'
        , C.USER_NAME    AS '社區工作師'
        , D.USER_NAME    AS '組長'
        FROM CONTRACT A, DEPT B, USERFILE C, USERFILE D, USERFILE E, WORKFLOW F
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND A.QUIT_DATE is null
        AND CONVERT(CHAR(8),A.CONTRACT_EndDate,112) = '20991231' 
        AND A.CONTRACT_STATUS IN ('已續約')
        AND B.CASE_SERVICEUSER2 = C.USER_ID 
        AND B.CASE_SUPERVISOR2  = D.USER_ID 
        AND B.CASE_SERVICEUSER  = E.USER_ID
        AND A.CONTRACT_ID = F.OBJECT_ID  
        AND F.APP_CODE = 'CONTRACT'
        AND CONVERT(CHAR(8),F.APPROVE_DATE,112) <= """ + self.end_date.replace ('/','') + """
        and F.workflow_type = '決行'
        AND F.APPROVED = '已核准'
        and A.DEPT_ID not in
        ( select A.DEPT_ID AS '教會代號'
         FROM CONTRACT A, DEPT B, USERFILE C, USERFILE D, USERFILE E, WORKFLOW F
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND A.QUIT_DATE is null
        AND CONVERT(CHAR(8),A.CONTRACT_EndDate,112) = '20991231' 
        AND A.CONTRACT_STATUS IN ('已通過')
        AND B.CASE_SERVICEUSER2 = C.USER_ID 
        AND B.CASE_SUPERVISOR2  = D.USER_ID 
        AND B.CASE_SERVICEUSER  = E.USER_ID
        AND A.CONTRACT_ID = F.OBJECT_ID  
        AND F.APP_CODE = 'CONTRACT'
        AND CONVERT(CHAR(8),F.APPROVE_DATE,112) <= """ + self.end_date.replace ('/','') + """
        and F.workflow_type = '決行'
        AND F.APPROVED = '已核准' )
        ORDER BY A.DEPT_ID"""
        
        ####################當月認養個案清冊
        
            sql_code_7 = """select A.DEPT_ID AS '教會代號'
        , B.DEPT_DESC    AS '教會名稱'
        , B.region       AS '區域'
        , D.DEPARTMENT   AS '服務中心'
        , A.CREATEDate   AS '開案日'
        , A.FAMILY_ID    AS '戶號'
        , A.CASE_ID      AS '案號'
        , A.CASE_NAME    AS '個案名稱'
        , A.BIRTHDAY     AS '個案生日'
        , A.SEX          AS '個案性別'
        , FLOOR(DATEDIFF(DY,A.Birthday,GETDATE())/365.25) AS '個案年齡'
        , A.Welfare AS '個案福利狀況'
        , A.School_type + A.CaseEducation + A.Student_type AS '個案學籍'
        , A.IsOriginal AS '個案身份別'
        , A.Disabled_Desc + A.degree AS '個案障別'
        , A.CASESTATUS   AS '個案狀態'
        , C.USER_NAME    AS '個案管理師'
        , E.USER_NAME    AS '社區工作師'
        , D.USER_NAME    AS '組長'
        FROM CASEDATA A, DEPT B, USERFILE C, USERFILE D, USERFILE E
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND (
            (A.CASESTATUS IN ('待配對','認養中', '結案審核') AND (CONVERT(CHAR(8),A.CREATEDate,112) <= """ + self.end_date.replace ('/','') + """ OR A.CREATEDate IS NULL)) 
            OR (A.CASESTATUS IN ('結案') AND CONVERT(CHAR(8),A.CLOSEDate,112) > """ + self.end_date.replace ('/','') + """ )
            )
        AND B.CASE_SERVICEUSER  = C.USER_ID
        AND B.CASE_SUPERVISOR2  = D.USER_ID
        AND B.CASE_SERVICEUSER2 = E.USER_ID 
        ORDER BY A.dept_id,D.USER_NAME, C.USER_NAME"""
        
        ###################簽約教會有認養個案
        
            sql_code_8 = """select A.DEPT_ID, COUNT(A.CASE_ID) AS CNT_CASE 
        FROM CASEDATA A, DEPT B
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND B.DEPT_DESC NOT LIKE '自行%'
        AND A.CASESTATUS IN ('待配對','認養中', '結案審核')
        GROUP BY A.DEPT_ID
        ORDER BY A.DEPT_ID """
        
            
        ###################各區當月新教會數
        
            sql_code_9 = """select C.DEPARTMENT     AS '服務中心'
        , COUNT(B.DEPT_ID)      AS '新簽約教會數'
        FROM WORKFLOW A, CONTRACT B , DEPT F, USERFILE C,
        (SELECT DEPT_ID, COUNT(CONTRACT_ID) AS CONTRACTN FROM CONTRACT GROUP BY DEPT_ID) G
        WHERE A.OBJECT_ID = B.CONTRACT_ID 
        AND A.APP_CODE = 'CONTRACT' 
        AND A.WORKFLOW_TYPE = '決行'
        AND CONVERT(CHAR(8),A.APPROVE_DATE,112) BETWEEN """ + self.start_date.replace ('/','') + """ AND  """ + self.end_date.replace ('/','') + """
        AND B.DEPT_ID = F.DEPT_ID
        AND B.DEPT_ID = G.DEPT_ID 
        AND G.CONTRACTN = 1
        AND F.DEPT_TYPE = '院外服務'
        AND F.CASE_SUPERVISOR2  = C.USER_ID 
        GROUP BY C.DEPARTMENT"""
        
            
        ###################各區當月新個案數
        
            sql_code_10 = """select 
        C.department   AS  '服務中心'
        , COUNT(A.CASE_ID) AS '新個案數量'
        FROM CASEDATA A, DEPT B, USERFILE C
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND CONVERT(CHAR(8),A.CREATEDate,112) BETWEEN """ + self.start_date.replace ('/','') + """ AND  """ + self.end_date.replace ('/','') + """ 
        AND A.CASESTATUS IN ('待配對','認養中')
        AND B.CASE_SUPERVISOR2  = C.USER_ID
        GROUP BY C.department """
        
            
        ###################各區簽約教會總數
        
            sql_code_11 = """select C.DEPARTMENT  AS  '服務中心'
        , COUNT(A.DEPT_ID) AS '簽約教會數'
         FROM CONTRACT A, DEPT B, USERFILE C, WORKFLOW F
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND A.QUIT_DATE is null
        AND CONVERT(CHAR(8),A.CONTRACT_EndDate,112) = '20991231' 
        AND A.CONTRACT_STATUS IN('已通過')
        AND B.CASE_SUPERVISOR2 = C.USER_ID 
        AND A.CONTRACT_ID = F.OBJECT_ID  
        AND F.APP_CODE = 'CONTRACT'
        AND CONVERT(CHAR(8),F.APPROVE_DATE,112) <= """ + self.end_date.replace ('/','')  + """
        and F.workflow_type = '決行'
        AND F.APPROVED = '已核准'
        GROUP BY C.DEPARTMENT"""
        
        
        ####################各區當月在案數
        
            sql_code_12 = """select C.department   AS  '服務中心'
        , COUNT(A.CASE_ID) AS '個案數量'
         FROM CASEDATA A, DEPT B, USERFILE C
        WHERE A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND A.CASESTATUS IN ('待配對','認養中', '結案審核')
        AND B.CASE_SUPERVISOR2  = C.USER_ID
        AND (CONVERT(CHAR(8),A.CREATEDate,112) <= """ + self.end_date.replace ('/','') + """ OR A.CREATEDate IS NULL)
        GROUP BY C.DEPARTMENT"""
        
        
        ###################有認養個案教會數
        
            sql_code_13 = """select C.DEPARTMENT  AS  '服務中心' 
        , COUNT(distinct A.DEPT_ID)   AS  '有認養個案教會數' 
        FROM CASEDATA A, DEPT B,  USERFILE C
        WHERE CASESTATUS IN ('待配對','認養中', '結案審核')
        AND A.DEPT_ID = B.DEPT_ID
        AND B.DEPT_TYPE = '院外服務'
        AND B.CASE_SUPERVISOR2 = C.USER_ID 
        AND (CONVERT(CHAR(8),A.CREATEDate,112) <= """ + self.end_date.replace ('/','')  + """ OR A.CREATEDate IS NULL)
        GROUP BY C.DEPARTMENT"""
        
            dict_num = { 1:sql_code_1, 
                2:sql_code_2, 
                3:sql_code_3, 
                4:sql_code_4, 
                5:sql_code_5, 
                6:sql_code_6, 
                7:sql_code_7, 
                8:sql_code_8, 
                9:sql_code_9, 
                10:sql_code_10, 
                11:sql_code_11, 
                12:sql_code_12, 
                13:sql_code_13, 
            }
        else:
            ################### 當月新開個案  
            sql_code_1 = """select 
        B.region AS '區域' , 
        B.dept_desc as '服務單位' , 
        A.case_id as '案號' , 
        A.case_name as '案主姓名' , 
        A.sex AS '性別' , 
        A.Birthday AS '生日' ,
        A.School_name AS '學校名稱' ,
        A.CaseEducation AS '學制' ,
        A.SchoolClass AS '年級' ,
        A.ApplyDate AS '申請日期' ,
        A.CreateDate AS '開案日期' ,
        A.CloseDate as '結案日期' ,
        A.CaseStatus as '個案狀態' , 
        A.Update_status as '更新狀態' ,
        F.user_name AS '社工'
        from casedata A , dept B , userfile F
        where B.dept_id = A.dept_id
        and A.casestatus in ('認養中' , '待配對' , '結案審核')
        and B.region in ( '尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and B.dept_desc <> 'TA社區'
        and B.Case_Serviceuser = F.user_id
        and A.createDate between '""" + self.start_date + "' AND '" + self.end_date + """'
        order by A.CASE_ID"""
    
        ################### 當月新開個案（含認養人）
            sql_code_2 = """select 
        B.region AS '區域' , 
        B.dept_desc as '服務單位' , 
        A.case_id as '案號' , 
        A.case_name as '案主姓名' , 
        A.sex AS '性別' , 
        A.Birthday AS '生日' ,
        A.School_name AS '學校名稱' ,
        A.CaseEducation AS '學制' ,
        A.SchoolClass AS '年級' ,
        A.ApplyDate AS '申請日期' ,
        A.CreateDate AS '開案日期' ,
        A.CloseDate as '結案日期' ,
        A.CaseStatus as '個案狀態' , 
        A.Update_status as '更新狀態' ,
        E.Donor_name as '認養人姓名' ,
        E.Donor_id as '認養人編號' ,
        D.Adopt_Status AS '認養狀態' ,
        D.Adopt_BeginDate AS '認養日期' ,
        D.Adopt_EndDate AS '終止日期' ,
        F.user_name AS '社工'
        from casedata A , dept B , adopt D , Donor E , userfile F
        where B.dept_id = A.dept_id
        and A.casestatus in ('認養中' , '待配對' , '結案審核')
        and B.region in ( '尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and B.dept_desc <> 'TA社區'
        and A.case_id = D.case_id
        and D.donor_id = E.donor_id
        and B.Case_Serviceuser = F.user_id
        and A.createDate between '""" + self.start_date + "' AND '" + self.end_date + """'
        and (D.Adopt_EndDate is null or D.Adopt_EndDate between '""" + self.start_date + "' AND '" + self.end_date + """' )
        order by A.case_id"""
        
        ################### 當月認養中個案（含認養人資料）
        
            sql_code_3 = """select 
        B.region AS '區域' , 
        B.dept_desc as '服務單位' , 
        A.case_id as '案號' , 
        A.case_name as '案主姓名' , 
        A.sex AS '性別' , 
        A.Birthday AS '生日' ,
        A.School_name AS '學校名稱' ,
        A.CaseEducation AS '學制' ,
        A.SchoolClass AS '年級' ,
        A.ApplyDate AS '申請日期' ,
        A.CreateDate AS '開案日期' ,
        A.CloseDate as '結案日期' ,
        A.CaseStatus as '個案狀態' , 
        A.Update_status as '更新狀態' ,
        E.Donor_name as '認養人姓名' ,
        E.Donor_id as '認養人編號' ,
        D.Adopt_Status AS '認養狀態' ,
        D.Adopt_BeginDate AS '認養日期' ,
        D.Adopt_EndDate AS '終止日期' ,
        F.user_name AS '社工'
        from casedata A , dept B , adopt D , Donor E , userfile F
        where B.dept_id = A.dept_id
        and A.casestatus in ('認養中' , '待配對' , '結案審核')
        and B.region in ( '尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and B.dept_desc <> 'TA社區'
        and A.case_id = D.case_id
        and D.donor_id = E.donor_id
        and B.Case_Serviceuser = F.user_id
        and D.Adopt_EndDate is null
        order by B.region , A.case_id"""
        
        #################### 當月認養中個案
        
            sql_code_4 = """select 
        B.region AS '區域' , 
        B.dept_desc as '服務單位' , 
        A.case_id as '案號' , 
        A.case_name as '案主姓名' , 
        A.sex AS '性別' , 
        A.Birthday AS '生日' ,
        A.School_name AS '學校名稱' ,
        A.CaseEducation AS '學制' ,
        A.SchoolClass AS '年級' ,
        A.ApplyDate AS '申請日期' ,
        A.CreateDate AS '開案日期' ,
        A.CloseDate as '結案日期' ,
        A.CaseStatus as '個案狀態' , 
        A.Update_status as '更新狀態' ,
        F.user_name AS '社工'
        from casedata A , dept B , userfile F
        where B.dept_id = A.dept_id
        and A.casestatus in ('認養中' , '待配對' , '結案審核')
        and B.region in ( '尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and B.dept_desc <> 'TA社區'
        and B.Case_Serviceuser = F.user_id
        order by B.region , A.case_id"""
        
        ################### 認養中個案 認養人終止認養
        
            sql_code_5 = """select 
        B.region AS '區域' , 
        B.dept_desc as '服務單位' , 
        A.case_id as '案號' , 
        A.case_name as '案主姓名' , 
        A.sex AS '性別' , 
        A.Birthday AS '生日' ,
        A.School_name AS '學校名稱' ,
        A.CaseEducation AS '學制' ,
        A.SchoolClass AS '年級' ,
        A.ApplyDate AS '申請日期' ,
        A.CreateDate AS '開案日期' ,
        A.CloseDate as '結案日期' ,
        A.CaseStatus as '個案狀態' , 
        A.Update_status as '更新狀態' ,
        E.Donor_name as '認養人姓名' ,
        E.Donor_id as '認養人編號' ,
        D.Adopt_Status AS '認養狀態' ,
        D.Adopt_BeginDate AS '認養日期' ,
        D.Adopt_EndDate AS '終止日期' ,
        F.user_name AS '社工'
        from casedata A , dept B , adopt D , Donor E , userfile F
        where B.dept_id = A.dept_id
        and A.casestatus in ('認養中' , '待配對' , '結案審核')
        and B.region in ( '尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and B.dept_desc <> 'TA社區'
        and A.case_id = D.case_id
        and D.donor_id = E.donor_id
        and B.Case_Serviceuser = F.user_id
        and D.Adopt_EndDate between '""" + self.start_date + "' AND '" + self.end_date + """'
        order by B.region , A.case_id"""
        
        ##################### 當月結案個案 
        
            sql_code_6 = """select B.region as '區域' ,
        B.dept_desc as '教會', 
        A.case_id as '案號', 
        A.case_name as '案主姓名', 
        A.sex as '性別',
        A.Birthday as '生日', 
        A.School_name as '學校名稱' ,
        A.CaseEducation as '學制',
        A.SchoolClass as '年級', 
        A.ApplyDate as '申請日期', 
        A.CreateDate as '開案日期', 
        A.CaseStatus as '狀態', 
        A.CloseDate as '結案日期',
        A.Update_status as '更新狀態' ,
        E.Donor_name as '認養人姓名' ,
        E.Donor_id as '認養人編號'
        from casedata A , dept B , caseclose C , adopt D , Donor E
        where B.dept_id = A.dept_id
        and A.CloseDate BETWEEN '""" + self.start_date + "' AND '" + self.end_date + """'
        and A.CaseStatus = '結案'
        and B.region in ('尼泊爾' , '巴基斯坦' , '柬埔寨' , '印度')
        and C.case_id = A.case_id
        and A.case_id = D.case_id
        and D.donor_id = E.donor_id
        order by A.CloseDate"""
        
        #################### 社區認養
        
            sql_code_7 = """select 
        E.Donor_Name AS '認養人姓名'
        ,E.Donor_id AS '認養人編號'
        ,D.Adopt_BeginDate AS '認養日期'
        ,D.Adopt_EndDate AS '終止日期'
        ,C.region AS '區域' 
        ,C.dept_desc AS '服務單位'
        ,A.case_id AS '案號' 
        ,A.Case_Name AS '案主姓名'
        ,A.sex AS '性別'
        ,A.Birthday AS '生日'
        ,A.School_name AS '學校名稱'
        ,A.CaseEducation AS '學制'
        ,A.SchoolClass AS '年級'
        ,A.ApplyDate AS '申請日期' 
        ,A.CreateDate AS '開案日期' 
        ,D.狀態 
        ,A.closeDate AS '結案日期'
        ,A.Update_Status '更新狀態'
        ,F.user_name AS '社工'
        from CASEDATA A, DEPT C , 
        (select case_id , DONOR_ID , Adopt_BeginDate , Adopt_EndDate , Adopt_Status AS '狀態'
        from ADOPT
        where Adopt_EndDate is null or Adopt_EndDate between '""" + self.start_date + "' AND '" + self.end_date + """'
        GROUP BY case_id , DONOR_ID , Adopt_Status , Adopt_BeginDate , Adopt_EndDate) D ,
        DONOR E ,userfile F , CodeCity H , (SELECT * FROM CodeCity) G
        WHERE A.dept_id=C.dept_id  and     
             A.case_id=D.case_id  and  
             D.DONOR_ID=E.DONOR_ID  and
             C.Case_Serviceuser=F.user_id  and 
             H.mCode=E.ZipCode and 
             G.mSortValue=E.City and
             C.dept_desc = 'TA社區'
        ORDER BY  E.Donor_Name """
           
        
            dict_num = { 1:sql_code_1 , 
                2:sql_code_2 ,
                3:sql_code_3 ,
                4:sql_code_4 ,
                5:sql_code_5 ,
                6:sql_code_6 ,
                7:sql_code_7 ,
            }

        self.sql = dict_num[self.num]

