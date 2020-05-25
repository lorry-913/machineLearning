# coding=gbk
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt


def operation_write_file(file_name, matrix):
    try:
        h_file = open(file_name, 'w', 1)
        try:
            for i in matrix.shape[0]:
                for j in matrix.shape[1]:
                    print matrix[i][j]
                    # h_file.write(str(matrix[i][j]))
                h_file.write("\n")
        finally:
            h_file.close()
    except IOError:
        print("IOError")

def ImageToMatrix(filename):
    # 读取图片
    im = Image.open(filename)
    mountain = cv2.imread(filename, 0)  # 读取为灰度图
    imgMatri=np.asarray(mountain)
    print imgMatri[0]
    print imgMatri.shape[0]
    print imgMatri.shape[1]
    # 显示图片
    #     im.show()
    width, height = im.size
    #
    # operation_write_file("text.txt",imgMatri)
    # im = im.convert("L")
    # data = im.getdata()
    # data = np.matrix(data, dtype='float') / 32.0
    # new_data = np.reshape(data, (width, height))
    # return new_data
    #     new_im = Image.fromarray(new_data)
    #     # 显示图片
    #     new_im.show()
def MatrixToImage(data):
    data = data * 255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im

# new_im = MatrixToImage(data)
# plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
# new_im.show()
# new_im.save('lena_1.bmp')
if __name__ == '__main__':
    filename = './data/img/7img.png'
    ImageToMatrix(filename)
