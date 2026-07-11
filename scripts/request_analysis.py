import os

import requests

import json

from datetime import datetime



def request_analysis():
  
    api_key = os.getenv("MANUS_API_KEY")
  
    project_id = os.getenv("PROJECT_ID")
  


    if not api_key:
      
        print("Error: MANUS_API_KEY is not set.")
      
        return
      


    # 分析対象の競合リスト

    competitors = [
      
        "https://www.instagram.com/kicocochi_kobo/",
      
        "https://www.instagram.com/placehome/",
      
        "https://www.instagram.com/eda_kensetsu/",
      
        "https://www.instagram.com/irodori8223",
      
        "https://www.instagram.com/torikaihome/",
      
        "https://www.instagram.com/inouehousing/",
      
        "https://www.instagram.com/rokka_staff/",
      
        "https://www.instagram.com/hooop.inc/",
      
        "https://www.instagram.com/eternal_designlife/"
      
    ]
  


    prompt = f"""
    
直近1週間のInstagram競合分析と自社分析を行い、来週の投稿戦略を提案してください。



### 分析対象（競合）:

{chr(10).join(competitors)}



### 指示事項:

1. 各競合アカウントの直近投稿内容、反応数、使用ハッシュタグを調査してください。

2. 自社アカウント（@tiida_saga）の直近パフォーマンスと比較してください。

3. 分析結果をMarkdown形式でまとめ、リポジトリの `reports/analysis_{datetime.now().strftime('%Y%m%d')}.md` として保存してください。

4. 来週の投稿案（リール、カルーセル、ストーリーズ各1件以上）を作成し、PR（Pull Request）として提出してください。

"""
  


    url = "https://api.manus.ai/v2/task.create"
  
    headers = {
      
        "Content-Type": "application/json",
      
        "x-manus-api-key": api_key
      
    }
  


    payload = {
      
        "project_id": project_id,
      
        "message": {
          
            "content": prompt
          
        }
      
    }
  


    print(f"Sending analysis request to Manus API for project {project_id}...")
  
    response = requests.post(url, headers=headers, json=payload)
  


    if response.status_code == 200:
      
        result = response.json()
      
        if result.get("ok"):
          
            task_id = result["data"]["task_id"]
          
            print(f"Success! Task created with ID: {task_id}")
          
        else:
          
            print(f"API Error: {result.get('error')}")
          
    else:
      
        print(f"HTTP Error: {response.status_code} - {response.text}")
      


if __name__ == "__main__":
  
    request_analysis()
  











































