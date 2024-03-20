# -*- coding: UTF-8 -*-
"""
__Author__ = "Draco-111"
__Version__ = "2.0.0"
__Description__ = "大麦app抢票自动化"
__Created__ = 2024/3/20 10:20
"""
from time import sleep

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
while True:
    try:
        # 使用 XPath 定位元素
        element = driver.find_element(by=By.XPATH,
                     value='//android.widget.TextView[@resource-id="cn.damai:id/goto_setinfo_tv2"]')

        print("未开放购买，操操操")
        # 如果找到了元素，则刷新
        driver.swipe(500, 400, 500, 2000, 300)
        # sleep(0.1)
        # count += 1
        # if count == 5:
        # # 测试，等待期间换成其他已经开放的
        #     sleep(5)
    except NoSuchElementException:
        # 如果找不到元素，则点击立即购买
        print("已开放购买，干干干")
        # 立即购买 按钮已经被隐藏，模拟短快坐标滑动
        driver.swipe(750, 2065, 800, 2067, 100)
        # 选则座位 ，模拟短快坐标滑动
        driver.swipe(560, 900, 590, 900, 100)
        # 检查观影人数并选择张数
        if len(config.users) > 1: 
            # >1，循环 人数-1 次
            for _ in range(len(config.users) - 1 ):
                # 点击 + 按钮
                driver.find_element(by=By.XPATH,
                    value='//android.widget.ImageView[@resource-id="cn.damai:id/img_jia"]').click()
        # 点击确定按钮
        driver.find_element(by=By.XPATH,
                    value='//android.widget.TextView[@text="确定"]').click()
        # 结束循环
        break

# 检查是否加载到选择观影人页面
while True:
    try:
        # 该元素出现即已经加载完成
        element = driver.find_element(by=By.XPATH,
                    value='//androidx.recyclerview.widget.RecyclerView[@resource-id="cn.damai:id/recycler_view"]/android.widget.FrameLayout[3]/android.widget.LinearLayout[1]')
        # 跳出本次检查
        break
    except NoSuchElementException:
        print("等待加载...")
        # 等待并继续检查
        continue

# 如果观影人较多
for user in config.users:
    # 从配置文件中获取观影人姓名
    driver.find_element(by=By.XPATH,
                    value='//android.widget.TextView[@resource-id="cn.damai:id/text_name" and @text="' + user + '"]').click()	
# 点击提交订单
driver.find_element(by=By.XPATH,
                    value='//android.widget.TextView[@text="提交订单"]').click()	


driver.quit()
