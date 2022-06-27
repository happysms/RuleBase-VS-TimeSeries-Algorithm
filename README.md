# RuleBase-VS-TimeSeries-Algorithm

Rule Base Trading Strategy VS TimeSeries Algorithm Trading Strategy (KHU Data Analysis Capstone Lec, 경희개미 team)

## Warm Up

### git clone

```git
git clone https://github.com/happysms/RoleBase-VS-TimeSeries-Algorithm.git
```

### git 강제 pull 방법

```git
git fetch --all
git reset --hard origin/main
git pull origin main
```

### Python 환경

Conda Python 3.8 - 구글링해서 패키지 환경 세팅 방법 확인 후 세팅 바람

### conda 환경 세팅

```pwsh
conda create -n 가상환경이름 python=3.8
conda activate 가상환경이름
```

### Requirement install (./RoleBase-VS-TimeSeries-Algorithm 폴더에서 명령어 입력)

```python
pip install -r requirements.txt
```

### 주의사항

- 작업 전 "git pull"하고 수행하기
- 작업 마친 후 git add . | git commit -m "작업 완료" | git push 수행하기
- 각자 작업하는 폴더 이외의 코드는 수정하기 않기, 꼭 수정이 필요하면 먼저 알리고 수정 (충돌 방지)
- repository 별 달기

### Flow

```git
git pull
--- 작업 시작 --- 
git add .
git commit -m "작업 종료"
git push
```

---

## 코드 작성 규칙

### 초기 암호화폐.pkl 파일을 불러오는 함수 통일

- 데이터프레임 칼럼 명을 ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']로 지정할 것.

### 데이터 프레임 전처리 과정 명시화, 주석 작성

- 모델마다 DateFrame 전처리 과정이 다르므로 상세한 주석 및 함수를 통해 해결.

### .ipynb 파일 내 데이터 프레임 출력을 최소화할 것

- 트레이딩 분석 지표 함수의 출력 형식을 공통의 데이터프레임으로 변환하여 저장.

### .ipynb 파일 내 plt 이미지 출력을 최소화할 것

- plt.save()를 이용하여 해당 모델을 반영하는 경로와 파일명으로 저장하는 함수 사용.

---

## TimeSeries Algorithm

- Linear Regression
- Arima
- XGB regression
- LSTM



### 예측 방법

1. 1200시간(50일) fitting, 24시간(1일) 미래 예측
2. 2400시간(100일) fitting, 24시간(1일) 미래 예측

### 트레이딩 방법

1. 예측 시점의 가격의 현 가격보다 높다면 피팅 종료 시점에서 매수한 뒤 예측 시점에서 매도

### rule base 보조 지표

1. 5, 10, 20, 50, 100일 시가 이동평균선
2. 전일 RSI 지표
3. noise - 캔들 전체에서 아래꼬리, 윗꼬리의 비중 - noise가 크다는 것은 시장이 불안정하다는 의미

### 트레이딩 분석 지표

1. 거래 확률(trading rate): 거래한 날 / 전체 날
2. 거래 성공 확률(trading success rate): 거래 성공 횟수 / 거래한 날
3. MDD(Maximum drawdown): 최대 손실폭(최고점 수익률에서 최저점 수익률까지의 낙폭)
4. 누적 수익률(Cumulative return rate): 누적 수익률
5. 손익비(P&L rate): 거래 성공시 수익률 평균 / 거래 실패시 수익률 평균

### 테스트 기간 설정

2017년 이후에서야 경우 비트코인이 많은 사람들에게 주목을 받고 많은 개인 투자자들이 투자를 했기 때문에 2017년 이후의 데이터로만 테스트를 진행한다.

총 기간: 2017-01-01 ~ 2022-05-15
상승장: 2020-03-14 ~ 2021-01-09
하락장: 2021-10-10 ~ 2022-05-15
