import json
import os
from multiprocessing import Pool
import pandas as pd

os.chdir(r"..\\")
cur_path = os.getcwd()
originPics_path = os.path.join(cur_path, "originalPics")
# total_info.json file
total_ellip_info = dict()   # total_info.json 불러오기
with open("total_info.json", "r") as file:
    total_ellip_info = json.load(file)

# 레이블 처리된 파일들의 "경로 + 이름 + .csv"
masked_file_list = list()
for name in total_ellip_info.keys():
    masked_file_list.append(os.path.join(originPics_path, name) + ".csv")

# 파일을 5분할
each_file_len = len(masked_file_list) // 5
# file_list = [first_set[], second_set[], third_set[], fourth_set[], fifth_set[]]
file_list = []
for i in range(5):
    file_list.append(masked_file_list[each_file_len*i:each_file_len*(i+1)])

def makeFrequancy(file_set, count):
    # for count, file_set in enumerate(file_list):
    # 이미 있으면 패스!
    if os.path.isfile(os.path.join("pmf_freq", r"Skin_BGR_{}_freq.csv".format(count + 1))):
        print(r"freq_set\Skin_BGR_{}_freq.csv".format(count + 1) + "는 이미 있습니다!")
        return

    print("{}번째 set 생성 중".format(count + 1))

    # 각각의 BGR 값이 몇번씩 나왔는지 체크
    SkinBdict = dict()
    SkinGdict = dict()
    SkinRdict = dict()
    NonSkinBdict = dict()
    NonSkinGdict = dict()
    NonSkinRdict = dict()

    # 0~255까지 0으로 초기화
    for i in range(0, 256):
        SkinBdict[i] = 0
        SkinGdict[i] = 0
        SkinRdict[i] = 0
        NonSkinBdict[i] = 0
        NonSkinGdict[i] = 0
        NonSkinRdict[i] = 0

    for path in file_set:
        try:
            file = pd.read_csv(path, header=None)
        except(Exception):
            # 흑백이나 깨진 이미지
            # 예외 파일들.
            continue
        row = len(file)            # 행 길이
        col = len(file.iloc[0])    # 열 길이
        # 각 행마다 Skin 값이 1인지 확인.
        for i in range(row):
            Skin = file.iloc[i, -1]
            if (Skin == 1):  # 피부!
                SkinBdict[file.iloc[i, 0]] += 1
                SkinGdict[file.iloc[i, 1]] += 1
                SkinRdict[file.iloc[i, 2]] += 1
            else:
                NonSkinBdict[file.iloc[i, 0]] += 1
                NonSkinGdict[file.iloc[i, 1]] += 1
                NonSkinRdict[file.iloc[i, 2]] += 1

    Skin_B_freq = list()
    Skin_G_freq = list()
    Skin_R_freq = list()
    NonS_B_freq = list()
    NonS_G_freq = list()
    NonS_R_freq = list()
    
    for i in range(0, 256):
        # 각각의 색상별로 데이터 갯수를 구함. p(B|Skin) ...
        Skin_B_freq.append(str(SkinBdict[i]))
        Skin_G_freq.append(str(SkinGdict[i]))
        Skin_R_freq.append(str(SkinRdict[i]))
        NonS_B_freq.append(str(NonSkinBdict[i]))
        NonS_G_freq.append(str(NonSkinGdict[i]))
        NonS_R_freq.append(str(NonSkinRdict[i]))

    # 각 집합마다 파일을 따로 저장.
    with open(r"pmf_freq\Skin_BGR_{}_freq.csv".format(count + 1), 'w') as f:
        f.write(",".join(Skin_B_freq) + "\n")
        f.write(",".join(Skin_G_freq) + "\n")
        f.write(",".join(Skin_R_freq))
    with open(r"pmf_freq\NonS_BGR_{}_freq.csv".format(count + 1), 'w') as f:
        f.write(",".join(NonS_B_freq) + "\n")
        f.write(",".join(NonS_G_freq) + "\n")
        f.write(",".join(NonS_R_freq))


if __name__ == "__main__":
    # 분산 작업을 위해!
    count_list = [0, 1, 2, 3, 4]
    with Pool(8) as p:
        p.starmap(makeFrequancy, zip(file_list, count_list))




