import requests
from icalendar import Calendar, Event
from datetime import datetime
import time

def main():
    # 使用 Session 保持連線狀態
    session = requests.Session()
    
    # 模擬非常具體的 Chrome 瀏覽器特徵
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.wantgoo.com/stock/calendar/dividend-right",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    })

    api_url = "https://www.wantgoo.com/stock/calendar/dividend-right-data"

    try:
        # 先訪問一次首頁，取得 Cookie
        print("正在獲取存取權限 (Step 1/2)...")
        session.get("https://www.wantgoo.com/stock/calendar/dividend-right", timeout=10)
        time.sleep(2) # 稍微停頓，模仿人類行為

        print("正在抓取資料 (Step 2/2)...")
        response = session.get(api_url, timeout=10)
        
        # 檢查是否被擋
        if response.status_code != 200:
            print(f"存取失敗，狀態碼：{response.status_code}")
            print(f"回傳內容：{response.text[:100]}") # 印出前100個字看是什麼錯誤
            return

        data = response.json()
        items = data if isinstance(data, list) else data.get('data', [])

        cal = Calendar()
        cal.add('X-WR-CALNAME', '台股除權息日曆')
        cal.add('X-WR-TIMEZONE', 'Asia/Taipei')

        count = 0
        for item in items:
            try:
                # 玩股網 API 日期欄位通常叫 date
                date_str = item.get('date')
                if not date_str: continue
                
                clean_date = datetime.strptime(date_str[:10], '%Y-%m-%d').date()
                name = item.get('name', '未知')
                stock_no = item.get('stockNo', '')
                cash = item.get('cashDividend', 0)

                event = Event()
                event.add('summary', f"除權息: {stock_no} {name}")
                event.add('dtstart', clean_date)
                event.add('dtend', clean_date)
                event.add('description', f"現金股利: {cash} 元")
                cal.add_component(event)
                count += 1
            except:
                continue

        with open('web.ics', 'wb') as f:
            f.write(cal.to_ical())
        
        print(f"🎉 成功！已建立 {count} 筆事件。")

    except Exception as e:
        print(f"❌ 錯誤詳情: {e}")
        # 即使失敗也產生一個檔案，避免 Action 下一步報錯
        with open('web.ics', 'w') as f: f.write("")

if __name__ == "__main__":
    main()
