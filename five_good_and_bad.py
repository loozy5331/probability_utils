from utils.Evaluate import *
import pandas as pd
import os
import json
import cv2

#def extract_five_score(Score_dict):



if __name__ == "__main__":
    # Frequency 파일 불러오기
    skin_freq = [pd.read_csv(r"pmf_freq\skin_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]
    Nonskin_freq = [pd.read_csv(r"pmf_freq\NonS_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]

    # pmf 만들기
    jointed_skin_pmf = make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[2] + skin_freq[3] + skin_freq[4])
    jointed_Non_skin_pmf = make_pmf(Nonskin_freq[0] + Nonskin_freq[1]
                                    + Nonskin_freq[2] + Nonskin_freq[3] + Nonskin_freq[4])

    # key: img_name, value: [score, precision, recall] 인 dict 불러오기
    Normal_Score_dict = dict()
    Gaussian_Score_dict = dict()
    with open("Normal_score.json", "r") as file:
        Normal_Score_dict = json.load(file)

    with open("Gaussian_score.json", "r") as file:
        Gaussian_Score_dict = json.load(file)

    # 뒤의 18개를 빼준 것은 예외처리된 파일이 18개 있기 때문.
    sorted_by_score_Normal = sorted(Normal_Score_dict, key=lambda k: Normal_Score_dict[k][0], reverse=True)
    sorted_by_score_Normal = sorted_by_score_Normal[:-18]
    sorted_by_score_Gaussian = sorted(Gaussian_Score_dict, key=lambda k: Gaussian_Score_dict[k][0], reverse=True)
    sorted_by_score_Gaussian = sorted_by_score_Gaussian[:-18]

    # 5개의 score가 높고 낮은 이미지를 모델별로 만듬.
    five_good_score_Normal = sorted_by_score_Normal[:5]
    five_bad_score_Normal = sorted_by_score_Normal[-5:]
    five_good_score_Gaussian = sorted_by_score_Gaussian[:5]
    five_bad_score_Gaussian = sorted_by_score_Gaussian[-5:]




