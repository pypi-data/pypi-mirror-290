"""
def focus_mumu()

def click(
    xy: tuple[int, int],
    before_click_time: float = 0,
    after_click_time: float = 0,
    click_count: int = 1,
    enable_dbclick: bool = False,
    move_duration: float = 0.8,
)

def get_image_coordinate(
    image_path: str, region: tuple[int, int, int, int] = None, confidence: float = 0.85
) -> tuple[int, int] | None

def click_image(
    image_path: str,
    before_click_time: float = 0,
    region: tuple[int, int, int, int] = None,
    enable_dbclick: bool = False,
    move_duration: float = 0.8,
    confidence: float = 0.85,
    wait_for_image_appear: bool = True,
    wait_timeout: float = 1,
) -> tuple[int, int] | None
"""

import random

import pyautogui as pag
import win32con
import win32gui
from PIL import Image

from qfpy.log import logger


def focus_mumu():
    hwnd = win32gui.FindWindow(None, "MuMu模拟器12")

    win32gui.SetForegroundWindow(hwnd)
    # 缩小：SW_RESTORE
    # 放大：SW_MAXIMIZE
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    pag.sleep(0.5)


def click(
    xy: tuple[int, int],
    before_click_time: float = 0,
    after_click_time: float = 0,
    click_count: int = 1,
    enable_dbclick: bool = False,
    move_duration: float = 0.8,
):
    """点击坐标

    Arguments:
        xy {tuple[int, int]} -- 坐标

    Keyword Arguments:
        before_click_time {float} -- 点击前 延迟时间。如果为 0，随机等待 0.3~0.6 秒
        after_click_time {float} -- 点击后 延迟时间
        click_count {int} -- 点击次数 (default: {1})
        enable_dbclick {bool} -- 是否双击 (default: {False})
        move_duration {float} -- 移动时间 (default: {0.8})
    """
    x, y = xy

    pag.moveTo(x, y, duration=move_duration)

    if before_click_time == 0:
        before_click_time = random.uniform(0.3, 0.6)

    for _ in range(click_count):
        pag.sleep(before_click_time)

        if enable_dbclick:
            pag.doubleClick(x, y)
        else:
            pag.click(x, y)

        if after_click_time > 0:
            pag.sleep(after_click_time)


def get_image_coordinate(
    image_path: str, region: tuple[int, int, int, int] = None, confidence: float = 0.85
) -> tuple[int, int] | None:
    """获取图片坐标

    Arguments:
        image_name {str} -- 图片路径

    Keyword Arguments:
        region {tuple[int, int, int, int]} -- 识别区域（左，上，宽，高）(default: {None})
        confidence {float} -- 准确度 (default: {0.85})

    Returns:
        tuple[int, int] | None -- 图片坐标
    """
    try:
        img = Image.open(image_path)
        point = pag.locateCenterOnScreen(
            img,
            confidence=confidence,
            region=region,
        )
        img.close()
        return tuple(point)
    except pag.ImageNotFoundException:
        return None


def click_image(
    image_path: str,
    before_click_time: float = 0,
    after_click_time: float = 0,
    region: tuple[int, int, int, int] = None,
    enable_dbclick: bool = False,
    move_duration: float = 0.8,
    confidence: float = 0.85,
    wait_for_image_appear: bool = True,
    wait_timeout: float = 1,
) -> tuple[int, int] | None:
    """点击图片

    默认一直等待图片出现，1 秒超时，返回 None

    否则识别一次图片，如果没找到，返回 None

    Arguments:
        image_path {str} -- 图片路径

    Keyword Arguments:
        before_click_time {float} -- 点击前 延迟时间 (default: {0})
        region {tuple[int, int, int, int]} -- 识别区域（左，上，宽，高） (default: {None})
        enable_dbclick {bool} -- 启用双击 (default: {False})
        move_duration {float} -- 移动时间 (default: {0.8})
        confidence {float} -- 图片识别准确度 (default: {0.85})
        wait_for_image_appear {bool} -- 等待图片出现 (default: {True})
        wait_timeout {float} -- 等待超时 时间 (default: {2})

    Returns:
        tuple[int, int] -- 图片坐标
    """

    # 默认一直等待图片出现
    if wait_for_image_appear:
        while True:
            # 等待超时
            if wait_timeout <= 0:
                logger.error("等待图片超时：" + image_path)
                return None

            xy = get_image_coordinate(image_path, region, confidence)
            if xy:
                break
            pag.sleep(0.1)
            wait_timeout -= 0.1
    # 只识别一次
    else:
        xy = get_image_coordinate(image_path, region, confidence)
        # 找不到图片，返回 None
        if not xy:
            return None

    # 随机偏移坐标，再点击
    xy = (
        xy[0] + random.randint(-5, 5),
        xy[1] + random.randint(-5, 5),
    )
    click(
        xy,
        before_click_time=before_click_time,
        after_click_time=after_click_time,
        enable_dbclick=enable_dbclick,
        move_duration=move_duration,
    )
    logger.info(f"点击图片：{image_path} {xy}")
    return xy
