import os
import json
import urllib.request
from datetime import datetime
from dotenv import load_dotenv
import time
import xml.etree.ElementTree as ET

load_dotenv()

# 네이버 API 키 설정
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_trending_keywords():
    """구글 RSS 피드에서 가능한 모든 키워드를 가져와 최대 30개 반환"""
    print("구글 실시간 트렌드 수집 중 (Max 30)...")
    url = "https://trends.google.co.kr/trending/rss?geo=KR"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            xml_data = res.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            
            keywords = []
            # RSS 내의 모든 <item> 태그에서 키워드 추출
            for item in root.findall('.//item'):
                title = item.find('title').text
                if title:
                    keywords.append(title)
            
            # 최대 30개까지 자르기
            top_30_kws = keywords[:30]
            print(f"총 {len(top_30_kws)}개의 키워드를 확보했습니다.")
            return top_30_kws
            
    except Exception as e:
        print(f"구글 수집 오류: {e}")
        return ["뉴스", "날씨", "주식", "환율", "삼성전자"]

def fetch_naver_trend(keywords):
    """네이버 데이터랩 API 호출 (2026-02-17 ~ 현재)"""
    if not keywords:
        return []

    url = "https://openapi.naver.com/v1/datalab/search"
    start_date = "2026-02-17"
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    all_results = []
    
    # 5개씩 묶어서 호출 (30개일 경우 총 6번 호출)
    for i in range(0, len(keywords), 5):
        chunk = keywords[i:i+5]
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "keywordGroups": [{"groupName": kw, "keywords": [kw]} for kw in chunk]
        }

        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", NAVER_ID)
        req.add_header("X-Naver-Client-Secret", NAVER_SECRET)
        req.add_header("Content-Type", "application/json")
        
        try:
            res = urllib.request.urlopen(req, data=json.dumps(body).encode("utf-8"))
            res_data = json.loads(res.read())
            all_results.extend(res_data['results'])
            print(f"네이버 API 호출 성공: {i+1} ~ {i+len(chunk)}번째 키워드 완료")
            time.sleep(0.3) # 30개 호출 시 안전을 위해 지연 시간 소폭 상향
        except Exception as e:
            print(f"네이버 API 호출 오류 ({chunk}): {e}")
            
    return all_results

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 수집 프로세스 시작")
    
    # 1. 키워드 수집
    kws = get_trending_keywords()
    
    # 2. 네이버 트렌드 조회 (수집된 개수만큼 전체 진행)
    if kws:
        naver_results = fetch_naver_trend(kws)
        
        # 3. JSON 구조화
        output = {
            "top_keywords_list": kws, # 최상단에 리스트 배치
            "meta_info": {
                "source": "google_trends_rss & naver_datalab",
                "period": "2026-02-17 to " + datetime.now().strftime('%Y-%m-%d'),
                "collected_at": datetime.now().isoformat(),
                "count": len(kws)
            },
            "data": naver_results
        }
        
        # 4. 파일 저장
        with open('naver_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        
        print(f"완료: {len(kws)}개의 키워드 분석 데이터를 naver_data.json에 저장했습니다.")
    else:
        print("수집된 키워드가 없어 중단합니다.")