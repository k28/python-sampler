#! /usr/bin/env python
# vim: fileencoding=utf-8

import requests
import json
import bs4

#
# CHECK_URLを監視して、変更があった時にアクション(Slackに通知)します
#
# resuests, bs4はpipでインストールしておきます
#

# SlackのIncoming webhookのURL
WEB_HOOK_URL = ""
# 更新確認するサイト
CHECK_URL = 'https://.....'

def post_message_to_slack():
    requests.post(WEB_HOOK_URL, data = json.dumps({
        'text': u'Slackに投稿するメッセージを入れます' + CHECK_URL
    }))

def check_is_website_update():
    # チェックするURL
    url = CHECK_URL
    # URLの結果を保存しておくファイル(次回の比較に使用する)
    file = '/tmp/html_source.txt'
    
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser') # parser

    elems = soup.select('.entry-content')
    str_elems = str(elems)
    # print(str_elems)

    try:
        f = open(file)
        old_elems = f.read()
    except:
        old_elems = ' '
    
    if (str_elems == old_elems):
        return False

    # 違いがあった
    f = open(file, 'w')
    f.writelines(str_elems)
    f.close()
    return True


def main():
    if (check_is_website_update()):
        # slackに通知する
        post_message_to_slack()

if __name__ == '__main__':
    main()

