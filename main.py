import os
import re

from urllib.request import urlopen, urlretrieve, Request
from urllib.request import build_opener, install_opener
from bs4 import BeautifulSoup as bs




def main(url, out_folder="test/"):
    """Main function to find elements and get it."""
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    soup = bs(urlopen(req), "html.parser")

    for image in soup.find_all('img', {"class": 'wp-manga-chapter-img'}):
        image = image['data-src']
        image = re.sub('\t', '', image)
        image = re.sub('\n', '', image)
        filename = image.split("/")[-1]
        outpath = os.path.join(out_folder, filename)
        if not os.path.isfile(outpath):
            urlretrieve(image, outpath)


if __name__ == "__main__":
    CONTENTNAME = None
    URL = [] # destination urls
    # folder output
    FOLDER = ['/content/drive/MyDrive/Document/Compressed/DOC' +
              '/'+CONTENTNAME+'/' + i.split("/")[-1] for i in URL ]
    for url, folder in zip(URL, FOLDER):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        main(url, folder)