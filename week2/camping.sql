select * from camping_info;

-- [실습01]
-- 1. 캠핑장의 사업장명과 지번주소를 출력(단, 사업장명은 NAME, 지번주소는 ADDRESS로 출력)
select 사업장명, 지번주소, 영업상태코드, 영업상태명 from camping_info;

-- 2. 1번 데이터에서 정상 영업 하고 있는 캠핑장만 출력
select 사업장명, 지번주소, 영업상태코드, 영업상태명 from camping_info
where 영업상태코드=1;

-- 3. 양양에 위치한 캠핑장은 몇 개인지 출력
select count(camping_info_id) from camping_info 
where `지번주소` like '강원특별자치도 양양군%';

-- 4. 3번 데이터에서 폐업한 캠핑장은 몇 개인지 출력
select count(camping_info_id) from camping_info 
where `지번주소` like '강원특별자치도 양양군%'
and 영업상태코드=3;

-- 5. 태안에 위치한 캠핑장의 사업장명 출력
select 사업장명 from camping_info 
where `지번주소` like '충청남도 태안군%';

-- 5번 데이터에서 2020년에 폐업한 캠핑장만 출력
select 사업장명, 지번주소, 폐업일자 from camping_info 
where `지번주소` like '충청남도 태안군%'
and 폐업일자 between '2020-01-01' and '2020-12-31'
and 폐업일자 is not null;

-- 제주도와 서울에 위치한 캠핑장은 몇 개인지 출력
select count(camping_info_id) from camping_info 
where `지번주소` like '서울특별시%' or 지번주소 like '제주특별자치도%';
--  
-- [실습02]
-- 해수욕장에 위치한 캠핑장의 사업장명과 인허가일자를 출력
select 사업장명, 인허가일자
from camping_info
where 지번주소 like '%해수%'
or 사업장명 like '%해수%';

-- 제주도 해수욕장에 위치한 캠핑장의 지번주소와 사업장명 출력
select 지번주소, 사업장명 from camping_info ci
where 지번주소 like '제주%'
and 사업장명 like '%해수%';

-- 2번 데이터에서 인허가일자가 가장 최근인 곳의 인허가일자 출력
select 인허가일자 from camping_info ci
where 지번주소 like '제주%'
and 사업장명 like '%해수%'
order by 인허가일자 desc
limit 1;

-- 인천 해수욕장에 위치한 캠핑장 중 영업중인 곳만 출력
select 사업장명, 지번주소, 영업상태명 from camping_info ci
where 지번주소 like '인천%'
and (사업장명 like '%해수%' or 지번주소 like '%해수%')
and 영업상태코드 = 1;

-- 4번 데이터 중에서 인허가일자가 가장 오래된 곳의 인허가일자 출력
select 사업장명, 지번주소, 영업상태명, 인허가일자
from camping_info ci
where 지번주소 like '인천%'
and (사업장명 like '%해수%' or 지번주소 like '%해수%')
and 영업상태코드 = 1
order by 인허가일자
limit 1;

-- 해수욕장에 위치한 캠핑장 중 시설면적이 가장 넓은 곳의 시설면적 출력
select 사업장명, 지번주소, 시설면적
from camping_info ci
where (사업장명 like '%해수%' or 지번주소 like '%해수%')
and 시설면적 is not null
order by 시설면적 desc
limit 1;

-- 해수욕장에 위치한 캠핑장의 평균 시설면적 출력
select avg(시설면적)
from camping_info ci
where (사업장명 like '%해수%' or 지번주소 like '%해수%')
and 시설면적 is not null;

-- [실습03]
-- 캠핑장의 사업장명, 시설면적을 시설면적이 가장 넓은 순으로 출력
select 사업장명, 시설면적
from camping_info
order by 시설면적 desc;

-- 1번 데이터에서 10위까지만 출력
select 사업장명, 시설면적
from camping_info
order by 시설면적 desc
limit 10;

-- 경기도 캠핑장 중에 면적이 가장 넓은 순으로 5개만 출력
select 사업장명, 시설면적, 지번주소
from camping_info
where 지번주소 like '경기%'
order by 시설면적 desc
limit 5;

-- 3번 데이터에서 1위는 제외
select 사업장명, 시설면적, 지번주소
from camping_info
where 지번주소 like '경기%'
order by 시설면적 desc
limit 1, 4;

-- 영업중인 캠핑장 중에서 인허가일자가 가장 오래된 순으로 20개 출력
select 사업장명, 영업상태명, 인허가일자
from camping_info
where 영업상태코드 = 1
order by 인허가일자
limit 20;

-- 2020년 10월 ~2021년 3월 사이에 폐업한 캠핑장의 사업장명과 지번주소 출력
select 사업장명, 지번주소, 영업상태명, 폐업일자
from camping_info
where 폐업일자 is not null
and 폐업일자 between '2020-10-01' and '2021-03-31';

-- 폐업한 캠핑장 중에서 시설면적이 가장 컷던 곳의 사업장명과 시설면적 출력
select 사업장명, 시설면적
from camping_info
where 영업상태코드 = 3
and 시설면적 is not null
order by 시설면적 desc
limit 1;

-- [실습04]
-- 각 지역별 캠핑장 수 출력 (단, 지역은 LOCATION으로 출력)
select 지역구분명, count(camping_info_id)  from camping_info
where 지역구분명 != ''
group by 지역구분명;

-- 1번 데이터를 캠핑장 수가 많은 지역부터 출력
select 지역구분명, count(camping_info_id) as cnt from camping_info
where 지역구분명 != ''
group by 지역구분명
order by cnt desc;

-- 각 지역별 영업중인 캠핑장 수 출력
select 지역구분명, count(camping_info_id) as cnt from camping_info
where 지역구분명 != ''
and 영업상태코드 = 1
group by 지역구분명
order by cnt desc;

-- 3번 데이터에서 캠핑장 수가 300개 이상인 지역만 출력
select 지역구분명, count(camping_info_id) as cnt from camping_info
where 지역구분명 != ''
and 영업상태코드 = 1
group by 지역구분명
having cnt >= 300
order by cnt desc;

-- 년도별 폐업한 캠핑장 수 출력 (단, 년도는 YEAR로 출력)
select date_format(폐업일자, '%Y') as YEAR, count(camping_info_id)
from camping_info ci
where 폐업일자 is not null
group by YEAR
;

-- 5번 데이터를 년도별로 내림차순하여 출력
select date_format(폐업일자, '%Y') as YEAR, count(camping_info_id)
from camping_info ci
where 폐업일자 is not null
group by YEAR
order by YEAR desc
;

-- UPDATE camping_info 
-- SET 폐업일자 = NULL 
-- WHERE 폐업일자 = '' OR 폐업일자 IS NULL;
-- 
-- SELECT 폐업일자
-- FROM camping_info ci  
-- WHERE STR_TO_DATE(폐업일자, '%Y-%m-%d') IS NULL;
-- 
-- -- 1. 데이터를 명시적으로 DATE 형식으로 업데이트 (필요한 경우)
-- UPDATE camping_info 
-- SET 폐업일자 = STR_TO_DATE(폐업일자, '%Y-%m-%d');
-- 
-- -- 2. 컬럼 정의 변경
-- ALTER TABLE camping_info 
-- MODIFY COLUMN 폐업일자 DATE;

commit;