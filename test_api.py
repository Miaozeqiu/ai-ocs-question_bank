import requests
import json
from config import API_CONFIG

# API 配置信息
api_config = {
    "name": "ZE题库(自建版)",
    "homepage": "https://pages.zaizhexue.top/",
    "url": f"http://127.0.0.1:{API_CONFIG['port']}/api/query",
    "method": "get",
    "type": "GM_xmlhttpRequest",
    "contentType": "json",
    "data": {
        "title": "${title}",
        "options": "${options}",
        "type": "${type}"
    },
    "handler": "return (res)=>res.code === 0 ? [undefined, undefined] : [undefined,res.data.data]"
}

def test_api(title, options="", question_type=""):
    """
    测试 ZE题库(自建版) API
    
    参数:
        title (str): 问题标题
        options (str): 问题选项，可选
        question_type (str): 问题类型，可选
    """
    # 准备请求参数
    params = {
        "title": title,
        "options": options,
        "type": question_type
    }
    
    print(f"正在发送请求到 {api_config['url']}")
    print(f"请求参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送 GET 请求
        response = requests.get(api_config["url"], params=params)
        
        # 检查响应状态码
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 解析 JSON 响应
            result = response.json()
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 检查是否成功
            if result.get("success"):
                data = result.get("data", {})
                code = data.get("code")
                answer = data.get("data")
                
                if code == 1 and answer:
                    print(f"\n✅ 查询成功！答案: {answer}")
                else:
                    print(f"\n❌ 未找到答案: {data.get('msg')}")
            else:
                print(f"\n❌ 请求失败: {result.get('error')}")
        else:
            print(f"\n❌ 请求失败: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    # 测试示例
    print("=" * 50)
    print("ZE题库 API 测试工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 测试单个问题")
        print("2. 退出")
        
        choice = input("请输入选项 (1/2): ").strip()
        
        if choice == "1":
            title = input("\n请输入问题标题: ").strip()
            options = input("请输入选项 (可选): ").strip()
            question_type = input("请输入问题类型 (可选): ").strip()
            
            print("\n" + "=" * 50)
            test_api(title, options, question_type)
            print("=" * 50)
        elif choice == "2":
            print("\n感谢使用 ZE题库 API 测试工具！")
            break
        else:
            print("\n❌ 无效的选项，请重新输入。")