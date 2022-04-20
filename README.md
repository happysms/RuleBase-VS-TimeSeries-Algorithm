# RuleBase-VS-TimeSeries-Algorithm
Rule Base Trading Strategy VS TimeSeries Algorithm Trading Strategy (KHU Data Analysis Capstone Lec, 경희개미 team)

## Warm Up

### git clone
```
git clone https://github.com/happysms/RoleBase-VS-TimeSeries-Algorithm.git
```

### Python 환경

Conda Python 3.8 - 구글링해서 패키지 환경 세팅 방법 확인 후 세팅 바람

### conda 환경 세팅
```
conda create -n 가상환경이름 python=3.8
conda activate 가상환경이름
```


### Requirement install (./RoleBase-VS-TimeSeries-Algorithm 폴더에서 명령어 입력)
```
pip install -r requirements.txt
```

### 주의사항
- 작업 전 "git pull"하고 수행하기
- 작업 마친 후 git add . | git commit -m "작업 완료" | git push 수행하기
- 각자 작업하는 폴더 이외의 코드는 수정하기 않기, 꼭 수정이 필요하면 먼저 알리고 수정 (충돌 방지)
- repository 별 달기

### Flow
```
git pull
--- 작업 수행 --- 
git add .
git commit -m "작업 종료"
git push
```

### TimeSeries Algorithm
- Linear Regression
- Arima
- XGB regression
- LSTM
- Prophet


### 예측 방법
1. 1200시간(50일) fitting, 24시간(1일) 미래 예측
2. 2400시간(100일) fitting, 24시간(1일) 미래 예측


### 트레이딩 방법
1. 예측 시점의 가격의 현 가격보다 높다면 피팅 종료 시점에서 매수한 뒤 예측 시점에서 매도


### 트레이딩 분석 지표
1. 거래 확률(trading rate): 거래한 날 / 전체 날
2. 거래 성공 확률(trading success rate): 거래 성공 횟수 / 거래한 날
3. MDD(Maximum drawdown): 최대 손실폭(최고점 수익률에서 최저점 수익률까지의 낙폭)
4. 누적 수익률(Cumulative return rate): 누적 수익률
5. 손익비(P&L rate): 거래 성공시 수익률 평균 / 거래 실패시 수익률 평균
