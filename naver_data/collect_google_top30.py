import os
import json
import time
import urllib.request
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# .env 파일에서 API 키 로드
load_dotenv()

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_integrated_analysis_final():
    target_urls = {
        'finance': 'https://trends.google.co.kr/trending?geo=KR&hl=ko&hours=168&category=3',
        'sports': 'https://trends.google.co.kr/trending?geo=KR&hl=ko&hours=168&category=17',
        'entertainment': 'https://trends.google.co.kr/trending?geo=KR&hl=ko&hours=168&category=4',
        'climate': 'https://trends.google.co.kr/trending?geo=KR&hl=ko&hours=168&category=20'
    }
    
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    summary_report = {}

    for label, url in target_urls.items():
        print(f"\n🚀 [{label}] 카테고리 분석 시작...")
        driver.get(url)
        time.sleep(12) 

        # [수정포인트] r""" 를 사용하여 자바스크립트 내부의 \n이 파이썬에서 깨지지 않게 보호합니다.
        extract_script = r"""
        let results = [];
        let rows = document.querySelectorAll('tr[role="row"]');
        rows.forEach(row => {
            let cells = row.querySelectorAll('td');
            if(cells.length > 2) {
                let titleDiv = cells[1].querySelector('.mZ3Rlc') || cells[1].querySelector('div');
                let volumeDiv = cells[2]; 
                
                if(titleDiv) {
                    let title = titleDiv.innerText.trim();
                    let volume = volumeDiv ? volumeDiv.innerText.trim() : "0";
                    if(title && !results.some(item => item.title === title)) {
                        results.push({title: title, google_volume: volume});
                    }
                }
            }
        });
        return results;
        """
        
        try:
            raw_google_data = driver.execute_script(extract_script)
            
            filtered_list = []
            for item in raw_google_data:
                if not any(char.isdigit() for char in item['title']) and "전" not in item['title']:
                    filtered_list.append(item)
                if len(filtered_list) >= 30: break

            titles = [it['title'] for it in filtered_list]
            naver_raw = fetch_naver_data(titles)

            final_data_list = []
            for item in filtered_list:
                n_data = next((res['data'] for res in naver_raw if res['title'] == item['title']), [])
                ratio_sum = round(sum(day['ratio'] for day in n_data), 2)
                
                final_data_list.append({
                    "rank_title": item['title'],
                    "google_volume": item['google_volume'],
                    "naver_trend_sum": ratio_sum,
                    "naver_daily_ratio": n_data
                })

            save_path = f'trend_report_{label}.json'
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "category": label,
                    "base_date": datetime.now().strftime('%Y-%m-%d'),
                    "results": final_data_list
                }, f, ensure_ascii=False, indent=4)
            
            summary_report[label] = {
                "total_count": len(final_data_list),
                "keywords": [x['rank_title'] for x in final_data_list]
            }
            print(f"✅ {label} 완료: {len(final_data_list)}개 키워드 분석됨")

        except Exception as e:
            print(f"❌ {label} 실행 중 자바스크립트 오류 발생: {e}")

    with open('collection_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=4)
    
    print("\n✨ 모든 분석이 완료되었습니다!")
    driver.quit()

def fetch_naver_data(keywords):
    if not keywords: return []
    url = "https://openapi.naver.com/v1/datalab/search"
    results = []
    for i in range(0, len(keywords), 5):
        chunk = keywords[i:i+5]
        body = {
            "startDate": "2026-02-17",
            "endDate": datetime.now().strftime('%Y-%m-%d'),
            "timeUnit": "date",
            "keywordGroups": [{"groupName": k, "keywords": [k]} for k in chunk]
        }
        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", NAVER_ID)
        req.add_header("X-Naver-Client-Secret", NAVER_SECRET)
        req.add_header("Content-Type", "application/json")
        try:
            res = urllib.request.urlopen(req, data=json.dumps(body).encode("utf-8"))
            results.extend(json.loads(res.read())['results'])
            time.sleep(0.5)
        except:
            pass
    return results

if __name__ == "__main__":
    get_integrated_analysis_final()