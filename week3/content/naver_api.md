# 네이버 데이터랩 - 통합 검색어 트렌드 조회 API 명세

본 문서는 네이버 데이터랩에서 제공하는 `통합 검색어 트렌드 조회` API의 요청 및 응답 규격을 정리한 것입니다.

## 1. 기본 정보

- **요청 URL**: `https://openapi.naver.com/v1/datalab/search`
- **프로토콜**: HTTPS
- **HTTP 메서드**: POST
- **인증 방식**: HTTP Header 사용
  - `X-Naver-Client-Id`: 애플리케이션 등록 시 발급받은 클라이언트 아이디
  - `X-Naver-Client-Secret`: 애플리케이션 등록 시 발급받은 클라이언트 시크릿
  - `Content-Type`: `application/json`

---

## 2. 요청 파라미터 (Request Body - JSON)

| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| **startDate** | String | Y | 조회 시작 날짜 (yyyy-mm-dd) |
| **endDate** | String | Y | 조회 종료 날짜 (yyyy-mm-dd) |
| **timeUnit** | String | Y | 구간 단위 (`date`, `week`, `month`) |
| **keywordGroups** | Array | Y | 주제어 묶음 (최대 5개 주제어) |
| - **groupName** | String | Y | 주제어 명칭 |
| - **keywords** | Array | Y | 주제어에 포함될 검색어들 (최대 20개) |
| **device** | String | N | 기기 범위 (`pc`, `mo`, 설정 안 함: 전체) |
| **gender** | String | N | 성별 (`m`: 남성, `f`: 여성, 설정 안 함: 전체) |
| **ages** | Array | N | 연령대 (1~11 코드값 배열) |

---

## 3. 응답 속성 (Response Fields - JSON)

| 속성 | 타입 | 설명 |
| :--- | :--- | :--- |
| **startDate** | String | 실제 조회 시작 날짜 (yyyy-mm-dd) |
| **endDate** | String | 실제 조회 종료 날짜 (yyyy-mm-dd) |
| **timeUnit** | String | 구간 단위 |
| **results** | Array | 각 주제어 그룹별 검색 추이 결과 |
| - **title** | String | 주제어 명칭 |
| - **keywords** | Array | 해당 주제어에 포함된 검색어 리스트 |
| - **data** | Array | 구간별 상세 데이터 |
| -- **period** | String | 구간 시작 날짜 (yyyy-mm-dd) |
| -- **ratio** | Number | 해당 구간 내 상댓값 (최고치를 100으로 설정) |

---

## 4. 결과 코드 (Result Codes)

| 코드 | HTTP 상태 코드 | 메시지 | 설명 |
| :--- | :--- | :--- | :--- |
| **400** | 400 | 잘못된 요청 | 파라미터 오루 등 확인 |
| **403** | 403 | 권한 없음 | API 설정에서 '데이터랩' 항목 활성화 확인 |
| **500** | 500 | 서버 오류 | 네이버 내부 서버 오류 |