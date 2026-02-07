import requests
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime
import os

def main():
    url = "https://www.wantgoo.com/stock/calendar/dividend-right"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 爬取網頁表格
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        # 玩股網表格通常在 class="table" 中
        dfs = pd.read_html(response.text)
        df = dfs[0] 

        # 建立 iCal 物件
        cal = Calendar()
        cal.add('prodid', '-//Custom Stock Calendar//TW//')
        cal.add('version', '2.0')
        cal.add('X-WR-CALNAME', '台股除權息行事曆')

        for _, row in df.iterrows():
            try:
                # 假設欄位名：日期, 股票, 現金股利, 股票股利 (需依實際網頁標題微調)
                date_str = row['日期'].replace('-', '/') # 標準化日期格式
                date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                
                event = Event()
                event.add('summary', f"除權息: {row['股票']}")
                event.add('dtstart', date_obj.date())
                event.add('dtend', date_obj.date())
                event.add('description', f"現金: {row['現金股利']} / 股票: {row['股票股利']}")
                
                cal.add_component(event)
            except:
                continue

        with open('web.ics', 'wb') as f:
            f.write(cal.to_ical())
        print("Success: web.ics generated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()