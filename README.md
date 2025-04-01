# 支持OCS的AI题库

## 环境要求
- Python 3.8+
- pip 包管理器

## 安装依赖
```bash
pip install -r requirements.txt
```

## 配置
在 `config.json` 文件中设置以下配置：
- host: API服务器地址
- port: API服务器端口
- api_key: 硅基流动 API密钥

目前只支持硅基流动的API_Key
[注册链接](https://cloud.siliconflow.cn/i/yWzlOTHL)
邀请码：`yWzlOTHL`

## 如何运行

```bash
python main.py
```

## 测试

```bash
python test_api.py
```



