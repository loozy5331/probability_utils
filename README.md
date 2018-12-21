<응용확률 기록장>
<utils>
[text_preprocessing.py]
1. 텍스트 데이터를 불러와서 이미지 주소, 타원 개수, 타원 속성으로 값을 각각 얻음(정규식 사용).
2. 이미지 주소를 key값으로 하고, 타원 속성을 value로 하여 "total_info.json"파일을 만듬 
//"total_info.json" 파일의 형식
{
  "2002/08/11/big/img_591": [
    [
      123.5833,
      85.5495,
      1.265839,
      269.6934,
      161.7812,
      1.0
    ]
  ], ...

[bringAndMaskingImg.py]
3. total_info.json 파일을 불러와서 각각의 이미지에 타원으로 마스킹을 한 뒤에 마스킹(Skin = 1, NonSkin = 2)을 하고, (B,G,R,skin)순으로 csv 파일을 만듬. 위치는 원래 이미지 파일이 있는 곳과 동일한 폴더에 만듬.(왜냐하면 같은 이름의 이미지들이 다른 이름의 폴더에 들어있었기 때문에 그리고 total_info.json파일을 계속 활용하기 위하여.)
3.1 타원으로 마스킹을 할때, 원래는 검정으로 했다가 배경에 검정색까지 마킹되는 것을 확인하고 가능하면 피부색과 비슷한 색으로 마킹하고자 주어진 파일인 "Skin_NonSkin.txt" 파일을 활용하였음. 

3.1.1 완전히 검은색은 Skin보다는 눈, 입, 머리카락일 확률이 높기 때문에 Non-Skin으로 따로 처리!
+ 이 처리 없이 뽑은 pmf에선 검정색 값에서 매우 높은 값을 가진 그래프를 첨부!
3.2 파일을 불러오는 과정에서 흑백이미지나 깨진 이미지 들이 존재함을 확인하였고, 이런 이미지들을 따로 "exception_file.txt"로 만들어서 제거해주었음.  

[makeFreq.py]
4. 레이블 처리된 파일들의 "경로 + 이름 + .csv"로 리스트를 만듬. 
4.1 그리고 k-fold를 위해 이 리스트를 가능한 균등하게 5등분을 함.
4.1.1 분할은 픽셀이 아닌 이미지 갯수로 함. 왜냐하면 분할하는 과정에서 한 이미지가 중간에서 잘라져서 다른 그룹으로 각각 나누어지면 연속성이 없다고 생각함.
5. 그리고 각각의 Set 별로 Skin_BGR과 Non_Skin_BGR로 총 10개의 pmf를 만듬.
행은 BGR 순서이고, 열은 0~255 총 256의 색상값
그리고 pmf_freq 폴더에 Skin_BGR은 "Skin_BGR_{}_freq.csv"라는 이름으로 저장. 
그리고 Non_Skin_BGR은 "NonS_BGR_{}_freq.csv"라는 이름으로 저장.
5.1 각각의 pmf를 만들어서 합치는 것보다 각 Set의 빈도수를 저장하여 그때그때 pmf를 만드는 것이 더 합이적으로 생각해서 빈도수를 저장하기로 함.

[Evaluate.py]
0. PRIOR라는 전역변수로 전체 함수들이 동일한 prior가 들어가도록함.
1. 빈도수 파일을 불러와서 5개의 Set으로 pmf을 만들어서 이 pmf를 likelihood로 하여 
posterior를 만듬.
2. Bayesian decision으로 각 Set들의 precision과 recall을 저장함.
2.1 prior를 변경하며 test를 하던 중, prior=0.3에서 precision을 계산하는 도중에 ZeroDivisionError 발생. 즉, skin으로 한번도 판단한 적이 없다는 것을 의미.
따라서 계획한 0.1~1을 0.1간격으로 10개를 테스트한다는 계획을 수정해야함.
0.35에서는 문제없이 실행되었기 때문에 0.35~1 사이에서 10개 정도로 수행하려함.
 + 문제는 하나의 prior를 실행할 때마다 6시간정도가 걸린다는 것...
 + (해결) 코드를 조금 간결하게 했고, multiprocessing을 통해 최대한 병렬 동작하게함. 무엇보다 python의 numpy라이브러리가 c언어로 동작한다고 하여 바꾸었더니 한 prior 당 1시간 정도로 단축되었음.
3. 계산한 precision과 recall은 Evaluate_data에 저장되고, 하위 폴더인 prior=0.x에 옮겨줌.

--------------------------------------------------------------------------------------------

나머지는 중간중간 데이터들을 확인하기 위하여 jupyter notebook을 사용함.

[middle_test.ipynb]
1. 모델이 어떻게 작동하는지 확인하기 위하여 pmf만 비교하여 이미지에 적용해봄.
Skin은 하얀색, NonSkin은 검정으로 했는데, 생각보다 잘 되는 듯함.

[make_map_and_prepare_score]
1. Evaluate_data에 Set별로 나누어진 precision과 recall을 모델별로 합쳐줌.
각 prior마다 N_set_R.csv, N_set.csv, G_set_R.csv, G_set.csv 이렇게 4개의 모델을 만듬.
2. 그리고 평가를 위하여 prior 별로 나누어진 파일들을 다시 하나로 합쳐서 모델별로
precision과 recall을 각각 따로 총 8개의 파일을 만듬. 파일 이름은
Normal_R_precision.csv, Gaussian_R_precision.csv이런 식이고, 내용은 
#prior, Set1, Set2, Set3, Set4, Set5 이렇게 구성됨.

3. prior에 따라서 precision과 recall을 더하여 어떤 모델이 더 좋은지 비교하려고 각 모델마다 두 값을 더하고, 그래프를 그렸더니 precision이 상대적으로 recall보다 작은 값을 가졌기 때문에 recall의 영향이 매우 컷음. 하지만 precision과 recall 어느 것이 더 중요하다고 할 수없기 때문에 똑같은 비율로 점수를 반영하기 위하여 Set 별로 precision과 recall의 상대적인 비율을 곱하여 같은 최종결과에 같은 영향을 미칠 수 있도록 하였다.

[make_graph.ipynb]
1. Gnuplot 그래프를 그리기 위하여 만듬.

[draw_picture.inynb]
1. RGB로 구한 Normal pmf와 Gaussian pmf를 likelihood로 불러와서 좋은 성적의 5개와 나쁜 성적의 5개를 
출력.
2. 이미지 출력 형식은 Original, 타원으로 마스킹된 이미지, Skin classifier를 통과하고 나온 이미지
3. Skin classifier를 통과하고 나온 이미지의 경우 Skin의 판단을 위하여 Skin은 하얀색, 아닌 곳은 검은색으로 이미지를 출력.