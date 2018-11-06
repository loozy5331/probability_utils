import pandas as pd
import numpy as np
import os
import json
from multiprocessing import Pool

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

def make_pmf(freq):
    freq.iloc[0, :] = [b / sum(freq.iloc[0, :]) for b in freq.iloc[0, :]]
    freq.iloc[1, :] = [g / sum(freq.iloc[1, :]) for g in freq.iloc[1, :]]
    freq.iloc[2, :] = [r / sum(freq.iloc[2, :]) for r in freq.iloc[2, :]]
    return freq

def Test_SkinOrNonSkin_R(file_set, skin_likelihood, NonSkin_likelihood, count):
    PRIOR = 0.5
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    skin_R = skin_likelihood.iloc[2, :]
    NonSkin_R = NonSkin_likelihood.iloc[2, :]
    print(count)
    for path in file_set:
        try:
            file = pd.read_csv(path, header=None)
        except(Exception):
            continue
        row = len(file)  # 행 길이
        for i in range(row):
            real_val = file.iloc[i, -1]
            R = file.iloc[i, 2]
            skin_posterior = skin_R[R] * PRIOR
            Nonskin_posterior = NonSkin_R[R] * (1 - PRIOR)

            # skin 이고, 실제로 skin
            if((skin_posterior > Nonskin_posterior) and real_val == 1):
                TP += 1
            # Nonskin 이고, 실제로 Nonskin
            elif((skin_posterior < Nonskin_posterior) and real_val != 1):
                TN += 1
            # skin 이고, 실제론 Nonskin
            elif((skin_posterior > Nonskin_posterior) and real_val != 1):
                FP += 1
            # Nonskin 이고, 실제로 skin
            else:
                FN += 1
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    temp = str(precision) + ", " + str(recall)
    with open(r"Evaluate_data\precision_recall_set_{}_R.csv".format(count + 1)) as f:
        f.write(temp)

def Test_SkinOrNonSkin(file_set, skin_likelihood, NonSkin_likelihood, count):
    PRIOR = 0.5
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    skin_B = skin_likelihood.iloc[0, :]
    skin_G = skin_likelihood.iloc[1, :]
    skin_R = skin_likelihood.iloc[2, :]

    NonSkin_B = NonSkin_likelihood.iloc[0, :]
    NonSkin_G = NonSkin_likelihood.iloc[1, :]
    NonSkin_R = NonSkin_likelihood.iloc[2, :]
    print(count)
    for path in file_set:
        try:
            file = pd.read_csv(path, header=None)
        except(Exception):
            continue
        row = len(file)  # 행 길이
        for i in range(row):
            real_val = file.iloc[i, -1]
            B = file.iloc[i, 0]
            G = file.iloc[i, 1]
            R = file.iloc[i, 2]
            skin_posterior = (skin_B[B] * skin_G[G] * skin_R[R]) * PRIOR
            Nonskin_posterior = (NonSkin_B[B] * NonSkin_G[G] * NonSkin_R[R]) * (1 - PRIOR)
            # skin 이고, 실제로 skin
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
    temp = str(precision) + ", " + str(recall)
    with open(r"Evaluate_data\precision_recall_set_{}.csv".format(count + 1)) as f:
        f.write(temp)

def gaussian_distribution(x):
    var = np.var(x)
    mean = np.mean(x)
    y = (1 / (np.sqrt(2 * np.pi * var))*np.exp(-(x-mean)**2/(2*var)))
    return y

def Test_Gaussian_SkinOrNonSkin_R(file_set, skin_likelihood, NonSkin_likelihood, count):
    PRIOR = 0.5
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    skin_R = skin_likelihood.iloc[2, :]
    skin_R = gaussian_distribution(skin_R)
    NonSkin_R = NonSkin_likelihood.iloc[2, :]
    NonSkin_R = gaussian_distribution(NonSkin_R)
    print(count)
    for path in file_set:
        try:
            file = pd.read_csv(path, header=None)
        except(Exception):
            continue
        row = len(file)  # 행 길이
        print(TP, TN, FP, FN)
        for i in range(row):
            real_val = file.iloc[i, -1]
            R = file.iloc[i, 2]
            skin_posterior = skin_R[R] * PRIOR
            Nonskin_posterior = NonSkin_R[R] * (1 - PRIOR)

            # skin 이고, 실제로 skin
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
    temp = str(precision) + ", " + str(recall)
    with open(r"Evaluate_data\Gaussian_precision_recall_set_{}_R.csv".format(count + 1)) as f:
        f.write(temp)

