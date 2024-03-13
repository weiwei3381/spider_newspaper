# coding: utf-8
# @Time : 2021/12/18 23:14
# @Author : wowbat
# @File : defense_paper.py
# @Describe:新华每日电讯自动下载

import datetime
import utils
import config
from bs4 import BeautifulSoup
from urllib import parse
from model import News


def get_all_news_in_paper(paper_date, paper_url, section_list_selector):
    """
    获得报纸url中的各部分信息
    :param paper_url: 当天报纸主页的url链接
    :param section_list_selector: 获取部分的选择器
    :return: 各部分的信息列表, 每个信息包括name(版面信息, 如"第01版：头条")和url(版面对应的链接)
    """
    paper_html = utils.get_url_content(paper_url)  # 获得报纸html内容
    news_list = []  # 存储版面信息的列表, 最后会返回该列表
    soup = BeautifulSoup(paper_html, "lxml")
    section_node = soup.find(**section_list_selector)
    if section_node:
        section_nodes = section_node.select('h4 > a:nth-child(2)')  # 获得所有版面节点
        for i in range(len(section_nodes)):
            section_node = section_nodes[i]
            # 分析每个版面节点, 将其加入到版面信息列表中
            section_name = section_node.text.strip().replace(" ","")
            news_node = soup.select_one('body > div.listdaohang > ul:nth-child({})'.format((i+1)*2+1))
            if news_node:
                news = news_node.find_all('a')
                for new in news:
                    news_list.append(
                        {"date": paper_date,
                         "section": section_name,
                         "title": new.text.strip(),
                         "url": parse.urljoin(paper_url, new.attrs['daoxiang'])
                         }
                    )
    unique_news_url_list = utils.delete_repeated_news(news_list)  # 得到唯一的新闻list
    return unique_news_url_list


def analysis_new(new_url):
    """
    分析新闻
    :param new_url: 新闻网址
    :return: 返回解析后的新闻信息,包括标题, 副标题, 正文, 摘要和原始的html信息
    """
    html = utils.get_url_content(new_url)
    soup = BeautifulSoup(html, "lxml")
    title_node = soup.find('h2')
    subtitle_node = soup.find('h4')
    content_node = soup.select_one('div#contenttext > div:nth-child(7)')
    # 保存的信息
    title_str = title_html = ''  # 标题及其原始html代码
    subtitle_html = subtitle_str = ''  # 副标题及其原始html代码
    content_str = content_html = ''  # 内容及其原始的html代码
    abstract = ''  # 摘要信息
    # 更新值
    if title_node:
        title_html = title_node.prettify()  # 将node进行美化, 添加换行符
        title_str = title_node.text.strip()
    if subtitle_node:
        subtitle_html = subtitle_node.prettify()
        subtitle_str = subtitle_node.text.strip()
    if content_node:
        content_html = content_node.prettify()
        content_str = content_node.text.strip()
        # 第一段为概述
        if len(content_node.find_all("p")) > 1:
            abstract = content_node.find_all("p")[0].text + content_node.find_all("p")[1].text
    return {
        "title": title_str,
        "titleHtml": title_html,
        "subtitle": subtitle_str,
        "subtitleHtml": subtitle_html,
        "content": content_str,
        "contentHtml": content_html,
        "abstract": abstract.strip()
    }


def get_all_news_by_date(giving_date):
    """
    根据指定日期获取所有的不相同的新闻列表
    :param giving_date:
    :return:
    """
    url, date_str = utils.get_paper_url(giving_date, type="新华每日电讯")
    # 获取报纸各版面信息
    unique_news_url_list = get_all_news_in_paper(date_str, url, config.Xinhua_Paper_Selectors['section_list_selector'])
    return unique_news_url_list


def save_detail_new_by_date(new_model, giving_date):
    """
    保存指定日期对应的所有新闻详情
    :param new_model: 新闻模型
    :param giving_date: datetime型，指定的日期
    :return:
    """
    unique_news_url_list = get_all_news_by_date(giving_date)
    for new in unique_news_url_list:
        if new['title'].strip() == "图片":
            continue
        new_info = analysis_new(new['url'])  # 分析网址内容
        if len(new_info['content']) < 150:
            continue
        new_model.save(new, new_info)
    print("《新华每日电讯》({})保存完毕, 共保存{}条新闻".format(giving_date, len(unique_news_url_list)))


def collect_xinhua_paper(start_date, collect_num):
    new_model = News(source="新华每日电讯")  # 存储模型
    date_list = utils.generate_date_list(start_date, collect_num)  # 获得日期列表
    for date in date_list:
        save_detail_new_by_date(new_model, date)
    print("《新华每日电讯》采集完成！")


if __name__ == "__main__":
    start_date = datetime.date(2022, 2, 1)  # 给定日期
    collect_xinhua_paper(start_date, 90)
