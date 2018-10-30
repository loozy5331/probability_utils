import os
import re
import json

# 경로 입력.
os.chdir(r"C:\Users\time8\Desktop\program\2018.10")
path = os.getcwd()
tpath = os.path.join(path, "FDDB-folds", "FDDB-folds")

def text_preprocessing(tpath):
    text_name_list = os.listdir(tpath)
    # 타원 데이터가 들어있는 텍스트를 불러옴.
    ellipseList_list = list()
    for i, name in enumerate(text_name_list):
        if (i % 2 == 0):
            ellipseList_list.append(name)
    # 폴더 안에 있는 모든 텍스트 내용을 저장할 변수
    raw_text = ""
    for path in ellipseList_list:
        with open(os.path.join(tpath, path), "r") as file:
            raw_text += file.read()

    # path만 추출
    image_path_list = re.findall(r"(\d+/\d+/\d+/big/img_\d+)\n", raw_text)
    # 타원 갯수 추출 + 숫자로
    ellipNum = re.findall(r"\n([0-9]+)\n", raw_text)
    ellipNum = [int(n) for n in ellipNum]
    # 타원 정보 추출
    raw_text_list = raw_text.split("\n")
    ellipVal = []
    for data in raw_text_list:
        if (len(data) >= 25):
            ellipVal.append(data)

    # dict 값으로 저장.
    # key : path(str), val : ellipVal(list(list()))
    path_ellipse_dict = dict()
    for path, num in zip(image_path_list, ellipNum):
        path_ellipse_dict[path] = []
        for i in range(num):
            tmp = ellipVal[0].split()
            tmp = [float(i) for i in tmp]
            path_ellipse_dict[path].append(tmp)
            ellipVal.pop(0)

    return path_ellipse_dict

if __name__ == "__main__":
    path_ellipse_dict = text_preprocessing(tpath)
    with open(r"utils\total_info.json", "w") as f:
        f.write(json.dumps(path_ellipse_dict, indent=2))