import math
import os
import time
from collections import deque

import cv2
import numpy as np

from airtestProject.airtest.core import api as air
from airtestProject.airtest.core.helper import G
from airtestProject.airtest.core.android.recorder import Recorder
from airtestProject.airtest.report.report import LogToHtml
import multiprocessing
import time
from airtestProject.commons.utils.logger import log
from airtestProject.commons.utils.tools import coordinate_transformation
from airtestProject.factory.operateFactory import operate
import threading
import time

quest_date = {
    10110101: (488, 1531),
    10110102: (460, 1053),
    10110103: (578, 1105),
}

snp_list = [(slice(884, 939), slice(412, 705))]

null_pos = [0.7, 0.45]  # 空位置
close_pos = [0.8, 0.16]  # 关闭位置
move_init_pos = [0.15, 0.75]  # 摇杆默认位置
move_forward_pos = [0.15, 0.65]  # 摇杆向前移动位置
move_backward_pos = [0.15, 0.85]  # 摇杆向后移动位置
move_left_pos = [0.05, 0.75]  # 摇杆向左移动位置
move_right_pos = [0.25, 0.75]  # 摇杆向右移动位置

class QuestPage:
    def __init__(self, adb, script_root, Project=None, log_path=None):
        self.adb = adb
        self.device = G.DEVICE
        if Project is not None:
            operate('air').set_dict(script_root, Project)
        if log_path is not None:
            self.log_path = log_path
        else:
            self.log_path = None

    def get_current_resolution(self):
        w, h = self.device.get_current_resolution()
        return w, h

    def extract_coordinates(self, text):
        parts = text.split('.')
        if ' ' in text:
            # 包含空格
            x = parts[0]
            y = parts[-2].split()[-1]
        else:
            # 不包含空格
            x = parts[0]
            y = parts[2][1:]

        return x, y

    def get_now_pos(self, close_pos, snp, fun_name="air"):
        operate(fun_name).click("GM")
        operate(fun_name).sleep(0.1)
        operate(fun_name).click(null_pos)
        operate(fun_name).sleep(1.5)
        screen = self.device.snapshot()
        image_np = np.array(screen)
        image = image_np[snp[0]]
        str_text = operate(fun_name).get_text(image)[0].get("text")
        log.step(f"拿不到？？？？？{str_text}")
        now_pos_x, now_pos_y = self.extract_coordinates(str_text)
        operate(fun_name).click(close_pos)
        return now_pos_x, now_pos_y

    def get_quest_pos(self, quest_id):
        quest_pos = quest_date.get(quest_id)
        if quest_pos is None:
            log.error(f"剧情坐标未配置: {quest_id}")
        quest_pos_x, quest_pos_y = quest_pos[0], quest_pos[1]
        log.step(f"当前剧情：{quest_id}, 坐标为({quest_pos_x}, {quest_pos_y})")
        return quest_pos_x, quest_pos_y

    def test_fov(self, quest_id, fun_name="air"):
        x2_1, y2_1 = self.get_now_pos(close_pos, snp_list)
        log.step(f"当前坐标{x2_1, y2_1}")
        x1_3, y1_3 = move_backward_pos[0], move_backward_pos[1]
        log.step(f"摇杆向后移动坐标{x1_3, y1_3}")
        operate(fun_name).swipe_plus((move_init_pos[0], move_init_pos[1]),
                                     (move_forward_pos[0], move_forward_pos[1]), down_event_sleep=0.5)
        x2_2, y2_2 = self.get_now_pos(close_pos, snp_list)
        log.step(f"人物移动后坐标{x2_2, y2_2}")
        x3_1, y3_1 = self.get_quest_pos(quest_id)
        operate(fun_name).swipe_plus((move_init_pos[0], move_init_pos[1]),
                                     (move_backward_pos[0], move_backward_pos[1]), down_event_sleep=0.5)

        now_pos_x, now_pos_y = self.get_now_pos(close_pos, snp_list)
        log.step(f"现在当前坐标{now_pos_x, now_pos_y}")
        log.step(f"摇杆向左移动坐标{move_left_pos[0], move_left_pos[1]}")
        operate(fun_name).swipe_plus((move_init_pos[0], move_init_pos[1]),
                                     (move_left_pos[0], move_left_pos[1]), down_event_sleep=0.5)
        now_pos_x1, now_pos_y2 = self.get_now_pos(close_pos, snp_list)
        log.step(f"人物移动后坐标{now_pos_x1, now_pos_y2}")
        log.step(f"摇杆向右移动坐标{move_right_pos[0], move_right_pos[1]}")
        operate(fun_name).swipe_plus((move_init_pos[0], move_init_pos[1]), (move_right_pos[0], move_right_pos[1]),
                                     down_event_sleep=0.5)
        operate(fun_name).sleep(2.0)
        log.step(f"剧情坐标{x3_1, y3_1}")
        kx, ky, end_time = coordinate_transformation((float(x2_1), float(y2_1)),
                                                     (float(x2_2), float(y2_2)),
                                                     (float(now_pos_x1), float(now_pos_y2)),
                                                     (float(x3_1), float(y3_1)), 0.5, move_init_pos, 0.1)
        log.step(f"计算后摇杆需要滑动的坐标{kx, ky}")
        operate(fun_name).swipe_plus((move_init_pos[0], move_init_pos[1]), (kx, ky), down_event_sleep=end_time)
        now_pos_x3, now_pos_y3 = self.get_now_pos(close_pos, snp_list)
        log.step(f"现在当前坐标{now_pos_x3, now_pos_y3}")

    def thread_click_skip(self, pos, stop_event, fun_name="air"):
        while not stop_event.is_set():
            if not operate(fun_name).exists(pos):
                operate(fun_name).sleep(1)
            operate(fun_name).click(pos)

    def thread_main(self, pos, stop_event, fun_name="air"):
        for i in range(10):
            if not operate(fun_name).exists(pos):
                stop_event.set()

    @log.wrap("执行剧情流程")
    def do_quest(self, quest_id):
        log.step(f"进入剧情-{quest_id}")
        stop_event = threading.Event()

        t1 = threading.Thread(target=self.thread_click_skip, args=("跳过", stop_event))
        t2 = threading.Thread(target=self.thread_main, args=("自动", stop_event,))

        t1.start()
        t2.start()

        t2.join()
        t1.join()


if __name__ == '__main__':
    from airtestProject.airtest.core.android.adb import ADB
    from airtestProject.airtest.core import api as air
    from airtestProject.manager.DeviceManager import DeviceManager, uwa_auto_setup

    file_path = __file__
    # uwa_auto_setup()  # uwa pipline启动方法
    project_device = DeviceManager()
    log_path = project_device.auto_setup(file_path, logdir=True)  # 在uwa模式下不自己生成报告

    adb = ADB(air.device().adb.serialno)

    quest_page = QuestPage(adb, __file__, Project="rd", log_path=log_path, )
    # quest_page.get_current_resolution()
    quest_page.test_fov(10110103)
    # x1_1, y1_1 = move_init_pos[0], move_init_pos[1]
    # x1_2, y1_2 = move_forward_pos[0], move_forward_pos[1]
    # x2_1, y2_2 = quest_page.get_now_pos(10110101, close_pos, snp_list)

    # 执行任务
    # quest_page.do_quest(quest_id="10011010")
