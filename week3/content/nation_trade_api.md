# 국가별 수출입 현황 API 명세

본 문서는 공공데이터포털에서 제공하는 관세청 `국가별 수출입 현황` API의 요청 인자 및 출력값 정보를 정리한 것입니다.

## 1. 기본 정보
- **서비스 URL**: `http://apis.data.go.kr/1220000/nationtrade/getNationtradeList`
- **데이터 포맷**: XML

## 2. 요청 인자 (Request Parameters)

| 변수명 | 타입 | 필수 여부 | 변수 설명 | 값 설명 |
| :--- | :--- | :--- | :--- | :--- |
| **serviceKey** | String | 필수 | 인증키 | 공공데이터포털에서 발급받은 서비스키 |
| **strtYymm** | String | 필수 | 시작년월 | YYYYMM 형식 (예: 202301) |
| **endYymm** | String | 필수 | 종료년월 | YYYYMM 형식 (예: 202312) |
| **cntyCd** | String | 선택 | 국가코드 | ISO 국가코드 (예: US, CN 등) |

---

## 3. 출력값 (Response Fields)

### 3.1. 응답 헤더 (Header)
| 출력명 | 타입 | 설명 |
| :--- | :--- | :--- |
| **resultCode** | String | 결과코드 |
| **resultMsg** | String | 결과메시지 |

### 3.2. 응답 바디 (Body - Item)
| 출력명 | 타입 | 설명 |
| :--- | :--- | :--- |
| **year** | String | 기간 (조회 기준 년월) |
| **statCdCntnKor1** | String | 국가명 (한글) |
| **statCd** | String | 국가코드 |
| **expCnt** | Number | 수출건수 |
| **expDlr** | Number | 수출금액 (달러) |
| **impCnt** | Number | 수입건수 |
| **impDlr** | Number | 수입금액 (달러) |
| **balPayments** | Number | 무역수지 (달러) |

---

## 4. 참고 사항
- 시작년월(`strtYymm`)과 종료년월(`endYymm`)의 범위가 너무 클 경우 응답 속도가 느려질 수 있습니다.
- 국가코드(`cntyCd`)를 입력하지 않으면 전 국가를 대상으로 조회합니다.
