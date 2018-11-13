from utils.Evaluate import *
import pandas as pd
import os
import json

# flag 1: Normal, 2: Gaussian
def judge_score(img_name, skin_df, Non_skin_df, PRIOR, flag):
    # 경로 지정
    cur_path = os.getcwd()
    originPics_path = os.path.join(cur_path, "originalPics")
    img_path = os.path.join(originPics_path, img_name)

    score = 0
    precision = 0
    recall = 0
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    # Normal
    if(flag == 1):
        skin_B = listToArray(skin_df.iloc[0, :])
        skin_G = listToArray(skin_df.iloc[1, :])
        skin_R = listToArray(skin_df.iloc[2, :])
        NonSkin_B = listToArray(Non_skin_df.iloc[0, :])
        NonSkin_G = listToArray(Non_skin_df.iloc[1, :])
        NonSkin_R = listToArray(Non_skin_df.iloc[2, :])

    # Gaussian
    else:
        skin_B = listToArray(gaussian_distribution(skin_df.iloc[0, :]))
        skin_G = listToArray(gaussian_distribution(skin_df.iloc[1, :]))
        skin_R = listToArray(gaussian_distribution(skin_df.iloc[2, :]))
        NonSkin_B = listToArray(gaussian_distribution(Non_skin_df.iloc[0, :]))
        NonSkin_G = listToArray(gaussian_distribution(Non_skin_df.iloc[1, :]))
        NonSkin_R = listToArray(gaussian_distribution(Non_skin_df.iloc[2, :]))


    # masked_img_csv : 타원으로 마스킹된 csv 파일 B G R mask 순으로 저장되어있음.
    # 이름만 있고 예외처리된 이미지 때문에 예외처리문 작성.
    try:
        masked_img_csv = listToArray(pd.read_csv(img_path + ".csv"))
    except(Exception):
        print(img_name + "은 예외처리 되었습니다.")
        return img_name, score, precision, recall

    row = len(masked_img_csv)
    for i in range(row):
        real_val = int(masked_img_csv[i, -1])
        B = int(masked_img_csv[i, 0])
        G = int(masked_img_csv[i, 1])
        R = int(masked_img_csv[i, 2])
        skin_posterior = (skin_B[B] * skin_G[G] * skin_R[R]) * PRIOR
        Nonskin_posterior = (NonSkin_B[B] * NonSkin_G[G] * NonSkin_R[R]) * (1 - PRIOR)

        if ((skin_posterior > Nonskin_posterior) and real_val == 1):
            TP += 1
        # Nonskin 이고, 실제로 Nonskin
        elif ((skin_posterior < Nonskin_posterior) and real_val != 1):
            TN += 1
        # skin 이고, 실제론 Nonskin
        elif ((skin_posterior > Nonskin_posterior) and real_val != 1):
            FP += 1
        # Nonskin 이고, 실제로 skin
        else:
            FN += 1
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    # 비중을 비슷하게 하기 위하여 임의로 2.5를 곱해줌.
    score = precision*2.5 + recall
    return img_name, score, precision, recall


if __name__ == "__main__":
    Normal_Score_dict = dict()
    Gaussian_Score_dict = dict()

    # total_info.json file
    total_ellip_info = dict()  # total_info.json 불러오기
    with open("total_info.json", "r") as file:
        total_ellip_info = json.load(file)

    # 레이블 처리된 파일들의 이름
    img_name_list = list()
    for name in total_ellip_info.keys():
        img_name_list.append(name)

    # Frequency 파일 불러오기
    skin_freq = [pd.read_csv(r"pmf_freq\skin_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]
    Nonskin_freq = [pd.read_csv(r"pmf_freq\NonS_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]

    # pmf 만들기
    jointed_skin_pmf = make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[2] + skin_freq[3] + skin_freq[4])
    jointed_Non_skin_pmf = make_pmf(Nonskin_freq[0] + Nonskin_freq[1]
                                    + Nonskin_freq[2] + Nonskin_freq[3] + Nonskin_freq[4])
    # Normal Score 생성
    for i in range(len(img_name_list)):
        _img_name, _score, _precision, _recall = judge_score(img_name_list[i],
                                                             jointed_skin_pmf,
                                                             jointed_Non_skin_pmf, 0.7, 1)
        Normal_Score_dict[_img_name] = [_score, _precision, _recall]

    # Gaussian Score 생성
    for i in range(len(img_name_list)):
        _img_name, _score, _precision, _recall = judge_score(img_name_list[i],
                                                             jointed_skin_pmf,
                                                             jointed_Non_skin_pmf, 0.8, 2)
        Gaussian_Score_dict[_img_name] = [_score, _precision, _recall]

    with open(r"Normal_Score.json", "w") as f:
        f.write(json.dumps(Normal_Score_dict, indent=2))

    with open(r"Gaussian_Score.json", "w") as f:
        f.write(json.dumps(Gaussian_Score_dict, indent=2))