#encoding=utf-8
import os,shutil

from win32com.client import gencache
from win32com.client import constants, gencache
from win32com import client
def createPdf(wordPath, pdfPath):
    """
    word转pdf
    :param wordPath: word文件路径
    :param pdfPath:  生成pdf文件路径
    """
    try:
        word=client.DispatchEx("Word.Application")
        if os.path.exists(pdfPath):
            os.remove(pdfPath)
        worddoc=word.Documents.Open(wordPath,ReadOnly=1)
        worddoc.SaveAs(pdfPath,FileFormt=17)
        worddoc.Close()
        return pdfPath
    except:
        return 1


def func(path):
    if os.path.isdir(path):
        for name in os.listdir(path):
            base_name = os.path.join(path, name)
            # print(base_name)
            return func(base_name)
    elif os.path.isfile(path) and path.endswith('.py)'):
        # print(path)
        return os.system('python %s' % path)

if __name__ == '__main__':
    createPdf("D:/MyData/lurui1/Desktop/转换/服务器.docx","D:/MyData/lurui1/Desktop/转换/服务器.pdf")


