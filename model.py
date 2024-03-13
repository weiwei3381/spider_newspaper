# coding: utf-8
# @Time : 2021/12/18 19:13
# @Author : wowbat
# @File : model.py
# @Describe:

from peewee import *
import json
import datetime
import config

db = SqliteDatabase(config.DATABASE_FILE)  # 初始化数据库对象


class NewsModel(Model):
    title = CharField(max_length=128)  # 标题
    titleHtml = TextField(null=True)  # 原标题的HTML
    date = DateField(null=True)  # 报导时间
    section = CharField(max_length=16)  # 新闻版面
    url = CharField(max_length=128)  # url链接

    subtitle = CharField(max_length=64, null=True)  # 副标题
    subtitleHtml = TextField(null=True)  # 副标题
    content = TextField()  # 新闻内容
    contentHtml = TextField()  # 新闻内容的html
    abstract = TextField(null=True)  # 概述

    source = CharField(max_length=16, null=True)  # 新闻来源，新增加的选项

    class Meta:
        database = db


class News:
    def __init__(self, source="解放军报"):
        """
        初始化方法，需要根据新闻来源不同进行传入，默认为解放军报
        :param source:
        """
        # db.connect()  # 显式地连接数据库
        self.source = source  # 新闻来源

    def get_all_news_map(self):
        all_news_map = {}
        news_records = NewsModel.select(NewsModel.date, NewsModel.title).where(NewsModel.source == self.source)
        for record in news_records:
            news_key = "%s_%s" % (record.title, record.date)
            if news_key not in all_news_map:
                all_news_map[news_key] = 1
        return all_news_map

    def get_all_news_date(self):
        all_date = {}
        news_records = NewsModel.select(NewsModel.date).where(NewsModel.source == self.source)
        for record in news_records:
            date_key = "%s" % (record.date,)
            if date_key not in all_date:
                all_date[date_key] = 1
        return all_date

    def get_news_by_date(self, date):
        """
        根据日期获得传入参数的报纸数据
        :param date: 日期，例如“2021-09-01”
        :return:
        """
        news_records = NewsModel.select().where(
            (NewsModel.date == date) &
            (NewsModel.source == self.source)) \
            .order_by(NewsModel.section)
        return [news for news in news_records]

    def get_news_about_war(self, date):
        """
        获得所有跟俄乌冲突相关的新闻报导
        :param string date: 给定的某一天
        :return List: 当天涉及到的新闻列表
        """
        records = NewsModel.select().where(
            (NewsModel.date == date) &
            (NewsModel.title ** '%俄%' | NewsModel.title ** '%乌%' | NewsModel.title ** '%美%' |
             NewsModel.title ** '%欧%' | NewsModel.title ** '%战%' | NewsModel.title ** '%冲突%')
        )
        return [news for news in records]

    def get_military_news_by_date(self, date):
        """
        根据日期获得传入参数的军事报纸数据
        :param date: 日期，例如“2021-09-01”
        :return:
        """
        news_records = NewsModel.select().where(
            (NewsModel.date == date) &
            ((NewsModel.source == "解放军报") | (NewsModel.source == "国防报"))) \
            .order_by(NewsModel.section)
        return [news for news in news_records]

    def get_local_news_by_date(self, date):
        """
        根据日期获得传入参数的各地报纸数据
        :param date: 日期，例如“2021-09-01”
        :return:
        """
        news_records = NewsModel.select().where(
            (NewsModel.date == date) &
            ((NewsModel.source == "光明日报") | (NewsModel.source == "新华每日电讯") | (NewsModel.source == "新华每日电讯") | (
                    NewsModel.source == "北京青年报") | (NewsModel.source == "天津日报") | (NewsModel.source == "成都商报") | (
                     NewsModel.source == "南国都市报") | (NewsModel.source == "香港文汇报") | (NewsModel.source == "现代快报") | (
                     NewsModel.source == "每日新报"))) \
            .order_by(NewsModel.section)
        return [news for news in news_records]

    def get_all_news_by_date(self, date):
        """
        根据日期获得所有的报纸数据
        :param date: 日期，例如“2021-09-01”
        :return:
        """
        news_records = NewsModel.select().where(NewsModel.date == date) \
            .order_by(NewsModel.section)
        return [news for news in news_records]

    def get_last_date(self):
        """
        获得数据库中最后的日期
        :return:
        """
        news_records = NewsModel.select(NewsModel.date) \
            .where(NewsModel.source == self.source) \
            .order_by(NewsModel.date.desc()).limit(1)
        return [news.date for news in news_records][0]

    def get_early_date(self):
        """
        获得数据库中最新的日期
        :return:
        """
        news_records = NewsModel.select(NewsModel.date) \
            .where(NewsModel.source == self.source) \
            .order_by(NewsModel.date).limit(1)
        return [news.date for news in news_records][0]

    def get_all_date(self):
        """
        获得报纸对应的所有日期
        :return:
        """
        records = NewsModel.select(NewsModel.date) \
            .where(NewsModel.source == self.source) \
            .group_by(NewsModel.date) \
            .order_by(NewsModel.date.desc())
        return [record.date for record in records]

    def save(self, new, newInfo):
        data = {
            "date": new['date'],
            "section": new['section'],
            "title": new['title'],
            "url": new['url'],
            "source": self.source,
            "titleHtml": newInfo['titleHtml'],
            "subtitle": newInfo['subtitle'],
            "subtitleHtml": newInfo['subtitleHtml'],
            "content": newInfo['content'],
            "contentHtml": newInfo['contentHtml'],
            "abstract": newInfo['abstract'],

        }
        NewsModel.create(**data)


