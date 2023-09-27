import requests
import time
import re

# 定义去除链接中无用空格的函数
def remove_whitespace_in_links(text):
    # 使用正则表达式查找并替换链接中的无用空格
    text = re.sub(r'(\[[^\]]+\])\(([^)]+?)\s+([^)]+?)\)', r'\1(\2\3)', text)
    return text

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
    tmp[0] = '[{}]({})'.format(tmp[0], 'https://cn.bing.com/search?q=' + tmp[0])
    sum.append(tmp)

for i in sum:
    i[1] = int(i[1]) + 2
sum[0][1] = 1

markdown_text = "# 今日热点\n\n"
markdown_text += "更新时间: {}\n\n".format(time.strftime('%Y-%m-%d %H:%M:%S'))

for item in sum:
    # 使用去除链接中无用空格的函数处理链接
    item[0] = remove_whitespace_in_links(item[0])
    
    markdown_text += "## 热点：{}\n".format(item[0])
    markdown_text += "排行：{}\n".format(item[1])
    markdown_text += "热度：{}\n".format(item[2])
    markdown_text += "详细描述：{}\n\n".format(item[3])

with open("./index.md", "w", encoding="utf-8") as markdown_file:
    markdown_file.write(markdown_text)
