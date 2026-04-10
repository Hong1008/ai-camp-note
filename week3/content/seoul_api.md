# 서울시 열린데이터 광장 API 통합 명세

본 문서는 서울시 열린데이터 광장에서 제공하는 주요 API의 요청 인자 및 출력값 정보를 정리한 것입니다.

---

## 1. 서울시 지하철 호선별 역별 승하차 인원 정보 (CardSubwayStatsNew)

서울시 지하철의 호선별, 역별 승하차 인원 통계 정보를 제공합니다.

### 1.1. 요청 인자 (Request Parameters)

| 변수명 | 타입 | 필수 여부 | 변수 설명 | 값 설명 |
| :--- | :--- | :--- | :--- | :--- |
| **KEY** | String | 필수 | 인증키 | OpenAPI에서 발급된 인증키 |
| **TYPE** | String | 필수 | 요청파일타입 | xml, xmlf, xls, **json** |
| **SERVICE** | String | 필수 | 서비스명 | **CardSubwayStatsNew** |
| **START_INDEX** | Integer | 필수 | 요청시작위치 | 정수 입력 (페이징 시작번호) |
| **END_INDEX** | Integer | 필수 | 요청종료위치 | 정수 입력 (페이징 끝번호) |
| **USE_YMD** | String | 필수 | 사용일자 | YYYYMMDD 형식의 문자열 |
| **SBWY_ROUT_LN_NM** | String | 선택 | 호선명 | 지하철 호선 (공백 시 %20으로 조회) |
| **SBWY_STNS_NM** | String | 선택 | 역명 | 지하철 역명 |

### 1.2. 출력값 (Response Fields)

| No | 출력명 | 출력 설명 |
| :--- | :--- | :--- |
| 공통 | **list_total_count** | 총 데이터 건수 (정상 조회 시 출력됨) |
| 공통 | **RESULT.CODE** | 요청 결과 코드 |
| 공통 | **RESULT.MESSAGE** | 요청 결과 메시지 |
| 1 | **USE_YMD** | 사용일자 |
| 2 | **SBWY_ROUT_LN_NM** | 호선명 |
| 3 | **SBWY_STNS_NM** | 역명 |
| 4 | **GTON_TNOPE** | 승차 총 승객 수 |
| 5 | **GTOFF_TNOPE** | 하차 총 승객 수 |
| 6 | **REG_YMD** | 등록일자 |

---

## 2. 따릉이 실시간 대여정보 (bikeList)

서울시 공공자전거(따릉이) 대여소별 실시간 거치 및 대여 가능 정보를 제공합니다.

### 2.1. 요청 인자 (Request Parameters)

| 변수명 | 타입 | 필수 여부 | 변수 설명 | 값 설명 |
| :--- | :--- | :--- | :--- | :--- |
| **KEY** | String | 필수 | 인증키 | OpenAPI에서 발급된 인증키 |
| **TYPE** | String | 필수 | 요청파일타입 | xml, **json** |
| **SERVICE** | String | 필수 | 서비스명 | **bikeList** |
| **START_INDEX** | Integer | 필수 | 요청시작위치 | 정수 입력 (데이터 행 시작번호) |
| **END_INDEX** | Integer | 필수 | 요청종료위치 | 정수 입력 (데이터 행 끝번호) |
| **stationId** | String | 선택 | 대여소ID | 특정 대여소 정보 조회 시 입력 |

### 2.2. 출력값 (Response Fields)

| No | 출력명 | 출력 설명 |
| :--- | :--- | :--- |
| 공통 | **list_total_count** | 총 데이터 건수 |
| 공통 | **RESULT.CODE** | 요청 결과 코드 |
| 공통 | **RESULT.MESSAGE** | 요청 결과 메시지 |
| 1 | **rackTotCnt** | 거치대개수 |
| 2 | **parkingBikeTotCnt** | 자전거주차총건수 |
| 3 | **shared** | 거치율 |
| 4 | **stationLatitude** | 위도 |
| 5 | **stationLongitude** | 경도 |
| 6 | **stationId** | 대여소ID |
| 7 | **stationName** | 대여소이름 |

---

## 3. 공통 결과 코드 (Result Codes)

| 코드 | 메시지 | 설명 |
| :--- | :--- | :--- |
| **INFO-000** | 정상 처리되었습니다 | |
| **INFO-100** | 인증키가 유효하지 않습니다 | |
| **INFO-200** | 해당하는 데이터가 없습니다 | |
| **ERROR-300** | 필수 값이 누락되어 있습니다 | |
| **ERROR-310** | 해당하는 서비스를 찾을 수 없습니다 | |
| **ERROR-336** | 데이터 요청 제한 초과 | 한 번에 최대 1000건 |
| **ERROR-500** | 서버 오류 | |