class Inserter():
    """
    数据的插入类
    主要用于把json数据插入到数据库中
    """
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = []  # 需要插入的数据
        self.batch_num = 20  # 一次插入的数据量大小

    def set_data(self):
        all_news_map = News.get_all_news_map()  # 获得所有已有新闻的map
        news_data = []
        with open(self.json_file_path, mode='r', encoding="utf-8") as json_file:
            news_records = json.load(json_file)
            for news_record in news_records:
                new_key = "%s_%s" % (news_record['new']['title'], news_record['new']['date'])
                if new_key in all_news_map:
                    continue
                print("" * 6, new_key, "-" * 6)
                news_data.append({
                    "date": news_record['new']['date'],
                    "section": news_record['new']['section'],
                    "title": news_record['new']['title'],
                    "url": news_record['new']['url'],
                    "titleHtml": news_record['newInfo']['titleHtml'],
                    "subtitle": news_record['newInfo']['subtitle'],
                    "subtitleHtml": news_record['newInfo']['subtitleHtml'],
                    "content": news_record['newInfo']['content'],
                    "contentHtml": news_record['newInfo']['contentHtml'],
                    "abstract": news_record['newInfo']['abstract'],
                })
            self.data = news_data

    def init_database(self):
        db.create_tables([NewsModel])  # 创建表结构
        self.set_data()
        insert_fields = ['date', 'section', 'title', 'url', 'titleHtml', 'subtitle',
                         'subtitleHtml', 'content', 'contentHtml', 'abstract']  # 插入用到的属性列表
        with db.atomic():
            for idx in range(0, len(self.data), self.batch_num):
                NewsModel.insert_many(self.data[idx:idx + self.batch_num], fields=insert_fields).execute()


if __name__ == "__main__":
    # inserter = Inserter(r"D:\py_projects\spider\allInfo_20200630.json")
    # inserter.init_database()
    new_db = News()
    # records = new_db.get_news_about_war('2022-02-02')
    print(new_db.get_all_date())
    # new_db = News()
    # dates = new_db.get_all_date()
    # for date in dates:
    #     print(date)
    # news_records = new_db.get_news_by_date("2021-08-01")
    # for record in records:
    #     print(record.date, record.section, record.title)
