from utils.Evaluate import *
import pandas as pd
import numpy as np
import os
import json
from multiprocessing import Pool

if __name__ == "__main__":
    # 경로 지정
    cur_path = os.getcwd()
    originPics_path = os.path.join(cur_path, "originalPics")
    # total_info.json file
    total_ellip_info = dict()  # total_info.json 불러오기
    with open("total_info.json", "r") as file:
        total_ellip_info = json.load(file)

    # 레이블 처리된 파일들의 "경로 + 이름 + .csv"
    masked_file_list = list()
    for name in total_ellip_info.keys():
        masked_file_list.append(os.path.join(originPics_path, name) + ".csv")

    # Frequency 파일 불러오기
    skin_freq = [pd.read_csv(r"pmf_freq\skin_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]
    Nonskin_freq = [pd.read_csv(r"pmf_freq\NonS_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]

    jointed_skin_pmf = make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[2]
                                + skin_freq[3] + skin_freq[4])
    jointed_Non_skin_pmf = make_pmf(Nonskin_freq[0] + Nonskin_freq[1] + Nonskin_freq[2]
                                    + Nonskin_freq[3] + Nonskin_freq[4])
    