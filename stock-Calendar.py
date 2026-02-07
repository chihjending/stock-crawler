import requests
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime

def main():
    url = "https://www.wantgoo.com/stock/calendar/dividend-right"
    # 模擬瀏覽器，避免被網站封鎖
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.wantgoo.com/"
    }

    try:
        response = requests.get(url, headers=headers)
        # 使用 pandas 讀取表格，指定編碼為 utf-8
        dfs = pd.read_html(response.text)
        df = dfs[0]

        cal = Calendar()
        cal.add('X-WR-CALNAME', '台股除權息日曆') # 給日曆起個名字

        for _, row in df.iterrows():
            try:
                # 玩股網目前的欄位名稱通常是：'除權息日期', '名稱', '現金股利', '股票股利'
                date_str = str(row['除權息日期']).replace('-', '/')
                event = Event()
                event.add('summary', f"除權息: {row['名稱']}")
                event.add('dtstart', datetime.strptime(date_str, '%Y/%m/%d').date())
                event.add('dtend', datetime.strptime(date_str, '%Y/%m/%d').date())
                event.add('description', f"現金: {row['現金股利']} | 股票: {row['股票股利']}")
                cal.add_component(event)
            except:
                continue

        with open('web.ics', 'wb') as f:
            f.write(cal.to_ical())
        print("🎉 web.ics 已成功更新！")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()