# coding: utf-8
# @Time : 2021/12/18 23:14
# @Author : wowbat
# @File : defense_paper.py
# @Describe: 香港文汇报自动下载

import datetime, json
import utils
from model import News


def get_news_in_paper(date_str, paper_url):
    """
    获得报纸url中的各部分信息
    :param paper_url: 当天报纸主页的url链接
    :param date_str: 报纸当天日期
    :return: 各部分的信息列表, 每个信息包括name(版面信息, 如"第01版：头条")和url(版面对应的链接)
    """
    section_list_json = utils.get_url_content(paper_url)  # 获得报纸html内容
    section_list = json.loads(section_list_json).get('data')
    all_news = []
    if section_list:
        for section in section_list:
            # 只要A开头的版面
            if not section.get('sectionCode').startswith('A'):
                continue
            section_name = section.get('sectionName')
            section_uuid = section.get('uuid')
            if section_uuid:
                section_json = utils.get_url_content(
                    'https://www.wenweipo.com/epaper/api/v1/book/listSectionNewsWithoutFile?bookId=wwp&sectionId={}'.format(
                        section_uuid))
                news_list = json.loads(section_json).get('data')
                for new in news_list:
                    if new.get('title') and new.get('content'):
                        title = utils.to_simplified_chinese(new.get('title'))
                        column_name = utils.to_simplified_chinese(section_name)
                        content = utils.to_simplified_chinese(new.get('content'))
                        url = new.get('url') if new.get('url') else section_uuid
                        all_news.append({
                            "new": {"date": date_str,
                                    "section": column_name,
                                    "title": title,
                                    "url": url
                                    },
                            "new_info": {
                                "title": title,
                                "titleHtml": "<h1>{}</h1>".format(title),
                                "subtitle": '',
                                "subtitleHtml": '',
                                "content": content,
                                "contentHtml": '<p>'+"</p>\n<p>".join(content.split('\n')) + "</p>",
                                "abstract": content
                            }
                        })
    return all_news


def get_all_news_by_date(giving_date):
    """
    根据指定日期获取所有的不相同的新闻列表
    :param giving_date:
    :return:
    """
    url, date_str = utils.get_paper_url(giving_date, type="香港文汇报")
    # 获取报纸信息
    all_news = get_news_in_paper(date_str, url)
    return all_news


def save_detail_new_by_date(new_model, giving_date):
    """
    保存指定日期对应的所有新闻详情
    :param new_model: 新闻模型
    :param giving_date: datetime型，指定的日期
    :return:
    """
    all_news = get_all_news_by_date(giving_date)
    if all_news and len(all_news) > 1:
        for all_new in all_news:
            new = all_new['new']
            new_info = all_new['new_info']
            if len(new_info['content']) < 150:
                continue
            new_model.save(new, new_info)
    print("《香港文汇报》({})保存完毕, 共保存{}条新闻".format(giving_date, len(all_news)))


def collect_HongKong_paper(start_date, collect_num):
    new_model = News(source="香港文汇报")  # 存储模型
    date_list = utils.generate_date_list(start_date, collect_num)  # 获得日期列表
    for date in date_list:
        save_detail_new_by_date(new_model, date)
    print("《香港文汇报》采集完成！")


if __name__ == "__main__":
    start_date = datetime.date(2022, 5, 7)  # 给定日期
    collect_HongKong_paper(start_date, 3)
