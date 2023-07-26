import os, sys, requests, json
import re
from bs4 import BeautifulSoup
from tqdm import tqdm


def getPageHtml(url: str) -> bytes:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "referer": "https://www.google.com/",
    }
    request = requests.get(url, headers=headers)
    print(request.status_code)
    return request.content


def sanitizeString(string: str) -> str:
    spacesRemoved = re.sub(r"[\s\/]", "_", string)
    return re.sub(r"[^\w]", "", spacesRemoved)


def getThreadTitle(url: str, soup: BeautifulSoup) -> str:
    thread_board = url.split("org/")[-1]

    subject_span = soup.select_one("span.subject")

    if not subject_span:
        return sanitizeString(thread_board)

    return sanitizeString(f"{thread_board}_{subject_span.text}")


def createFolder(path: str) -> None:
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def downloadImage(download_path: str, url: str) -> None:
    # if os.path.exists(download_path):
    #     return

    source = getPageHtml(url)

    with open(download_path, "wb") as image:
        image.write(source)


def scrape(url):
    createFolder("downloads")

    html = getPageHtml(url)
    soup = BeautifulSoup(html, "lxml")

    thread_title = getThreadTitle(url, soup)

    folder_path = os.path.join("downloads", thread_title)
    createFolder(folder_path)

    img_anchor = soup.find_all("a", {"class": "fileThumb"}, href=True)

    hrefs = [f"https:{img['href']}" for img in img_anchor]

    print(f"Downloading: {thread_title}")
    for href in tqdm(hrefs):
        image_filename = href.split("/")[-1]

        image_download_path = os.path.join(folder_path, image_filename)

        downloadImage(image_download_path, href)


def main():
    scrape(input("thread url: "))


if __name__ == "__main__":
    main()
    # 403 status code response for all images href. why???
