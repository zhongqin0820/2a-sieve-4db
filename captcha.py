# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import os


class Convertor(object):
    """
    自动验证码
    前置条件：
        pip install tesseract
        pip install pytesseract
        brew install tesseract-ocr
    """
    def __init__(self, file_name='',config=''):
        super(Convertor, self).__init__()
        if file_name is '':
            self.file_name = 'captcha.jpg'
        else:
            self.file_name = file_name
        if config is '':
            self.config = '--psm 10 --oem 3 -c tessedit_char_whitelist=' \
                          'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        else:
            self.config = config
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.img = None

    def open_image(self):
        """
        读入图片
        """
        if os.path.exists(self.file_name) and os.path.isfile(self.file_name):
            self.img = Image.open(self.file_name)

    def pre_concert(self):
        """
        对图片做预处理，去除背景
        """
        img = self.img
        width,height = img.size
        threshold = 30
        # FIXME: 太糟糕了
        for i in range(0,width):
            for j in range(0,height):
                #抽取每个像素点的像素，二值化操作分离前景与背景
                p = img.getpixel((i,j))
                r,g,b = p
                if r > threshold or g > threshold or b > threshold:
                    img.putpixel((i,j),self.WHITE)
                else:
                    img.putpixel((i,j),self.BLACK)
        self.img = img
        # self.img.show()
 
    def remove_noise(self, window=1):
        """
        对去除背景的图片做噪点处理
        
        :param window: 窗口类型
        :type window: int
        :return: 切分后图片的切片
        :rtype: List[Image]
        """
        img = self.img
        # FIXME: 太糟糕了
        if window == 1:
            window_x = [1,0,0,-1,0]
            window_y = [0,1,0,0,-1]
        elif window == 2:
            window_x = [-1,0,1,-1,0,1,1,-1,0]
            window_y = [-1,-1,-1,1,1,1,0,0,0]
     
        width,height = img.size
        for i in range(width):
            for j in range(height):
                box = []
                for k in range(len(window_x)):
                    d_x = i + window_x[k]
                    d_y = j + window_y[k]
                    try:
                        d_point = img.getpixel((d_x,d_y))
                        if d_point == self.BLACK:
                            box.append(1)
                        else:
                            box.append(0)
                    except IndexError:
                            img.putpixel((i,j),self.WHITE)
                            continue
                box.sort()
                if len(box) == len(window_x):
                    mid = box[int(len(box)/2)]
                    if mid == 1:
                        img.putpixel((i,j),self.BLACK)
                    else:
                        img.putpixel((i,j),self.WHITE)
        self.img = img
        # self.img.show()
 
    def split_fig(self):
        """
        切分字符

        :return: 切分后图片的切片
        :rtype: List[Image]
        """
        img = self.img
        frame = img.load()
        img_new = img.copy()
        frame_new = img_new.load()
        # FIXME: 太糟糕了
        width,height = img.size
        line_status = None
        pos_x = []
        for x in range(width):
            pixs = []
            for y in range(height):
                pixs.append(frame[x,y])
     
            if len(set(pixs)) == 1:
                _line_status = 0
            else:
                _line_status = 1
     
            if _line_status != line_status:
                if _line_status != None:
                    if _line_status == 0:
                        _x = x
                    elif _line_status == 1:
                        _x = x - 1
     
                    pos_x.append(_x)
     
                    #辅助线
                    for _y in range(height):
                        frame_new[x,_y] = self.BLACK
     
            line_status = _line_status
     
        i = 0
        divs = []
        boxs = []
        while True:
            try:
                x_i = pos_x[i]
                x_j = pos_x[i+1]
            except:
                break
     
            i = i + 2
            boxs.append([x_i,x_j])
     
        fixed_boxs = []
        i = 0
        while i < len(boxs):
            box = boxs[i]
            if box[1] - box[0] < 10:
                try:
                    box_next = boxs[i+1]
                    fixed_boxs.append([box[0],box_next[1]])
                    i += 2
                except Exception:
                    break
            else:
                fixed_boxs.append(box)
                i += 1
     
        for box in fixed_boxs:
            div = img.crop((box[0],0,box[1],height))
            try:
                divs.append(div)
            except:
                divs.append(div)
     
        #过滤掉非字符的切片
        _divs = []
        for div in divs:
            width,heigth = div.size
            if width < 5:
                continue
     
            frame = div.load()
            points = 0
            for i in range(width):
                for j in range(heigth):
                    p = frame[i,j]
                    if p == self.BLACK:
                        points += 1
     
            if points <= 5:
                continue
     
            new_div = div
            _divs.append(new_div)
        return _divs
    
    def image_to_string(self, config=''):
        """
        将去除噪点后的图片转换为字符串

        :param config: pytesseract的配置选项
        :returns: 识别得到的字符
        """
        try:
            self.open_image()
            self.pre_concert()
            self.remove_noise()
            if config is '':
                config = self.config
            result = pytesseract.image_to_string(self.img,lang='eng',config=config)
            result = result.strip()
            return result.lower()
        except Exception as e:
            return None
    
    def images_to_string(self, config=''):
        """
        将分割后的序列转化为字符串

        :param config: pytesseract的配置选项
        :type config: str
        :return: 识别得到的字符
        :rtype: str
        """
        try:
            self.open_image()
            self.pre_concert()
            self.remove_noise()
            img = self.split_fig()
            if config is '':
                config = self.config
            res = []
            for i in img:
                res.append(pytesseract.image_to_string(i,lang='eng',config=config).strip().lower())
            return ''.join(res)
        except Exception as e:
            return None

    def digital_to_string(self, config='--psm 8 -c tessedit_char_whitelist=1234567890'):
        """
        数字转换

        :param config: pytesseract的配置选项
        :type config: str
        :return: 识别得到的字符
        :rtype: str
        """
        try:
            self.open_image()
            if config is '':
                config = self.config
            result = pytesseract.image_to_string(self.img,lang='eng',config=config)
            return result
        except Exception as e:
            return None

    def letter_to_string(self, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """
        字符转换

        :param config: pytesseract的配置选项
        :type config: str
        :return: 识别得到的字符
        :rtype: str
        """
        try:
            self.open_image()
            if config is '':
                config = self.config
            result = pytesseract.image_to_string(self.img,lang='eng',config=config)
            return result
        except Exception as e:
            return None


if __name__ == '__main__':
    # 数字
    c = Convertor("img/digital.jpg")
    captcha = c.digital_to_string()
    print(captcha)
    # 字母
    c = Convertor("img/letter.jpg")
    captcha = c.letter_to_string()
    print(captcha)
    # 验证码
    c = Convertor("img/captcha.jpg")
    captcha = c.images_to_string()
    print(captcha)
    captcha = c.image_to_string()
    print(captcha)
