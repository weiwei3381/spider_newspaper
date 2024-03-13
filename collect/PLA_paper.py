# coding: utf-8
# @Time : 2021/12/19 21:43
# @Author : wowbat
# @File : PLA_paper.py
# @Describe: 解放军报信息采集

import datetime
import utils
from bs4 import BeautifulSoup
from model import News

def get_contents_from_json(json_url):
    json_data = utils.get_json_data(json_url)
    sections = json_data.get('paperInfo', [])
    for section in sections:
        paperNumber = section.get('paperNumber', '')  # 板块序号
        paperBk = section.get('paperBk', '')  # 板块名称
        section_name = "第{}版：{}".format(paperNumber, paperBk)  # 拼接板块名称
        paper_date = section.get('paperData', '')  # 报纸日期
        news = section.get('xyList', [])
        for new in news:
            date = new.get('')
            main_title = new.get('title', '')  # 主标题
            sub_title = new.get('title2', '') or new.get('guideTitle', '')  # 副标题
            content_html = new.get('content', '')  # 内容html
            soup = BeautifulSoup(content_html, "lxml")
            content_str = soup.get_text(separator="\n").strip()  # 获得内容文本
            abstract = ""  # 摘要
            if len(soup.find_all("p")) > 1:
                abstract = soup.find_all("p")[0].text + soup.find_all("p")[1].text
            yield {
                'new': {
                    'date':paper_date,
                    'section': section_name,
                    'title': main_title,
                    "url": '',
                },
                'new_info': {
                    "title": main_title,
                    "titleHtml": '',
                    "subtitle": sub_title,
                    "subtitleHtml": '',
                    "content": content_str,
                    "contentHtml": content_html,
                    "abstract": abstract
                }
            }


def save_detail_new_by_date(new_model, giving_date):
    """
    保存指定日期对应的所有新闻详情
    :param new_model: 新闻模型
    :param giving_date: datetime型，指定的日期
    :return:
    """

    # 获得当天新闻对应的json路径
    json_url, date_str = utils.get_paper_url(giving_date, type="解放军报")
    exist_titles = {}   # 已经存储的标题
    for new_data in get_contents_from_json(json_url):
        new = new_data.get('new')
        new_info = new_data.get('new_info')
        if new['title'].strip() == "图片":
            continue
        if len(new_info['content']) < 150:
            continue
        if exist_titles.get(new['title']):
            continue
        new_model.save(new, new_info)
        exist_titles[new['title']] = 1
    print("《解放军报》({})保存完毕, 共保存{}条新闻".format(giving_date, len(exist_titles)))


def collect_PLA_paper(start_date, collect_num):
    new_model = News(source="解放军报")  # 存储模型
    date_list = utils.generate_date_list(start_date, collect_num)  # 获得日期列表
    for date in date_list:
        save_detail_new_by_date(new_model, date)
    print("《解放军报》采集完成！")


if __name__ == "__main__":
    start_date = datetime.date(2023, 4, 21)  # 给定日期
    collect_PLA_paper(start_date, 1)
