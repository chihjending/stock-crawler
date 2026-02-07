import requests
from icalendar import Calendar, Event
from datetime import datetime
import os

def main():
    # 這是玩股網後台真正的資料來源 API
    api_url = "https://www.wantgoo.com/stock/calendar/dividend-right-data"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.wantgoo.com/stock/calendar/dividend-right",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        print("正在從 API 獲取資料...")
        # 抓取 JSON 資料
        response = requests.get(api_url, headers=headers)
        data = response.json() # 直接解析 JSON

        cal = Calendar()
        cal.add('X-WR-CALNAME', '台股除權息日曆')
        cal.add('X-WR-TIMEZONE', 'Asia/Taipei')

        count = 0
        # 玩股網 API 回傳的資料結構通常在 data['data'] 或直接是清單
        # 根據觀察，API 通常回傳清單格式
        items = data if isinstance(data, list) else data.get('data', [])

        for item in items:
            try:
                # 取得 API 欄位：date (交易日期), stockNo (代碼), name (股票), cashDividend (現金股利)
                date_str = item.get('date') # 格式通常是 2026-02-07T00:00:00
                if not date_str: continue
                
                # 處理日期格式 (取前 10 碼 YYYY-MM-DD)
                clean_date = datetime.strptime(date_str[:10], '%Y-%m-%d').date()
                
                stock_name = item.get('name', '未知股票')
                stock_no = item.get('stockNo', '')
                cash = item.get('cashDividend', 0)
                stock_div = item.get('stockDividend', 0)

                event = Event()
                event.add('summary', f"除權息: {stock_no} {stock_name}")
                event.add('dtstart', clean_date)
                event.add('dtend', clean_date)
                event.add('description', f"現金股利: {cash} 元\n股票股利: {stock_div} 元")
                
                cal.add_component(event)
                count += 1
            except Exception as e:
                print(f"跳過一筆資料錯誤: {e}")
                continue

        with open('web.ics', 'wb') as f:
            f.write(cal.to_ical())
        
        print(f"🎉 成功處理 {count} 筆除權息事件！檔案已儲存。")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        # 建立保底空檔案避免 GitHub Action 報錯
        with open('web.ics', 'w') as f:
            f.write("")

if __name__ == "__main__":
    main()
