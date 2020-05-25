#encoding=utf-8
import urllib
import urllib.request

def get_image(url):

    urllib.request.urlretrieve(url, filename='./1.png')

if __name__ == '__main__':
    s1="https://slbimg-cabinet-image2.mideazn.com/images/2020/04/08/1586311259479863867027875796/1.jpg";
    get_image(s1)