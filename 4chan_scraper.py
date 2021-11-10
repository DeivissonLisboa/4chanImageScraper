import os, sys, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm


def scraper(threadlink):
    r = requests.get(threadlink)
    soup = BeautifulSoup(r.content, "lxml")

    classsubject = soup.find_all("span", {"class": "subject"})[0]
    threadname = classsubject.string or f'thread {threadlink.split("/")[-1]}'
    folderpath = os.path.join(os.getcwd(), threadname)
    try:
        os.mkdir(folderpath)
    except FileExistsError:
        pass

    imgsrc = soup.find_all("a", {"class": "fileThumb"}, href=True)
    imgsrclist = [img["href"] for img in imgsrc]
    for src in tqdm(imgsrclist, desc=threadname):
        imagerequest = requests.get("https:" + src)
        imagename = src.split("/")[-1]
        with open(os.path.join(folderpath, imagename), "wb") as image:
            image.write(imagerequest.content)


def help():
    print(
        """Usage: ~ python3 4chan_image_scraper.py link thread_link 
    or ~ python3 4chan_image_scraper.py batch "path/to/batch.json" """
    )


def main():
    if sys.argv[1] == "link":
        scraper(sys.argv[2])
    elif sys.argv[1] == "batch":
        with open(sys.argv[2], "r") as file:
            batch = json.load(file)
            for link in batch["links"]:
                scraper(link)
    else:
        help()


main()
