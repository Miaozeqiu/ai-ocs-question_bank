import requests
import json

def test_query_api():
    # 测试参数
    test_cases = [
        {
            "title": "Java是什么？",
            "options": "A. 编程语言 B. 一种咖啡 C. 游戏 D. 食物",
            "type": "single",
            "description": "测试基本查询"
        },
        {
            "title": "",  # 空标题
            "options": "",
            "type": "",
            "description": "测试空标题"
        },
        {
            "title": "1+1=?",
            "options": "A.1 B.2 C.3 D.4",
            "type": "single",
            "description": "测试简单数学题"
        }
    ]
    
    # API基础URL
    base_url = "http://127.0.0.1:5000/api/query"
    
    # 测试每个用例
    for case in test_cases:
        print(f"\n开始测试: {case['description']}")
        print(f"请求参数: {case}")
        
        try:
            # 发送GET请求
            response = requests.get(
                base_url,
                params={
                    "title": case["title"],
                    "options": case["options"],
                    "type": case["type"]
                }
            )
            
            # 打印响应状态码
            print(f"状态码: {response.status_code}")
            
            # 如果响应成功，打印响应内容
            if response.status_code == 200:
                result = response.json()
                print("响应内容:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"请求失败: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("连接失败: 请确保Flask服务器已启动")
        except Exception as e:
            print(f"测试异常: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    print("开始API测试...")
    test_query_api()
    print("\n测试完成!")