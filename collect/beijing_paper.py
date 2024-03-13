# coding: utf-8
# @Time : 2021/12/18 23:14
# @Author : wowbat
# @File : defense_paper.py
# @Describe:北京青年报自动下载

import datetime
import utils
import config
from bs4 import BeautifulSoup
from urllib import parse
from model import News


def get_section_in_paper(paper_url, section_list_selector):
    """
    获得报纸url中的各部分信息
    :param paper_url: 当天报纸主页的url链接
    :param section_list_selector: 获取部分的选择器
    :return: 各部分的信息列表, 每个信息包括name(版面信息, 如"第01版：头条")和url(版面对应的链接)
    """
    paper_html = utils.get_url_content(paper_url)  # 获得报纸html内容
    section_list = []  # 存储版面信息的列表, 最后会返回该列表
    soup = BeautifulSoup(paper_html, "lxml")
    section_node = soup.find(**section_list_selector)
    if section_node:
        section_nodes = section_node.find_all('a', id="pageLink")  # 获得所有版面节点
        for section_node in section_nodes:
            # 分析每个版面节点, 将其加入到版面信息列表中
            section_list.append(
                {
                    "name": section_node.text.strip(),
                    "url": parse.urljoin(paper_url, section_node.attrs['href'])
                }
            )
    return section_list


def get_news_in_section(section, paper_date, news_list_selector):
    section_html = utils.get_url_content(section['url'])
    soup = BeautifulSoup(section_html, "lxml")
    news_node = soup.find(**news_list_selector)
    news_list = []
    if news_node:
        news = news_node.find_all('a')
        for new in news:
            news_list.append(
                {"date": paper_date,
                 "section": section['name'],
                 "title": new.text.strip(),
                 "url": parse.urljoin(section['url'], new.attrs['href'])
                 }
            )
    return news_list


def analysis_new(new_url):
    """
    分析新闻
    :param new_url: 新闻网址
    :return: 返回解析后的新闻信息,包括标题, 副标题, 正文, 摘要和原始的html信息
    """
    html = utils.get_url_content(new_url)
    soup = BeautifulSoup(html, "lxml")
    title_node = soup.find('h1')
    subtitle_node = soup.find('p', class_='fbiaot')
    content_node = soup.find('div', class_='contnt')
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
        "abstract": abstract
    }


def get_all_news_by_date(giving_date):
    """
    根据指定日期获取所有的不相同的新闻列表
    :param giving_date:
    :return:
    """
    url, date_str = utils.get_paper_url(giving_date, type="北京青年报")
    # 获取报纸各版面信息
    section_list = get_section_in_paper(url, config.Beijing_Paper_Selectors['section_list_selector'])
    all_news_url_list = []  # 所有新闻列表
    # 遍历每个版块，将版块的新闻都放到所有新闻列表中
    for section in section_list:
        news_url_list = get_news_in_section(section, date_str,
                                            config.Beijing_Paper_Selectors['news_list_selector'])  # 获得news列表
        all_news_url_list.extend(news_url_list)  # 将列表加入到另一个列表中，使用extend方法
    unique_news_url_list = utils.delete_repeated_news(all_news_url_list)  # 得到唯一的新闻list
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
    print("《北京青年报》({})保存完毕, 共保存{}条新闻".format(giving_date, len(unique_news_url_list)))


def collect_beijing_paper(start_date, collect_num):
    new_model = News(source="北京青年报")  # 存储模型
    date_list = utils.generate_date_list(start_date, collect_num)  # 获得日期列表
    for date in date_list:
        try:
            save_detail_new_by_date(new_model, date)
        except Exception as e:
            print(e)
    print("《北京青年报》采集完成！")


if __name__ == "__main__":
    start_date = datetime.date(2022, 5, 9)  # 给定日期
    collect_beijing_paper(start_date, 1)
