import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

now = datetime.now()
year = now.year
month = now.month
day = now.day

validHrefs = []


def getTarget(target):
    res = requests.get(url=target)
    if res.status_code == 200:
        html = BeautifulSoup(res.text, "html.parser")
        div = html.find(id="conttpc")

        textContent = ""
        for elem in div.contents:
            if isinstance(elem, str):
                textContent += elem
            elif elem.name == "img":
                elem["src"] = elem["ess-data"]
                textContent += str(elem)
            elif elem.name == "h5":
                print("exit" + str(elem))
                break
            else:
                textContent += str(elem)
        href = div.find(id="rmlink")
        textContent += str(href)

        fileName = "{0}.{1}.{2}.html".format(year, month, day)
        file = open(fileName, "a", encoding="utf-8")
        file.write(textContent)
        file.close()


def getPage(page):
    res = requests.get(page)
    if res.status_code == 200:
        html = BeautifulSoup(res.text, "html.parser")
        targets = html.find_all(class_="tal")
        for target in targets:
            urls = target.find_all("a")
            for url in urls:
                href = url["href"]
                m = month if month >= 10 else "0{0}".format(month)
                m = "07"
                y = year % 100
                start = "htm_data/{0}{1}".format(y, m)
                if href.startswith(start):
                    validHrefs.append(href)


def changeScale(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "lxml")

    style_tag = soup.new_tag("style")
    style_tag.string = """
    .scaled-image {
        transform: scale(0.5);
    }
    """
    if soup.head:
        print("has head")
        soup.head.append(style_tag)
    else:
        head_tag = soup.new_tag("head")
        head_tag.append(style_tag)
        if soup.html:
            soup.html.insert(0, head_tag)

    for img in soup.find_all("img"):
        img["class"] = img.get("class", []) + ["scaled-image"]

    fileName = "{0}.{1}.{2}-scaled.html".format(year, month, day)
    with open(fileName, "w", encoding="utf-8") as file:
        file.write(str(soup))


if __name__ == "__main__":
    for i in range(1, 4):
        page = "https://www.t66y.com/thread0806.php?fid=25&search=&page={0}".format(i)
        getPage(page)

    print("got %d valid hrefs:" % len(validHrefs))
    print("\n".join(validHrefs))

    for i in range(0, len(validHrefs)):
        href = validHrefs[i]
        print("request url %s (%d/%d)" % (href, i + 1, len(validHrefs)))
        target = "https://t66y.com/{0}".format(href)
        getTarget(target)
        print("sleeping...")
        if i % 10 == 0:
            time.sleep(100)
        else:
            time.sleep(30)

    fileName = "{0}.{1}.{2}.html".format(year, month, day)
    # changeScale(fileName)
