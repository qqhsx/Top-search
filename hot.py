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

for i in sum2:
    tmp = []
    for j in i:
        tmp.insert(0, i[j])
    tmp[0] = '<a href="https://cn.bing.com/search?q={}">{}</a>'.format(tmp[0], tmp[0])
    sum.append(tmp)

for i in sum:
    i[1] = int(i[1]) + 2
sum[0][1] = 1


def generate_cards(data):
    cards = ""
    for item in data:
        card = f"""
            <div class="card">
                <h2>{item[0]}</h2>
                <p>热度: {item[1]}</p>
                <p>{item[3]}</p> <!-- 添加详细描述 -->
            </div>
        """
        cards += card
    return cards


html_template = f"""
<!DOCTYPE html>
<html>

<head>
    <title>热搜榜</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .card {{
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 10px;
            width: 300px;
            text-align: left;
        }}

        h2 {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        p {{
            font-size: 14px;
        }}
    </style>
</head>

<body>
    <h1>热搜排行榜</h1>
    <br />
    <span>更新时间: <br /><span id="time"></span></span>
    <br />
    <div>
        {generate_cards(sum)}
    </div>
</body>

<footer>
    <script>
        var time = new Date({int(time.time() * 1000)});
        document.getElementById("time").innerHTML = time;
    </script>
</footer>

</html>
"""

with open("./index.html", "w", encoding="utf-8") as file:
    file.write(html_template)