def Test_Gaussian_SkinOrNonSkin(file_set, skin_likelihood, NonSkin_likelihood, count):
    PRIOR = 0.5
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    skin_B = skin_likelihood.iloc[0, :]
    skin_B = gaussian_distribution(skin_B)
    skin_G = skin_likelihood.iloc[1, :]
    skin_G = gaussian_distribution(skin_G)
    skin_R = skin_likelihood.iloc[2, :]
    skin_R = gaussian_distribution(skin_R)

    NonSkin_B = NonSkin_likelihood.iloc[0, :]
    NonSkin_B = gaussian_distribution(NonSkin_B)
    NonSkin_G = NonSkin_likelihood.iloc[1, :]
    NonSkin_G = gaussian_distribution(NonSkin_G)
    NonSkin_R = NonSkin_likelihood.iloc[2, :]
    NonSkin_R = gaussian_distribution(NonSkin_R)
    print(count)
    for path in file_set:
        try:
            file = pd.read_csv(path, header=None)
        except(Exception):
            continue
        row = len(file)  # 행 길이
        for i in range(row):
            real_val = file.iloc[i, -1]
            B = file.iloc[i, 0]
            G = file.iloc[i, 1]
            R = file.iloc[i, 2]
            skin_posterior = (skin_B[B] * skin_G[G] * skin_R[R]) * PRIOR
            Nonskin_posterior = (NonSkin_B[B] * NonSkin_G[G] * NonSkin_R[R]) * (1 - PRIOR)
            # skin 이고, 실제로 skin
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
    temp = str(precision) + ", " + str(recall)
    with open(r"Evaluate_data\Gaussian_precision_recall_set_{}.csv".format(count + 1)) as f:
        f.write(temp)

if __name__ == "__main__":
    prior = 0.4
    # Frequency 파일 불러오기
    skin_freq = [pd.read_csv(r"pmf_set\skin_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]
    Nonskin_freq = [pd.read_csv(r"pmf_set\NonS_BGR_{}_freq.csv".format(count + 1), header=None) for count in range(5)]

    # Set별 pmf들을 만듬.
    skin_pmf = [make_pmf(skin_freq[1] + skin_freq[2] + skin_freq[3] + skin_freq[4])
                , make_pmf(skin_freq[0] + skin_freq[2] + skin_freq[3] + skin_freq[4])
                , make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[3] + skin_freq[4])
                , make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[2] + skin_freq[4])
                , make_pmf(skin_freq[0] + skin_freq[1] + skin_freq[2] + skin_freq[3])]

    Non_skin_pmf = [make_pmf(Nonskin_freq[1] + Nonskin_freq[2] + Nonskin_freq[3] + Nonskin_freq[4])
                    , make_pmf(Nonskin_freq[0] + Nonskin_freq[2] + Nonskin_freq[3] + Nonskin_freq[4])
                    , make_pmf(Nonskin_freq[0] + Nonskin_freq[1] + Nonskin_freq[3] + Nonskin_freq[4])
                    , make_pmf(Nonskin_freq[0] + Nonskin_freq[1] + Nonskin_freq[2] + Nonskin_freq[4])
                    , make_pmf(Nonskin_freq[0] + Nonskin_freq[1] + Nonskin_freq[2] + Nonskin_freq[3])]

    count_list = list(range(5))
    # R로만 precision, recall을 구함.
    with Pool(12) as p:
        p.starmap(Test_SkinOrNonSkin_R, zip(file_list, skin_pmf, Non_skin_pmf, count_list))

    # BGR로 precision, recall을 구함.
    with Pool(12) as p:
        p.starmap(Test_SkinOrNonSkin, zip(file_list, skin_pmf, Non_skin_pmf, count_list))

    # R만 Guassian fitting 후에 precision, recall을 구함.
    with Pool(12) as p:
        p.starmap(Test_Gaussian_SkinOrNonSkin_R, zip(file_list, skin_pmf, Non_skin_pmf, count_list))

    # BGR을 Guassin fitting 후에 precision, recall을 구함.
    with Pool(12) as p:
        p.starmap(Test_Gaussian_SkinOrNonSkin, zip(file_list, skin_pmf, Non_skin_pmf, count_list))
