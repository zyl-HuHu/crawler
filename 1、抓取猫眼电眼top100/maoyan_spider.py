import json
import requests
from requests.exceptions import RequestException
import re
import time

'''
整体思路：
1、利用requests.get解析出单页面的信息
2、解析获取到的单页面信息
3、将解析后的数据进行存储
4、循环获取10页数据
'''

# 请求单页面方法
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

'''
 <dd>
    <i class="board-index board-index-10">10</i>
    <a href="/films/3667" title="辛德勒的名单" class="image-link" data-act="boarditem-click" data-val="{movieId:3667}">
      <img src="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
      <img data-src="https://p0.meituan.net/movie/b0d986a8bf89278afbb19f6abaef70f31206570.jpg@160w_220h_1e_1c" alt="辛德勒的名单" class="board-img" />
    </a>
    <div class="board-item-main">
        <div class="board-item-content">
            <div class="movie-item-info">
                <p class="name"><a href="/films/3667" title="辛德勒的名单" data-act="boarditem-click" data-val="{movieId:3667}">辛德勒的名单</a></p>
                <p class="star">
                        主演：连姆·尼森,拉尔夫·费因斯,本·金斯利
                </p>
                <p class="releasetime">上映时间：1993-12-15(美国)</p>    </div>
                    <div class="movie-item-number score-num">
                <p class="score"><i class="integer">9.</i><i class="fraction">2</i></p>        
            </div>
        </div>
    </div>
</dd>
'''
# 解析单页面
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<img data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6],
        }

# 存储到文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        # 使用son.dumps将字典转换成字符串；json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    # 接收返回结果
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)