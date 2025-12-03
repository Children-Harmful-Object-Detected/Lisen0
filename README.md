<div style="text-align: center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=FFC2D1&height=120&text=LiSEN&animation=fadeIn&fontColor=000000&fontSize=60" style="width: 100%;" />
</div>

# LiSEN
- ML Team Project
- Listen + Sense, “아이의 작은 신호를 듣다”

## 프로젝트 소개
어린이집의 가정 내 아동학대 의심 아동 조기 발견 및 신고 자동화 솔루션
- **어린이집 CCTV 기반 '아동학대 실시간 탐지 시스템 개발**
    - 어린이집 CCTV는 대부분 사후 확인용이라 실시간 학대 감지가 어려움
    - 장난 / 제지 / 학대 동작이 유사해 사람이 즉시 판단에 제한적
    - 이를 보완하기 위해 AI 기반의 정확한 실시간 행동 분석 시스템이 필요하다고 판단

## 개발기간 (11/03 ~ 12/05)
- **2025.11.03 ~ 2025.11.05** : 기획 / 데이터 수집 / 분석
- **2025.11.06 ~ 2025.11.13** : 데이터 수집 / 분석 / 전처리
- **2025.11.14 ~ 2025.11.28** : 모델 선택 / 모델 학습 / 모델 평가
- **2025.12.01 ~ 2025.12.05** : 웹서비스 구현 / 문서 정리

## 팀원 소개
- [빙승현](https://github.com/ProjectBA0) : 자료 수집, 모델 학습 및 개발
- [정두균](https://github.com/dooposip) : streamlit 제작
- [지수정](https://github.com/ehqlsms1004) : PPT 제작 및 디자인
- [류주현](https://github.com/HyunRyuuu) : PL, 자료 수집, GITHUB ReadME 작성, 발표

## 문제 정의 & 기술적 난제
- 어린이의 행동은 빠르게 변화하고 정상 행동과 학대 행동이 시각적으로 유사함
- 단일 포즈 기반의 분석만으로는 의도와 맥락을 정확하게 판단하기 어려움
- 따라서 실환경에서 신뢰성 있게 동작하려면 시간적 흐름까지 고려한 분석 구조가 필요함
- YOLOv11m-pose 단독 모델은 장난 / 제지 / 학대가 비슷한 모션 패턴을 보임
- 포즈 정보만으로 오탐(Fasle Positive)이 빈번하게 발생하는 한계 발생
- 이를 해결하기 위해 포즈 이상의 정보를 활용하는 추가 판단 모델이 요구됨

<div style="text-align: left;">
    <h2 style="border-bottom: 1px solid #d8dee4; color: #282d33;"> 🛠️ Tech Stacks </h2> <br> 
    <div style="margin: ; text-align: left;" "text-align: left;">
        <img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white">
        <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white">
    </div>
</div>
 
## 프로젝트 구조
```
onDayClass/
├── static/
│   ├── photo/                   # 이미지 폴더
│   │  ├── baking                  # 베이킹 클래스
│   │  ├── drowing                 # 드로잉 클래스
│   │  ├── juwaly                  # 쥬얼리 클래스
│   │  ├── perfume                 # 향수 클래스
│   │  ├── popular_class           # 인기 클래스
│   ├── reset.css                # 브라우저 기본 스타일 초기화 css
│   └── style.css                # 스타일 css
│
├── templates/                   # HTML 템플릿 파일
│   ├── answer/                    # 클래스 문의 > 답변
│   │  └── answer_form.html          # 클래스 문의 > 답변 수정
│   ├── member/                  # 회원
│   │  ├── login.html              # 로그인
│   │  ├── modifyMember.html       # 회원정보 수정
│   │  ├── mypage.html             # 마이페이지(현재 예약, 전체 예약, 회원 정보)
│   │  └── signup.html             # 회원가입
│   ├── question/                # 클래스 문의
│   │  ├── question_detail.html    # 클래스 문의 상세 보기
│   │  ├── question_form.html      # 클래스 문의 등록
│   │  └── question_list.html      # 클래스 문의 목록
│   ├── reservation/             # 클래스 예약
│   │  └── reservation.form.html   # 클래스 예약하기
│   ├── base.html                # 공통 마크업
│   ├── form_errors.html         # 폼 에러
│   └── navbar.html              # 헤더(gnb) 마크업
│
├── views/
│   ├── answer_views.py          # 클래스 문의 답변(등록, 수정, 삭제)
│   ├── main_views.py            # 
│   ├── member_views.py          # 회원 정보(회원가입, 로그인, 마이페이지, 수정)
│   ├── product_views.py         # 클래스 목록
│   ├── question_views.py        # 클래스 문의(등록, 수정, 삭제)
│   └── reservation_views.py     # 클래스 예약
├── __init__.py
├── filter.py
├── forms.py                    # 폼 관리
├── models.py                   # db 모델 관리
├── .flaskenv                   # 가상환경 세팅
├── .gitignore                  # 깃 이그노어 파일 (깃허브에 올리지 않을 파일 정의)
├── app.py                      
├── config.py                   
├── oneDayClass.db              # 프로젝트 db
├── README.md                   # 프로젝트 개요 및 사용법
├── requirements.txt            # 프로젝트 버전 관리
└── seed.py                     # 이미지 db에 넣기 위한 seed 파일
```

## 시작하기
```conda
  # 가상환경 설정
  > conda create -n 가상환경이름 python=3.10
  > conda active 가상환경이름
```
```flask
  # cmd에서 입력
  # 인터프리터, 가상환경 설정 확인 이후 실행
  
  > streamlit run interfaces/streamlit_app/app.py
```
```flask
  # requirements 설치 필요 시
  > pip install -r requirements.txt
```
