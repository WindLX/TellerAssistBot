import json

# 获取token
def get_token():
    with open('./TellerAssistBot/config/core.json', 'r', encoding='utf-8')as f:
        return json.load(f)["token"]

# 获取信息
def load_information(index, key):
    with open('./TellerAssistBot/config/data.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data["information"][index][key]

# 获取字符串到emoji映射
def load_str2emoji(index, key):
    with open('./TellerAssistBot/config/data.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data["str_2_emoji"][index][key]
        