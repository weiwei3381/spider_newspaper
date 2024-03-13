# coding: utf-8
# @Time : 2021/12/18 19:37
# @Author : wowbat
# @File : model_migrate.py
# @Describe: 数据库迁移文件，用来修改数据库的结构

from playhouse.migrate import *
import config


db = SqliteDatabase(config.DATABASE_FILE)
migrator = SqliteMigrator(db)  # 数据迁移对象


def add_source_field():
    """
    增加新闻来源属性
    :return:
    """
    source_field = CharField(max_length=16, null=True)  # 新闻来源域
    # 运行数据迁移模型，指定数据库表，字段名称和对应的域
    migrate(
        migrator.add_column('newsmodel', 'source', source_field),
        migrator.drop_not_null('newsmodel', 'section'),  # 使字段可以为空
            )


if __name__ == "__main__":
    add_source_field()