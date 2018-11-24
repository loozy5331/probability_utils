import json
import os

if __name__ == "__main__":
    os.chdir(r"..\\")

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

    with open("five_good_score_Normal.csv", "w") as f:
        f.write(",".join(five_good_score_Normal))
    with open("five_bad_score_Normal.csv", "w") as f:
        f.write(",".join(five_bad_score_Normal))
    with open("five_good_score_Gaussian.csv", "w") as f:
        f.write(",".join(five_good_score_Gaussian))
    with open("five_bad_score_Gaussian.csv", "w") as f:
        f.write(",".join(five_bad_score_Gaussian))


