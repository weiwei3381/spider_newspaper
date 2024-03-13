# coding: utf-8
# @Time : 2021/12/18 19:39
# @Author : wowbat
# @File : config.py
# @Describe: 全局配置文件

import os

# 文件位置
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前项目绝对路径
DATABASE_FILE = os.path.join(PROJECT_DIR,'./data/record.db')  # 数据库文件位置
THEORY_KEY_WORDS_REGULAR = r"论坛|科技|评论|天下|时事|国际|前沿|理论|深读|观点|学习|讲坛|世界|观点"
STRICT_THEORY_KEY_WORDS_REGULAR = r"科技前沿|军事论坛|天下军事|国防科技|论坛|国际"  # 更加严格的军事理论版块
NEWS_KEY_WORDS_REGULAR = r'要闻'
TOP_PAPER_KEY_WORDS_REGULAR = r'第01版'

# 各类解析路径

# 国防报解析路径
Defense_Paper_Selectors = {
    # 版面列表节点选择器
    "section_list_selector": {
        "name": "ul",
        "attrs": {
            "id": "APP-SectionNav"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "attrs":{
            "id": "APP-NewsList"
        }
    },
}

# 人民日报解析路径
People_Paper_Selectors = {
    # 版面列表节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "class": "swiper-container"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "ul",
        "attrs":{
            "class": "news-list"
        }
    },
}

# 光明日报解析路径
Guangming_Paper_Selectors = {
    # 版面列表节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "id": "pageList"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs":{
            "id": "titleList"
        }
    },
}

# 解放军报解析路径
PLA_Paper_Selectors = {
    # 版面列表节点选择器
    "section_list_selector": {
        "name": "ul",
        "attrs": {
            "id": "APP-SectionNav"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "attrs": {
            "id": "APP-NewsList"
        }
    },
}

# 科技日报解析路径
Science_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "class": "bmname"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs": {
            "class": "title"
        }
    },
}

# 北京青年报解析路径
Beijing_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "id": "artcile_list_wapper"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "ul",
        "attrs": {
            "class": "jcul"
        }
    },
}

# 天津日报解析路径
Tianjin_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "table",
        "attrs": {
            "width": "98%"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "table",
        "attrs": {
            "width": "348"
        }
    },
}

# 成都商报解析路径
Chengdu_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "class": "pagenav-menulist"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs": {
            "class": "pagenav-menulist"
        }
    },
}

# 南国都市报解析路径
Hainan_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "table",
        "attrs": {
            "id": "bmdhTable"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs": {
            "id": "main-ed-articlenav-list"
        }
    },
}

# 新华每日电讯解析路径
Xinhua_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "class": "listdaohang"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs": {
            "class": "listdaohang"
        }
    },
}

# 学习时报解析路径
Xuexi_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "div",
        "attrs": {
            "id": "pageList"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "table",
        "attrs": {
            "width": "265"
        }
    },
}

# 每日新报解析路径
Xin_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "td",
        "attrs": {
            "width": "315"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "td",
        "attrs": {
            "width": "348"
        }
    },
}

# 现代快报解析路径
Modern_Paper_Selectors = {
    # 版面目录的节点选择器
    "section_list_selector": {
        "name": "td",
        "attrs": {
            "width": "293"
        }
    },

    # 报纸列表节点选择器
    "news_list_selector": {
        "name": "div",
        "attrs": {
            "id": "btdh"
        }
    },
}

