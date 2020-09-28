import threading_sql_Abroad as tA 
import threading_sql_Taiwan as tT
import time 
import threading 

if __name__ == '__main__':
    start_date = input ("請輸入查詢起始日期：")
    end_date = input ("請輸入查詢結束日期：")
    start_time = time.time ()
    t1 = threading.Thread (target=tA.main, args=(start_date,end_date))
    t2 = threading.Thread (target=tT.main, args=(start_date,end_date))

    t1.start()
    time.sleep(1)
    t2.start()

    t1.join()
    t2.join()

    print("--- execution time of all : %s  ---" % (time.time() - start_time))
