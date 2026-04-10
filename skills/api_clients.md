# Skill: API 수집 전문가 클라이언트 구축

본 문서는 프로젝트 내의 모든 외부 API 연동 클라이언트를 구축할 때 준수해야 하는 표준 패턴과 기술적 규격을 정의합니다.

---

## 1. 핵심 철학 (Core Philosophy)

1. **Zero-DTO (성능 최적화)**: 
   - 대용량 데이터 처리 시 Pydantic 객체 생성 오버헤드를 방지하기 위해 별도의 DTO(Data Transfer Object) 클래스를 사용하지 않습니다.
   - 데이터는 `List[dict]` 형태로 수입하여 곧바로 `Pandas DataFrame`으로 변환합니다.

2. **Raw-Field Harmony (직관성)**:
   - 스키마의 변수명은 API 응답의 실제 필드명과 1:1로 일치시켜 별칭(Alias) 관리에 따른 복잡성을 제거하고 IDE의 자동 완성 기능을 극대화합니다.

---

## 2. Pandera 스키마 표준 규격

모든 데이터프레임 검증은 `pandera.pandas.DataFrameModel`을 상속받은 클래스에서 수행합니다.

### 2.1. 필수 설정 및 스태틱 메서드
```python
import pandera.pandas as pa
from pandera.typing import Series

class ServiceSchema(pa.DataFrameModel):
    # 1. 원본 필드명을 변수명으로 정의
    FIELD_NAME_1: Series[str]
    FIELD_NAME_2: Series[int]
    
    @staticmethod
    def validate_df(data: List[dict]) -> pd.DataFrame:
        """데이터 변환 및 검증을 담당하는 표준 메서드"""
        df = pd.DataFrame(data)
        return ServiceSchema.validate(df)

    class Config:
        strict = True  # 정의되지 않은 컬럼이 유입될 경우 에러 발생
        coerce = True  # 데이터 타입 자동 변환 허용 (API의 문자열 숫자를 int로 변환 등)
```

---

## 3. 클라이언트 구현 가이드

### 3.1. 구성 요소
1. **인증 정보 관리**: 모든 URL과 API Key는 `config.py`를 통해 중앙 집중 관리합니다.
2. **평탄화(Flattening)**: 중첩된(Nested) JSON/XML 응답은 데이터프레임 생성이 용이하도록 사전에 평탄화된 `List[dict]` 구조로 변환합니다.
3. **페이지네이션(Pagination)**: 서울시 API 등 1000건 제한이 있는 경우, 반복문과 인덱스 계산을 통해 전수 수집 로직을 포함합니다.

### 3.2. 표준 코드 구조 (Boilerplate)
```python
def get_service_data(start_index: int = 1, end_index: int = 1000) -> Optional[List[dict]]:
    """API 호출 및 원본 데이터 리스트 반환"""
    url = f"{BASE_URL}/{start_index}/{end_index}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        # ... 파싱 및 평탄화 로직 ...
        return data
    except Exception as e:
        print(f"Request failed: {e}")
    return None
```

---

## 4. 작업 절차 (Workflow)

1. **명세 확인**: [week3/content/](file:///home/hong/project/ai-camp-note/week3/content/) 폴더 내에 API 명세서(`.md`)를 먼저 작성합니다.
2. **환경 변수 등록**: `.env`에 키를 추가하고 `config.py`에서 매핑합니다.
3. **스키마 정의**: `DataFrameModel`을 정의하고 `coerce=True`를 설정합니다.
4. **함수 구현**: 에러 핸들링과 평탄화 로직이 포함된 수집 함수를 작성합니다.
5. **검증**: 메인 블록(`if __name__ == "__main__":`)에서 실제 수집 및 스키마 검증 테스트를 수행합니다.
