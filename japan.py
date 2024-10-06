import requests
from bs4 import BeautifulSoup
import subprocess
import time
import os
import re
import sys


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


def getDesc(folder_path):
    excluded = {"OFJE-264.HD"}
    for f in os.listdir(folder_path):
        if f in excluded:
            continue
        full = os.path.join(folder_path, f)
        if os.path.isdir(full):
            for subfile in os.listdir(full):
                if subfile.endswith(".mp4"):
                    old = os.path.join(full, subfile)
                    new = os.path.join(folder_path, subfile)
                    os.rename(old, new)
                    print(f"moved: {subfile}")

    for filename in os.listdir(folder_path):
        match = re.search(r"([A-Za-z]+-\d+)_", filename)
        if filename.endswith(".mp4") and not match:
            match = re.search(r"([A-Za-z]+-\d+)", filename)
            if match:
                code = match.group(1)
                search_url = f"https://tokyolib.com/search?type=id&q={code}"
                response = requests.get(search_url)
                soup = BeautifulSoup(response.content, "html.parser")

                work_title = soup.find("h4", class_="work-title")
                if work_title:
                    desc = work_title.text.replace(" ", "")
                    new_filename = f"{code}_{desc}.mp4"
                    old_path = os.path.join(folder_path, filename)
                    new_path = os.path.join(folder_path, new_filename)
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                else:
                    print(f"No description found for {filename}")
                time.sleep(30)
            else:
                print(f"No valid code found in {filename}")


def format(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            match = re.search(r"([A-Za-z]+-\d+)", filename)
            if match:
                code = match.group(1)
                if code == code.upper():
                    continue
                new_filename = filename.replace(code, code.upper())
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"No valid code found in {filename}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        param = sys.argv[2]
        print(f"param={param}")
        if param == "format":
            format(folder_path)
        elif param == "desc":
            getDesc(folder_path)
    else:
        main()
