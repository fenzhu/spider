import requests
from bs4 import BeautifulSoup
import subprocess
import time


def get_magnet_link(code):
    search_url = f"https://tokyolib.com/search?type=id&q={code}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # 查找详细信息链接
    detail_link = soup.find("a", class_="work")["href"]
    detail_url = f"https://tokyolib.com{detail_link}"
    # print("detail url is " + detail_url)
    # 访问详细信息页面
    detail_response = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_response.content, "html.parser")

    # 获取磁力链接
    magnet_link = detail_soup.find("div", class_="magnet").find("a")["href"]
    # print("magnet link is " + magnet_link)
    return magnet_link


def download_magnet(magnet_link):
    # 使用迅雷下载
    subprocess.run(
        ["thunderstart", magnet_link], shell=True
    )  # 请确保迅雷的路径已加入系统环境变量


def main():
    with open("input.txt", "r") as file:
        codes = file.read().strip().splitlines()

    for code in codes:
        print(code)
        magnet_link = get_magnet_link(code)
        print(f"Downloading: {magnet_link}")
        download_magnet(magnet_link)
        time.sleep(30)  # 为了避免请求过于频繁


if __name__ == "__main__":
    main()
