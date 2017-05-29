# coding:utf-8
import xlsxwriter, os, re, sys
reload(sys)
sys.setdefaultencoding('utf8')

FILE_PATH = ['/tmp/']

def transform(file_path, file_name):
    name = file_name[0:len(file_name)-4].decode('utf-8')
    xf = xlsxwriter.Workbook(file_path + '/' + name + '.xlsx')
    sheet1 = xf.add_worksheet(name)
    with open(file_path + '/' + file_name) as f:
        for index, line in enumerate(f):
            line = line.decode('utf-8')
            a_txt = line[0:len(line)-1].split('&')
            for i in range(0, len(a_txt)):
                sheet1.write(index, i, a_txt[i])

def run():
    for path in FILE_PATH:
        for parent, dirnames, dirfiles in os.walk(path):
            for dirfile in dirfiles:
                if dirfile[-3:-1] + dirfile[-1] == 'csv':
                    transform(parent, dirfile)

if __name__ == '__main__':
    run()
