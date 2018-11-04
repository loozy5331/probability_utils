import cv2
import json
import os
import pandas as pd

# 이미지가 저장된 폴더 path
os.chdir(r"C:\Users\time8\Desktop\program\2018.10")
cur_path = os.getcwd()
originPics_path = os.path.join(cur_path, "originalPics")

# total_info.json file
total_ellip_info = dict()   # total_info.json 불러오기
with open("total_info.json", "r") as file:
    total_ellip_info = json.load(file)

#이미지를 불러와서 타원의 마스크를 씌우고 그 부분에 라벨링.
def bringAndMaskingImg(path):
    count = 0
    total_count = len(total_ellip_info.keys())
    for path, ellips in total_ellip_info.items():
        # 얼마나 진행되었는지 확인용
        count += 1;
        if (count % (total_count // 10) == 0):
            print("{}%".format(round((count / total_count) * 100)))
        # 만약 해당 경로에 이미 파일이 있다면 continue
        if os.path.isfile(os.path.join(originPics_path, path) + ".csv"):
            continue

        img_path = os.path.join(originPics_path, path) + ".jpg"
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        img_copy = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        # el[0] = major_axis_radius,
        # el[1] = minor_axis_radius,
        # el[2] = angle,
        # el[3] = center_x,
        # el[4] = center_y,
        # el[5] = detection_score
        for el in ellips:
            # cv2.ellipse(img, center, axes, angel, startAngle, endAngle, color, thickness)
            cv2.ellipse(img, (int(el[3]), int(el[4])), (int(el[1]), int(el[0])), int(el[2]), 0, 360, (113, 146, 203), -1)
        # 이미지의 원래 이름 + .csv
        with open(os.path.join(originPics_path, path) + ".csv", 'w') as f:
            try:
                for row, mrow in zip(img_copy, img):
                    for col, mcol in zip(row, mrow):
                        tmp_str = ""
                        label = "2"     # Non-Skin
                        for n in col:
                            tmp_str += str(n) + ","
                        if(mcol[0] == 113 and mcol[1] == 146 and mcol[2] == 203):
                            label = "1"     # Skin
                        tmp_str += label
                        tmp_str += "\n"
                        f.write(tmp_str)
            except(Exception):
                # 흑백 사진, 깨진 사진은 제외
                print(path)
                pass

# 흑백, 깨진 이미지의 CSV 파일 완전 제거
def removeExceptionFile(path):
    exception_files = list()
    with open("exception_file.txt", "r") as file:
        exception_files = file.readlines()
    for name in exception_files:
        file = os.path.join(path, name[:-1]) + ".csv"
        if os.path.isfile(file):
            os.remove(file)
            print(file)

# csv 파일 전부 삭제.
def removeAllcsvFile(path):
    total_path = total_ellip_info.keys()
    for loc_path in total_path:
        file_name = os.path.join(path, loc_path) + ".csv"
        if os.path.isfile(file_name):
            os.remove(file_name)
            print(file_name)


# 타원을 어떤 색으로 정해야 할 것인가 결정
def guess_Skin_tone():
    guess_Skin_tone = pd.read_csv("Skin_NonSkin.txt", sep="\t", header=None)
    count = 0
    row = len(guess_Skin_tone)
    Skin_tone_B = []
    Skin_tone_G = []
    Skin_tone_R = []
    for i in range(row):
        if guess_Skin_tone.iloc[i, 3] == 1:
            count += 1
            Skin_tone_B.append(guess_Skin_tone.iloc[i, 0])  # B에서 Skin인 값
            Skin_tone_G.append(guess_Skin_tone.iloc[i, 1])  # G에서 Skin인 값
            Skin_tone_R.append(guess_Skin_tone.iloc[i, 2])  # R에서 Skin인 값

    Skin_B_col = sum(Skin_tone_B) // count
    Skin_G_col = sum(Skin_tone_G) // count
    Skin_R_col = sum(Skin_tone_R) // count

    return Skin_B_col, Skin_G_col, Skin_R_col



if __name__ == "__main__":
    print(guess_Skin_tone())
    bringAndMaskingImg(originPics_path)
    removeExceptionFile(originPics_path)# 예외 파일 삭제

