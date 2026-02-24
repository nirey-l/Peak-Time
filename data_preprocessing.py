import json
import pandas as pd

# 구글 볼륨 문자열에서 '절대 검색량'과 '급상승 비율'을 숫자로 추출하는 함수
def parse_google_data(vol_str):
    if not isinstance(vol_str, str):
        return 0, 0
    
    lines = vol_str.split('\n')
    absolute_volume = 0
    surge_ratio = 0
    
    if len(lines) > 0:
        val_str = lines[0].replace('+', '').replace(',', '').strip()
        if '만' in val_str:
            absolute_volume = float(val_str.replace('만', '')) * 10000
        elif '천' in val_str:
            absolute_volume = float(val_str.replace('천', '')) * 1000
        else:
            try:
                absolute_volume = float(val_str)
            except ValueError:
                absolute_volume = 0
                
    if len(lines) >= 3:
        surge_str = lines[2].replace('%', '').replace(',', '').strip()
        try:
            surge_ratio = float(surge_str)
        except ValueError:
            surge_ratio = 0
            
    return absolute_volume, surge_ratio

# 분석할 4가지 카테고리 목록
categories = ['climate', 'entertainment', 'finance', 'sports']

print("🧹 데이터 전처리(불필요한 컬럼 제거 및 정제)를 시작합니다...\n")

for cat in categories:
    try:
        with open(f'data/trend_report_{cat}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        processed_results = []
        
        for item in data['results']:
            g_vol, g_surge = parse_google_data(item.get('google_volume', '0'))
            
            # 🔥 핵심 변경 사항: item.copy() 대신 필요한 5개 항목만 직접 지정해서 딕셔너리 생성
            new_item = {
                'rank_title': item.get('rank_title', ''),
                'google_absolute_volume': g_vol,
                'google_surge_ratio': g_surge,
                'naver_trend_sum': item.get('naver_trend_sum', 0),
                'naver_daily_ratio': item.get('naver_daily_ratio', [])
            }
            
            processed_results.append(new_item)
            
        # 1. JSON 파일로 저장
        new_json_data = {
            "category": data.get("category", cat),
            "base_date": data.get("base_date", ""),
            "results": processed_results
        }
        
        json_filename = f'data/preprocessed_{cat}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(new_json_data, f, ensure_ascii=False, indent=4)
            
        # 2. CSV 파일로 저장
        df = pd.DataFrame(processed_results)
        csv_filename = f'data/preprocessed_{cat}.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ [{cat.upper()}] 카테고리 최적화 완료! ({csv_filename} 생성됨)")
        
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: trend_report_{cat}.json")