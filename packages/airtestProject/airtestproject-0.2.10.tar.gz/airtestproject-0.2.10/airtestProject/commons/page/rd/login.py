import os
import time
from collections import deque

from airtestProject.airtest.core import api as air
from airtestProject.airtest.core.android.recorder import Recorder
from airtestProject.airtest.report.report import LogToHtml
from airtestProject.airtest.core.android.adb import ADB
from airtestProject.airtest.core import api as air
from airtestProject.manager.DeviceManager import DeviceManager, uwa_auto_setup
from airtestProject.commons.utils.logger import log
from airtestProject.factory.operateFactory import operate
import random

# screen = G.DEVICE.snapshot()
# w, h= device().get_current_resolution() #获取手机分辨率
input_pos = [0.5, 0.66]
select_server_pos = [0.5, 0.72]
start_game_pos = [0.5,0.78]
role_man_pos = [0.69, 0.3]
role_men_pos = [0.3, 0.3]
enter_game_pos = [0.8, 0.8]




class LoginPage:

    def __init__(self, adb, script_root, Project=None, log_path=None):
        self.adb = adb
        if Project is not None:
            operate('air').set_dict(script_root, Project)
        if log_path is not None:
            self.log_path = log_path
        else:
            self.log_path = None

    @log.wrap("进入登陆页面")
    def check_enter_login_view(self, pos, fun_name="air"):
        self.adb.shell("logcat -c")
        if operate(fun_name).wait_element_appear(pos):
            log.step("进入登录界面成功")
            return True
        else:
            log.step("进入登录界面失败")
            adb_log = self.adb.shell("logcat -d Unity:W *:S")
            log.log_adb_out(adb_log)
            return False


    @log.wrap('输入账号')
    def input_account(self, account_pos, fun_name="air"):
        user = ''.join(str(random.randint(1, 9)) for _ in range(6))
        operate(fun_name).set_text(account_pos, user)
        log.step(f'输入账号-{user}')


    @log.wrap('选择服务器')
    def select_server(self, select_sever, server_list, server_name, fun_name="air"):
        operate(fun_name).click(select_sever)
        operate(fun_name).swipe((0.12, 0.5))  # 在0.1s内上划0.5个屏幕
        operate(fun_name).sleep(1.0)
        operate(fun_name).click(server_list)
        operate(fun_name).sleep(1.0)
        operate(fun_name).click(server_name)

    @log.wrap('点击开始游戏')
    def click_start_game(self, start_game, fun_name="air"):
        operate(fun_name).click(start_game)

    @log.wrap('点击选择角色')
    def click_role(self, role, fun_name="air"):
        operate(fun_name).wait_for_any(["RoleMan", "RoleWoman"])
        operate(fun_name).click(role)

    @log.wrap('点击进入游戏')
    def click_enter_game(self, last_click_pos,next_pos, fun_name="air"):
        operate(fun_name).wait_next_element(last_click_pos, next_pos)
        while True:
            if not operate(fun_name).exists(next_pos):
                break
            else:
                operate(fun_name).click(next_pos)
        operate(fun_name).sleep(10.0)


    def rd_login(self):
        self.check_enter_login_view("StartGameBtn")
        self.input_account(input_pos)
        self.select_server(select_server_pos,"外网服务器","技术中心测试服")
        self.click_start_game(start_game_pos)
        self.click_role("RoleMan")
        self.click_enter_game("RoleMan","ContinueBtn")


    def test(self,w ,h):
        self.click_enter_game("RoleMan","ContinueBtn")


if __name__ == '__main__':
    LoginPage.rd_login()