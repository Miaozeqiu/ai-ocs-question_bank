import requests
import traceback
import json
import time

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    API_CONFIG = json.load(f)

def query_large_model(title, options, question_type):
    """
    调用SiliconFlow API获取问题答案
    
    参数:
        title (str): 问题标题
        options (str): 问题选项
        question_type (str): 问题类型
    
    返回:
        str: API返回的答案
    """
    url = "https://api.siliconflow.cn/v1/chat/completions"
    
    
    # 构建提问内容

    content = '''你是一个题库接口函数，请根据问题和选项提供答案。如果是选择题，直接返回对应选项的内容，注意是内容，不是对应字母；如果题目是多选题，将内容用“###”连接；如果选项内容是"对","错"，且只有两项，或者question_type是judgement，你直接返回“对”或“错”的文字，不要返回字母；如果是填空题，直接返回填空内容，多个空使用###连接。回答格式为：”{"anwser":"your_anwser_str"}“，严格使用此格式回答。比如我问你一个问题，你回答的是"是"，你回答的格式为：”{"anwser":"是"}“。不要回答嗯，好的，我知道了之类的话，你的回答只能是json。下面是一个问题，请你用json格式回答我，绝对不要使用自然语言'''
    content += f'''{{
        "问题": "{title}",
        "选项": "{options}",
        "类型": "{question_type}"
    }}'''

    payload = {
        "model": "Qwen/QwQ-32B",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "stop": None,
        "temperature": 0.1,  # 降低温度以获得更确定的答案
        "top_p": 0.9,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }
    
    headers = {
        "Authorization": f"Bearer {API_CONFIG['api_key']}",
        "Content-Type": "application/json"
    }
    
    # 添加重试机制
    max_retries = 3
    retry_delay = 2  # 秒
    
    for attempt in range(max_retries):
        try:
            print(f"尝试 {attempt+1}/{max_retries} - 准备发送请求到 {url}")
            print(f"请求头: {headers}")
            print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
            
            # 发送请求
            response = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
            
            print(f"API响应状态码: {response.status_code}")
            print(f"API响应内容: {response.text[:200]}...")  # 只打印前200个字符
            
            # 如果是服务器错误，尝试重试
            if response.status_code >= 500:
                if attempt < max_retries - 1:
                    print(f"服务器错误，将在 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                    continue
            
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析响应
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"]
                return answer
            else:
                print(f"API响应格式异常: {json.dumps(result, ensure_ascii=False)}")
                return "无法从API获取答案"
                
        except requests.exceptions.Timeout:
            print("API请求超时")
            if attempt < max_retries - 1:
                print(f"将在 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return "API调用超时，请稍后再试"
                
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
            if attempt < max_retries - 1:
                print(f"将在 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return f"API请求异常: {str(e)}"
                
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
            print(f"响应内容: {response.text}")
            return f"API响应解析失败: {str(e)}"
            
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"调用大模型API失败: {str(e)}")
            print(f"详细错误信息: {error_trace}")
            return f"API调用失败: {str(e)}"
    
    return "多次尝试后仍无法获取答案，请稍后再试"

if __name__ == "__main__":
    # 测试函数
    test_title = "中国的首都是哪里__，美国的首都是哪里__"
    test_options = ""
    test_type = "填空"
    print(f"测试参数: title={test_title}, options={test_options}, question_type={test_type}")
    
    ai_answer = query_large_model(test_title, test_options, test_type)
    print(f"测试结果: {ai_answer}")