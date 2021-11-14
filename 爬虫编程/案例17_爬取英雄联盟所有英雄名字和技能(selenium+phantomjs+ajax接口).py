# _*_ coding:utf-8 -*-
# 开发人员：&杜乾坤
# 开发工具：&pycharm
from selenium import webdriver
from lxml import etree
import requests, json

driver = webdriver.Chrome()
base_url = 'https://lol.qq.com/data/info-heros.shtml'
driver.get(base_url)
html = etree.HTML(driver.page_source)
hero_url_list = html.xpath('.//ul[@id="jSearchHeroDiv"]/li/a/@href')
hero_list = []  # 存放所有英雄的列表
for hero_url in hero_url_list:
    id = hero_url.split('=')[-1]
    # print(id)
    detail_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + id + '.js'
    # print(detail_url)
    headers = {
        'Referer': 'https://lol.qq.com/data/info-defail.shtml?id =4',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    response = requests.get(detail_url, headers=headers)
    n = json.loads(response.text)
    hero = []  # 存放单个英雄
    item_name = {}
    item_name['英雄名字'] = n['hero']['name'] + ' ' + n['hero']['title']
    hero.append(item_name)
    for i in n['spells']:  # 技能
        item_skill = {}
        item_skill['技能名字'] = i['name']
        item_skill['技能描述'] = i['description']
        hero.append(item_skill)
        hero.append('\n')
        #print(hero)
    hero_list.append(hero)
    # print(hero_list)
with open('hero.json','w',encoding='utf-8') as file:
    json.dump(hero_list,file,ensure_ascii=False)
    file.write('\n')
