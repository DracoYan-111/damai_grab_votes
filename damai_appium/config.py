# -*- coding: UTF-8 -*-
"""
__Author__ = "Draco-111"
__Version__ = "2.0.0"
__Description__ = "配置类"
__Created__ = 2024/3/20 10:20
"""
import json


class Config:
    def __init__(self, server_url, keyword, users, city, date, price, if_commit_order):
        self.server_url = server_url
        self.keyword = keyword
        self.users = users
        self.city = city
        self.date = date
        self.price = price
        self.if_commit_order = if_commit_order

    @staticmethod
    def load_config():
        with open('./config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
        return Config(config['server_url'],
                      config['keyword'],
                      config['users'],
                      config['city'],
                      config['date'],
                      config['price'],
                      config['if_commit_order'])
