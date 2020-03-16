import random
import requests
from bs4 import BeautifulSoup
# 引用 BlockingScheduler 類別
from apscheduler.schedulers.blocking import BlockingScheduler

# 當作報明牌隨機的股票 list
good_luck_list = ['0050', '0056', '2317', '2301', '2891', '1301', '1303' ,'2301', '2330', '2352', '2324', '9904']

# 創建一個 Scheduler 物件實例
sched = BlockingScheduler()

def compute_history_price():
	#stock_no = input("請輸入股票代號")
	#stock_no = 1301
	# random.choice 方法會從參數 list 隨機取出一個元素
  stock_no = random.choice(good_luck_list)
  year_limit = 100
	#year_limit = int(input("想計算近幾年以後的股價，如民國100年後之股價，請輸入100："))
  url = f'https://www.twse.com.tw/exchangeReport/FMNPTK?response=json&stockNo={stock_no}&_=1583236095771'
	#透過開發人員工具查得以上網址是利用API回傳歷年股價高低平均價，且以json型態回傳
  year_price = requests.get(url).json()
	#觀察回傳的資料year_price['data']為巢狀list
	#可用len()取得該list有幾筆歷年資料
  count = len(year_price['data'])

	#改用最近幾年的股價資料來計算
  hi_price = []
  low_price = []
  avg_price = []

  year_count=0
  for i in range(0,count):
		#只計算民國年股價資料計算最高最及ˊ平均股價
    if year_price['data'][i][0] >= year_limit:
      hi_price.append(float(year_price['data'][i][4]))
      low_price.append(float(year_price['data'][i][6]))
      avg_price.append(float(year_price['data'][i][8]))
      #顯示年度
      #print(year_price['data'][i][0])
      year_count += 1

  print('*************************歷年股價法**********************************')
  print(stock_no ,'近' , year_count , '年最高最低及平均股價')
  print('昂貴價', sum(hi_price)/year_count)
  print('便宜價', sum(low_price)/year_count)
  print('合理價', sum(avg_price)/year_count)
	#現在股價	
  url = f'https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stock_no}&CHT_CAT=YEAR'
  headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=2891'
	}
  resp = requests.post(url, headers=headers)
	# 設定編碼為 utf-8 避免中文亂碼問題
  resp.encoding = 'utf-8'

	# 根據 HTTP header 的編碼解碼後的內容資料（ex. UTF-8），若該網站沒設定可能會有中文亂碼問題。所以通常會使用 resp.encoding 設定
  raw_html = resp.text
	#將 HTML 轉成 BeautifulSoup 物件
  soup = BeautifulSoup(raw_html, 'html.parser')
  today_price = float(soup.select('body > table:nth-child(5) > tr > td:nth-child(3) > table > tr:nth-child(1) > td:nth-child(1) > table > tr:nth-child(3) > td:nth-child(1)')[0].text.replace(',',''))

  stock_name = soup.select('body > table:nth-child(5) > tr > td:nth-child(3) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table > tr:nth-child(1) > td > table > tr > td:nth-child(1) > nobr > a')[0].text

  print(stock_name, '今天股價', today_price)
  if (today_price >  sum(hi_price)/year_count):
    print('太貴了！')
  elif (today_price < sum(low_price)/year_count):
    print('太便宜了！')
  else:
    print('合理價！')


# decorator 設定 Scheduler 的類型和參數，例如 interval 間隔多久執行
@sched.scheduled_job('interval', minutes=5)
def timed_job():
    # 要注意不要太頻繁抓取
    print('每 5 分鐘執行一次程式工作區塊')
    compute_history_price()

# 開始執行
sched.start()