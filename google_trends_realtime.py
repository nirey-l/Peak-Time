from serpapi import GoogleSearch
import json
from datetime import datetime

def fetch_google_trends_top10_final():
    # 발급받은 본인의 SerpApi Key를 여기에 넣으세요
    API_KEY = "e768f5e81374dca3e8176b654bcc28c0425308dcdeb8a2be4d2626b9010e8c8d" 
    
    params = {
        "engine": "google_trends_trending_now",
        "geo": "KR",
        "hl": "ko",
        "api_key": API_KEY
    }

    try:
        print(f"📡 [{datetime.now().strftime('%H:%M:%S')}] SerpApi로 진짜 실시간 데이터 수집 중...")
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # 'trending_searches' 리스트 가져오기
        trends = results.get("trending_searches", [])
        
        realtime_data = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # [핵심] 정확히 상위 10개만 슬라이싱 및 스키마 변환
        for i, item in enumerate(trends[:10]):
            realtime_data.append({
                "rank": i + 1,
                "keyword_name": item.get("query"), # 실제 검색어 명칭
                "source": "Google",
                "created_at": current_time
            })

        if realtime_data:
            # 최종 JSON 저장 (DB 연동용)
            with open("google_realtime_dashboard.json", "w", encoding="utf-8") as f:
                json.dump(realtime_data, f, ensure_ascii=False, indent=4)
            
            print(f"✅ [미션 클리어] Top 10 수집 완료!")
            for data in realtime_data:
                print(f"{data['rank']}위: {data['keyword_name']}")
        else:
            print("⚠️ 데이터가 비어있습니다. API 설정을 확인하세요.")

    except Exception as e:
        print(f"❌ SerpApi 호출 에러: {e}")

if __name__ == "__main__":
    fetch_google_trends_top10_final()