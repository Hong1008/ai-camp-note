# Yu-Gi-Oh! API by YGOPRODeck (v7)

YGOPRODeck에서 제공하는 무료 유희왕 카드 데이터베이스 API 명세서입니다.

* **최신 버전:** v7 (최종 업데이트: 2025년 9월 22일)
* **기본 속도 제한 (Rate Limiting):** 1초당 최대 20회 요청 가능 (초과 시 1시간 동안 IP 차단)
* **권장 사항:** API 서버의 부하를 줄이기 위해 조회한 데이터 및 이미지는 가급적 **로컬 환경에 다운로드 후 캐싱하여 사용**하는 것을 강력히 권장합니다. (이미지 무단 핫링크 지속 시 IP 차단 처리될 수 있음)

---

## 1. 카드 정보 조회 엔드포인트

특정 카드의 상세 정보나 조건에 맞는 카드 목록을 검색합니다.

* **URL:** `https://db.ygoprodeck.com/api/v7/cardinfo.php`
* **Method:** `GET`
* **주의 사항:** 요청 매개변수(Parameter)를 아무것도 전달하지 않으면 전체 카드 목록을 반환합니다. 잘못된 매개변수 값을 전달하면 `400 Bad Request` 에러와 함께 올바른 값의 가이드가 반환됩니다.

### 📋 요청 매개변수 (Query Parameters)

| 매개변수 | 타입 | 설명 | 예시 |
| --- | --- | --- | --- |
| `name` | String | 카드의 정확한 이름. 파이프(`|`) 문자로 구분하여 다중 검색 가능 | `Baby Dragon|Time Wizard` |
| `fname` | String | 카드 이름 부분 일치(Fuzzy) 검색 | `Magician` |
| `id` | Integer | 카드의 8자리 고유 패스코드 (쉼표 `,` 구분으로 다중 검색 가능, `name`과 동시 사용 불가) | `6983839` |
| `konami_id` | Integer | 코나미 공식 ID (패스코드와 다름) |  |
| `type` | String | 카드 종류 (하단 종류 목록 참조, 쉼표 구분 다중 검색 가능) | `Normal Monster` |
| `race` | String | 몬스터의 종족 또는 마법/함정의 종류 (하단 목록 참조) | `Spellcaster`, `Equip` |
| `attribute` | String | 몬스터 속성 (쉼표 구분 다중 검색 가능) | `dark,light` |
| `atk` / `def` | String | 공격력 / 방어력 수치 필터링 (비교 연산자 사용 가능) | `lt2500` (2500 미만), `gte2000` (2000 이상) |
| `level` | String | 레벨 또는 랭크 (비교 연산자 사용 가능: `lt`, `lte`, `gt`, `gte`) | `lte8` (8 이하) |
| `link` / `scale` | Integer | 링크 마커 수치 / 펜듈럼 스케일 수치 필터링 |  |
| `linkmarker` | String | 링크 마커 방향 필터링 (Top, Bottom, Left, Right 등, 쉼표 구분 가능) | `top,bottom` |
| `cardset` | String | 수록 카드 세트 이름 검색 | `Metal Raiders` |
| `archetype` | String | 카드군(아키타입) 이름 검색 | `Blue-Eyes` |
| `banlist` | String | 금제 포맷 필터링 | `tcg`, `ocg`, `Goat` |
| `format` | String | 특정 게임 포맷 전용 카드 필터링 | `tcg`, `ocg`, `master duel`, `rush duel`, `speed duel` |
| `sort` | String | 정렬 기준 | `atk`, `def`, `name`, `type`, `level`, `id`, `new` |
| `misc` | String | `yes` 설정 시 추가 부가 정보(발매일, 조회수, 텍스트 상 취급 등) 포함 | `yes` |
| `staple` | String | `yes` 설정 시 범용 카드(Staple)만 필터링 | `yes` |
| `has_effect` | Boolean | 효과 존재 여부 필터링 (`true` / `false`) | `true` |
| `startdate` / `enddate` | String | 카드 발매일 범위 필터링 (`YYYY-MM-DD`) | `2000-01-01` |
| `dateregion` | String | 발매일 기준 지역 설정 (기본값: `tcg`) | `tcg`, `ocg` |
| `language` | String | 언어 설정 (이미지는 영어 고정, 텍스트만 변경) | `fr`(프랑스), `de`(독일), `it`(이탈리아), `pt`(포르투갈) |

---

## 2. 주요 부가 엔드포인트

### 🎲 랜덤 카드 조회

