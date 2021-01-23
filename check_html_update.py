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

# Webサイトの更新チェックを行うサイトなどの設定ファイルのパス
ACCESS_SITE_INFO_PATH = "/var/tmp/check_sites_info.json"

# 設定ファイルは以下の書式
# {
#   "sites_info" : [
#       { "url": "http://チェックするサイトのURL", "temp_file_name" : "更新履歴を保持するファイル名", "message" : "更新時のメッセージ"},
#       ... 複数サイト指定可能, tmp_file_nameはサイト毎に分ける
#   ],
#   "web_hook_url" : "http://.... SlackのIncommingWebhookのURL"
# }
#

# 更新チェックを行うサイトのリストを取得する
def load_check_site_info():
    info_path = ACCESS_SITE_INFO_PATH
    f = open(info_path, 'r')
    load_info = json.load(f)
    
    return load_info

# Slackにメッセージを投稿します
def post_message_to_slack(url, message):
    requests.post(url, data = json.dumps({
        'text': u'' + message
    }))

# urlのサイトが更新されているか調べる. 結果はtmpファイルに保存する
def check_is_website_update(url, tmp):
    # URLの結果を保存しておくファイル(次回の比較に使用する)
    file = '/tmp/' + tmp
    
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

    check_sites_info = load_check_site_info()
    web_hook_url = check_sites_info["web_hook_url"]

    for site in check_sites_info["sites_info"]:
        if (check_is_website_update(site['url'], site['temp_file_name'])):
            post_message_to_slack(web_hook_url, site['message'] + site['url'])

if __name__ == '__main__':
    main()

