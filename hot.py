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
    del sum2[i]["appUrl"]
    del sum2[i]["hotChange"]
    try:
        del sum2[i]["hotTag"]
    except:
        pass
    try:
        del sum2[i]["hotTagImg"]
    except:
        pass
    del sum2[i]["img"]
    del sum2[i]["indexUrl"]
    del sum2[i]["query"]
    del sum2[i]["rawUrl"]
    del sum2[i]["show"]
    del sum2[i]["url"]

for item in sum2:
    card = {
        '排行': item['index'],
        '热点': item['query'],
        '热度': item['hot'],
        '详细描述': item['detail']
    }
    sum.append(card)

# 按排行排序
sum.sort(key=lambda x: x['排行'])

# 创建卡片式HTML页面
cards_html = ''
for item in sum:
    card_html = f'''
    <div class="card">
        <h2>排行: {item['排行']}</h2>
        <p>热点: {item['热点']}</p>
        <p>热度: {item['热度']}</p>
        <p>详细描述: {item['详细描述']}</p>
    </div>
    '''
    cards_html += card_html

# 生成完整HTML页面
html = f'''
<!DOCTYPE html>
<html>

<head>
    <title>热搜榜</title>
    <style>
        .card {{
            background-color: #ffffff;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 10px;
        }}

        h2 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}

        p {{
            font-size: 18px;
            margin-bottom: 5px;
        }}
    </style>
</head>

<body>
    <h1>热搜排行榜</h1>
    <br />
    <span>更新时间: <br /><span id="time"></span></span>
    <br />
    {cards_html}
</body>

<footer>
    <script>
        var time = new Date({int(time.time() * 1000)});
        document.getElementById("time").innerHTML = time;
    </script>
</footer>

</html>
'''

with open("./index.html", "w", encoding="utf-8") as xxxx:
    xxxx.write(html)
