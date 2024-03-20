# -*- coding: UTF-8 -*-
"""
__Author__ = "Draco-111"
__Version__ = "2.0.0"
__Description__ = "大麦app抢票自动化"
__Created__ = 2024/3/20 10:20
"""

# ！！！！使用前请将要看的内容加入到预选
# ！！！！确定好观影人和场次
# 大麦app将自动识别张数和观影人


from time import sleep
from time import time


from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from config import Config

# 加载配置信息
config = Config.load_config()

device_app_info = AppiumOptions()
# 操作系统
device_app_info.set_capability('platformName', 'Android')
# 操作系统版本
device_app_info.set_capability('platformVersion', '12')
# 设备名称
device_app_info.set_capability('deviceName', 'RF8M80RVNBJ')
# app package
device_app_info.set_capability('appPackage', 'cn.damai')
# app activity name
device_app_info.set_capability('appActivity', '.launcher.splash.SplashMainActivity')
# 使用unicode输入
device_app_info.set_capability('unicodeKeyboard', True)
# 隐藏键盘
device_app_info.set_capability('resetKeyboard', True)
# 不重置app
device_app_info.set_capability('noReset', True)
# 超时时间
device_app_info.set_capability('newCommandTimeout', 6000)
# 使用uiautomator2驱动
device_app_info.set_capability('automationName', 'UiAutomator2')

# 连接appium server，server地址查看appium启动信息
driver = webdriver.Remote(config.server_url, options=device_app_info)

sleep(5)

# 设置等待时间，等待1s
driver.implicitly_wait(5)
# 空闲时间10ms,加速
driver.update_settings({"waitForIdleTimeout": 10})

# 点击搜索框
driver.find_element(by=By.ID, value='cn.damai:id/channel_search_text').click()

# 输入搜索关键词
driver.find_element(by=By.ID, value='cn.damai:id/header_search_v2_input').send_keys(config.keyword)

# 获取搜索的全名
driver.find_element(by=By.XPATH,
                    value='//androidx.recyclerview.widget.RecyclerView[@resource-id="cn.damai:id/search_v2_suggest_recycler"]/android.widget.RelativeLayout[1]').click()

# 点击结果列表的第一个
driver.find_element(by=By.XPATH,
                    value='(//android.widget.LinearLayout[@resource-id="cn.damai:id/ll_search_item"]/android.widget.LinearLayout)').click()

# element = driver.find_element(by=By.XPATH,
#                     value='//android.widget.TextView[@resource-id="cn.damai:id/goto_setinfo_tv2"]').text

# count= 0
users = config.users
strat_time = config.start_time

 # 刷新页面
driver.swipe(500, 400, 500, 2000, 300)

# 比较当前时间 和 开始售卖 两个时间戳
while True:
    if int(time.time()) >= strat_time:
        print("准备开抢")

        while True: 
            try:
                # 寻找确定按钮 没有则狂点立即购买按钮
                driver.find_element(by=By.XPATH,
                        value='//android.widget.TextView[@text="确定"]')
                break
            except NoSuchElementException:
                # 狂点立即购买按钮 按钮已经被隐藏，模拟短快坐标滑动
                driver.swipe(750, 2065, 800, 2067, 100)
        # 跳出抢票时间检查
        break


while True:
    try:
        # 寻找提交订单按钮 没有则狂点确定按钮
        driver.find_element(by=By.XPATH,
                 value='//android.widget.TextView[@text="提交订单"]')
    except NoSuchElementException:
        # 狂点确定按钮
        driver.find_element(by=By.XPATH,
                        value='//android.widget.TextView[@text="确定"]').click()
        # Todo 下方解决网络问题