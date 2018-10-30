import json
import os
import pandas as pd

os.chdir(r"C:\Users\time8\Desktop\program\2018.10")
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

for count, file_set in enumerate(file_list):
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
            continue
        row = len(file)            # 행 길이
        col = len(file.iloc[0])    # 열 길이
        # 각 행마다 sex의 값이 1인지 확인.
        for i in range(row):
            sex = file.iloc[i, -1]
            if (sex == 1):  # 이거 확인
                SkinBdict[file.iloc[i, 0]] += 1
                SkinGdict[file.iloc[i, 1]] += 1
                SkinRdict[file.iloc[i, 2]] += 1
            else:
                NonSkinBdict[file.iloc[i, 0]] += 1
                NonSkinGdict[file.iloc[i, 1]] += 1
                NonSkinRdict[file.iloc[i, 2]] += 1
    Skin_B_pmf = list()
    Skin_G_pmf = list()
    Skin_R_pmf = list()
    NonS_B_pmf = list()
    NonS_G_pmf = list()
    NonS_R_pmf = list()

    sumOfSkin_B = sum(SkinBdict.values())
    sumOfSkin_G = sum(SkinGdict.values())
    sumOfSkin_R = sum(SkinRdict.values())
    sumOfNSkin_B = sum(NonSkinBdict.values())
    sumOfNSkin_G = sum(NonSkinGdict.values())
    sumOfNSkin_R = sum(NonSkinRdict.values())
    
    for i in range(0, 256):

        Skin_B_pmf.append(str(SkinBdict[i] / sumOfSkin_B))
        Skin_G_pmf.append(str(SkinGdict[i] / sumOfSkin_G))
        Skin_R_pmf.append(str(SkinRdict[i] / sumOfSkin_R))
        NonS_B_pmf.append(str(NonSkinBdict[i] / sumOfNSkin_B))
        NonS_G_pmf.append(str(NonSkinGdict[i] / sumOfNSkin_G))
        NonS_R_pmf.append(str(NonSkinRdict[i] / sumOfNSkin_R))

    with open(r"pmf_set\Skin_BGR_{}_pmf.csv".format(count), 'w') as f:
        f.write(",".join(Skin_B_pmf) + "\n")
        f.write(",".join(Skin_G_pmf) + "\n")
        f.write(",".join(Skin_R_pmf))
    with open(r"pmf_set\NonS_BGR_{}_pmf.csv".format(count), 'w') as f:
        f.write(",".join(NonS_B_pmf) + "\n")
        f.write(",".join(NonS_G_pmf) + "\n")
        f.write(",".join(NonS_R_pmf))






