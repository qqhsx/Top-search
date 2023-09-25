import requests
import time

url = 'https://top.baidu.com/api/board?platform=wise&tab=realtime'
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
    'Host': 'top.baidu.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://top.baidu.com/board?tab=novel',
}

r = requests.get(url, headers=header)
json_data = r.json()
top_content_list = json_data['data']['cards'][0]['topContent']
content_list = json_data['data']['cards'][0]['content']

sum2 = top_content_list + content_list
sum = []

for i in range(len(sum2)):
    sum2[i]["index"] = i + 1  # 添加排行信息
    try:
        del sum2[i]["appUrl"]
        del sum2[i]["hotChange"]
        del sum2[i]["hotTag"]
        del sum2[i]["hotTagImg"]
        del sum2[i]["img"]
        del sum2[i]["indexUrl"]
        del sum2[i]["query"]
        del sum2[i]["rawUrl"]
        del sum2[i]["show"]
        del sum2[i]["url"]
    except KeyError:
        pass

for item in sum2:
    sum.append([item['index'], item['query'], item['hot'], item['detail']])

sum.sort(key=lambda x: x[0])

def generate_cards(data):
    cards = ""
    for item in data:
        card = f"""
            <div class="card">
                <div class="rank">排行: {item[0]}</div>
                <div class="hotspot">热点: {item[1]}</div>
                <div class="heat">热度: {item[2]}</div>
                <div class="description">详细描述: {item[3]}</div>
            </div>
        """
        cards += card
    return cards

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>热搜榜</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}

        .card {{
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            padding: 20px;
            margin: 10px 0;
        }}

        .rank {{
            font-weight: bold;
        }}

        .hotspot {{
            color: #FF5733;
        }}

        .heat {{
            color: #FFC300;
        }}

        .description {{
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>热搜排行榜</h1>
    <br>
    <span>更新时间: <br><span id="time"></span></span>
    <br>
    {generate_cards(sum)}
</body>
<footer>
    <script>
        var time = new Date({int(time.time() * 1000)});
        document.getElementById("time").innerHTML = time;
    </script>
</footer>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
