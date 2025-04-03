import argparse
import re
import logging
import urllib.request

import requests
from pytubefix import Channel

import po_token

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def get_latest_video_description(channel_username, po_token=None):
    """
    通过pytube获取频道最新视频信息
    :param po_token:
    :param channel_username: YouTube频道用户名
    :return: (视频标题, 视频简介)
    """
    # 创建频道对象
    if po_token:
        channel = Channel(f"https://youtube.com/channel/{channel_username}", po_token)
    else:
        channel = Channel(f"https://youtube.com/channel/{channel_username}")

    # 获取视频列表
    videos = channel.videos

    # 获取最新视频（按发布时间排序）
    latest_video = videos[0]

    return {
        "title": latest_video.title,
        "description": latest_video.description,
        "url": latest_video.watch_url
    }


def extract_link_after_keyword(text, keyword):
    """
    从文本中提取指定关键词后的第一个完整链接
    :param text: 待搜索文本
    :param keyword: 关键词
    :return: 匹配的链接或None
    """
    # 查找关键词位置
    start_idx = text.find(keyword)
    if start_idx == -1:
        return None

    # 截取关键词之后的内容
    search_text = text[start_idx + len(keyword):]

    # 正则匹配第一个完整URL
    url_pattern = re.compile(r'https?://[^\s"\'<>]+')
    match = url_pattern.search(search_text)
    return match.group(0) if match else None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--is_github_action', action='store_true', help='是否是在GitHub Action中运行')
    is_github_action = parser.parse_args().is_github_action

    # 使用示例
    username = "UCOQ5AdvDNOfyEAJY5SDXVZg"  # 替换为目标频道用户名
    if is_github_action:
        logging.info("正在运行在GitHub Action中")
        result = get_latest_video_description(username, po_token=po_token.po_token_verifier())
    else:
        result = get_latest_video_description(username)

    if not result:
        logging.error("未能获取视频信息")
        exit(1)

    logging.info(f"最新视频标题: {result['title']}")
    logging.info(f"视频链接: {result['url']}")
    logging.info(f"视频简介: {result['description']}")

    kwd_free_node = '免费节点获取地址'
    if kwd_free_node not in result['description']:
        logging.error("未找到关键词")
        exit(1)

    blog_link = extract_link_after_keyword(result['description'], kwd_free_node)
    if not blog_link:
        logging.error("未能提取链接")
        exit(1)

    logging.info(f"提取的链接: {blog_link}")

    blog_resp = requests.get(blog_link)

    kwd_subscribe = 'Clash-meta 20.37版以后/Shadowrocket订阅'
    sub_link = extract_link_after_keyword(blog_resp.text, kwd_subscribe)
    logging.info(f'订阅链接: {sub_link}')

    urllib.request.urlretrieve(sub_link, 'sfzy.yaml')
    logging.info('下载完成')
