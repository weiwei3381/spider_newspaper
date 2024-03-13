# coding: utf-8
# @Time : 2021/12/19 22:39
# @Author : wowbat
# @File : spider.py
# @Describe: 爬取并保存所有内容

from collect import defense_paper, people_paper, PLA_paper, guangming_paper, xinhua_paper, science_paper, beijing_paper, \
    tianjin_paper, chengdu_paper, hainan_paper, xuexi_paper, HongKong_paper, modern_paper, xin_paper
import datetime
import model


def collect_all_news(collect_num):
    """
    采集所有报纸
    :param collect_num: 采集的天数
    :return:
    """
    # 从数据库中获取采集的开始时间
    last_date = model.News().get_last_date()  # 数据库中最新日期
    start_date = last_date + datetime.timedelta(days=1)
    print("数据库的最新日期是{}".format(last_date))

    PLA_paper.collect_PLA_paper(start_date, collect_num)  # 解放军报
    people_paper.collect_people_paper(start_date, collect_num)  # 人民日报
    defense_paper.collect_defense_paper(start_date, collect_num)  # 国防报
    guangming_paper.collect_guangming_paper(start_date, collect_num)  # 光明日报
    xinhua_paper.collect_xinhua_paper(start_date, collect_num)  # 新华每日电讯
    science_paper.collect_science_paper(start_date, collect_num)  # 科技日报
    xuexi_paper.collect_xuexi_paper(start_date, collect_num)  # 科技日报
    beijing_paper.collect_beijing_paper(start_date, collect_num)  # 北京青年报
    tianjin_paper.collect_tianjin_paper(start_date, collect_num)  # 天津日报
    chengdu_paper.collect_chengdu_paper(start_date, collect_num) # 成都商报
    hainan_paper.collect_hainan_paper(start_date, collect_num)  # 南国都市报
    modern_paper.collect_moder_paper(start_date, collect_num)  # 现代快报
    xin_paper.collect_xin_paper(start_date, collect_num)  # 每日新报
    HongKong_paper.collect_HongKong_paper(start_date, collect_num)  # 香港文汇报


if __name__ == "__main__":
    collect_all_news(30)
    # xin_paper.collect_xin_paper(datetime.date(2023, 8, 29), 30)  # 每日新报
