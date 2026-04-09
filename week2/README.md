# Week 2: Streamlit 활용 및 SQL 실습

Week 2에서는 파이썬의 `Streamlit` 라이브러리를 사용해 웹 대시보드 및 간단한 어플리케이션을 제작하는 방법과, 데이터베이스 조작을 위한 `SQL` 기초를 학습했습니다.

## 📋 학습 내용 요약

### 1. Streamlit 기반 웹 앱 실습
다양한 인터랙티브 위젯을 활용하여 실습용 앱을 제작했습니다.

- **[fortune.py](fortune.py) (오늘의 운세)**: 사용자 이름과 별자리를 입력받아 오늘의 운세와 행운 지수를 랜덤하게 제공하는 앱입니다.
- **[menu.py](menu.py) (서초구 맛집 탐색기)**: 공공 데이터를 로드하여 서초구 내 식당을 카테고리별로 검색하고, 네이버 지도 링크를 제공합니다.
- **[test.py](test.py) (MBTI 성향 테스트)**: 4가지 지표(E/I, N/S, T/F, J/P)를 판단하는 12개의 질문을 통해 사용자의 MBTI를 분석해주는 앱입니다.
- **[week2_practice.py](week2_practice.py) (통합 앱)**: 위의 운세, 맛집, MBTI 테스트 기능을 탭(Tab) 구조로 통합하여 하나의 웹 서비스처럼 구성한 결과물입니다.

### 2. Streamlit 구성 요소 학습 (강의 코드)
- **[week2.py](week2.py)**: Streamlit에서 제공하는 다양한 컴포넌트(텍스트, 버튼, 체크박스, 선택박스, 다이얼로그, 메트릭, 데이터프레임, 미디어 재생 등)의 사용법을 익혔습니다.

### 3. SQL 데이터 분석 실습
- **[camping.sql](camping.sql)**: 전국 캠핑장 정보 데이터를 활용하여 데이터 추출(SELECT), 조건 필터링(WHERE), 패턴 매칭(LIKE), 그룹화(GROUP BY), 정렬(ORDER BY) 등 기본적인 SQL 쿼리문을 실습했습니다.

---

## 💻 실행 방법 (Streamlit)
```bash
# 통합 실습 앱 실행
streamlit run week2/week2_practice.py
```
