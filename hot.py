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

def dict_to_card(data):
    card_html = '<div class="card">'
    card_html += '<h2>热点：{}</h2>'.format(data[1])  # 对调了“热点”和“排行”位置
    card_html += '<p>排行：{}</p>'.format(data[0])  # 对调了“热点”和“排行”位置
    card_html += '<p>热度：{}</p>'.format(data[2])
    card_html += '<p>详细描述：{}</p>'.format(data[3])
    card_html += '</div>'
    return card_html

cards_html = ''
for item in sum:
    card_html = dict_to_card(item)
    cards_html += card_html

xs = """
<!DOCTYPE html>
<html>

<head>
    <title>热搜榜</title>
    <style>
        .card {
            border: 1px solid #ccc;
            padding: 16px;
            margin: 16px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        }

        h2 {
            font-size: 24px;
            margin: 0;
        }

        p {
            font-size: 16px;
            margin: 8px 0;
        }

        .return-home {
            margin-top: 20px;
            text-align: center;
        }

        .return-home a {
            font-size: 18px;
            text-decoration: none;
            background-color: #0074D9;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .return-home a:hover {
            background-color: #0056b3;
        }
    </style>
</head>

<body>
    <h1>热搜排行榜</h1>
    <br />
    <span>更新时间: <br /><span id="time"></span></span>
    <br />
    <div class="return-home">
        <a href="https://qqhsx.github.io/Top-search/">返回首页</a> <!-- 修改首页链接地址 -->
    </div>
    """ + cards_html + """
</body>

<footer>
    <script>
        var time = new Date(""" + str(int(time.time() * 1000)) + """);
        document.getElementById("time").innerHTML = time;
    </script>
</footer>

</html>
"""

with open("./index.html", "w", encoding="utf-8") as xxxx:
    xxxx.write(xs)