* **URL:** `https://db.ygoprodeck.com/api/v7/randomcard.php`
* **설명:** 무작위로 카드 1장의 정보를 반환합니다. (캐싱되지 않음, GET 파라미터 전달 시 에러 발생)

### 📦 전체 세트 목록 조회

* **URL:** `https://db.ygoprodeck.com/api/v7/cardsets.php`
* **설명:** DB에 등록된 모든 카드 세트의 이름, 세트 코드, 카드 수, TCG 발매일을 A-Z 순으로 반환합니다.

### 🔍 특정 세트 정보 조회

* **URL:** `https://db.ygoprodeck.com/api/v7/cardsetsinfo.php`
* **필수 매개변수:** `setcode`
* **예시:** `https://db.ygoprodeck.com/api/v7/cardsetsinfo.php?setcode=SDY-046`

### 🏷️ 전체 아키타입(카드군) 목록 조회

* **URL:** `https://db.ygoprodeck.com/api/v7/archetypes.php`
* **설명:** 등록된 모든 유희왕 카드군 이름을 A-Z 순으로 반환합니다.

### 🔄 DB 버전 체크

* **URL:** `https://db.ygoprodeck.com/api/v7/checkDBVer.php`
* **설명:** 새로운 카드가 추가되거나 데이터가 수정될 때 버전 및 날짜가 갱신됩니다. 클라이언트 측에서 업데이트 여부를 확인할 때 유용합니다.

---

## 3. 파라미터 허용 값 목록 (Values)

### 종족 및 마/함 종류 (`race`)

* **Monster:** `Aqua`, `Beast`, `Beast-Warrior`, `Creator-God`, `Cyberse`, `Dinosaur`, `Divine-Beast`, `Dragon`, `Fairy`, `Fiend`, `Fish`, `Insect`, `Machine`, `Plant`, `Psychic`, `Pyro`, `Reptile`, `Rock`, `Sea Serpent`, `Spellcaster`, `Thunder`, `Warrior`, `Winged Beast`, `Wyrm`, `Zombie`
* **Spell Card:** `Normal`, `Field`, `Equip`, `Continuous`, `Quick-Play`, `Ritual`
* **Trap Card:** `Normal`, `Continuous`, `Counter`

### 카드 종류 (`type`)

* **메인 덱:** `Effect Monster`, `Flip Effect Monster`, `Flip Tuner Effect Monster`, `Gemini Monster`, `Normal Monster`, `Normal Tuner Monster`, `Pendulum Effect Monster`, `Pendulum Effect Ritual Monster`, `Pendulum Flip Effect Monster`, `Pendulum Normal Monster`, `Pendulum Tuner Effect Monster`, `Ritual Effect Monster`, `Ritual Monster`, `Spell Card`, `Spirit Monster`, `Toon Monster`, `Trap Card`, `Tuner Monster`, `Union Effect Monster`
* **엑스트라 덱:** `Fusion Monster`, `Link Monster`, `Pendulum Effect Fusion Monster`, `Synchro Monster`, `Synchro Pendulum Effect Monster`, `Synchro Tuner Monster`, `XYZ Monster`, `XYZ Pendulum Effect Monster`
* **기타:** `Skill Card`, `Token`

---

## 4. 응답 데이터 JSON 예시

`https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Tornado%20Dragon` 요청 시의 반환 포맷 예시입니다.

```json
{
  "data": [
    {
      "id": 6983839,
      "name": "Tornado Dragon",
      "type": "XYZ Monster",
      "frameType": "xyz",
      "desc": "2 Level 4 monsters\nOnce per turn (Quick Effect): You can detach 1 material from this card, then target 1 Spell/Trap on the field; destroy it.",
      "atk": 2100,
      "def": 2000,
      "level": 4,
      "race": "Wyrm",
      "attribute": "WIND",
      "card_sets": [
        {
          "set_name": "Duel Devastator",
          "set_code": "DUDE-EN019",
          "set_rarity": "Ultra Rare",
          "set_rarity_code": "(UR)",
          "set_price": "1.4"
        }
      ],
      "card_images": [
        {
          "id": 6983839,
          "image_url": "https://images.ygoprodeck.com/images/cards/6983839.jpg",
          "image_url_small": "https://images.ygoprodeck.com/images/cards_small/6983839.jpg",
          "image_url_cropped": "https://images.ygoprodeck.com/images/cards_cropped/6983839.jpg"
        }
      ],
      "card_prices": [
        {
          "cardmarket_price": "0.42",
          "tcgplayer_price": "0.48",
          "ebay_price": "2.99",
          "amazon_price": "0.77",
          "coolstuffinc_price": "0.99"
        }
      ]
    }
  ]
}
