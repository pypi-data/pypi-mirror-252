# pynavernews

## Introduction

`pynavernews`는 [`canrevan`](https://github.com/affjljoo3581/canrevan)의 코드 중 일부를 재사용해 만든 네이버 웹툰 크롤링 라이브러리입니다.

이 라이브러리의 필요성에 대해서는 [canrevan](https://github.com/affjljoo3581/canrevan#introduction)에 자세히 역설되어 있습니다.

하지만 이 라이브러리는 자연어 데이터만을 위한 라이브러리는 아니며, 네이버 뉴스에서 종합적인 데이터를 불러오는 라이브러리입니다.

## Installation

```console
pip install pynavernews
```

`navernews`가 **아닙니다**. 다른 패키지를 설치하지 않도록 주의해 주세요.

## Build from source

우선 git과 python을 설치하고 레포지토리를 클론하세요.

```console
git clone https://github.com/ilotoki0804/pynavernews.git
```

그런 다음 가상 환경을 생성하고 활성화하세요.

```console
echo 윈도우의 경우
py -3.12 -m venv .venv
.venv\Scripts\activate

echo UNIX인 경우
python3.12 -m venv .venv
.venv/Scripts/activate
```

poetry를 설치하고 의존성을 설치하세요.

```console
pip install poetry
poetry install --no-root
```

`build.py`를 실행하세요.

```console
python build.py
```

이제 `dist`에 빌드된 `whl` 파일과 `tar.gz` 파일이 나타납니다.

## How to use

수집하고자 하는 카테고리의 id를 [네이버 뉴스](https://news.naver.com/)에서 확인합니다.

## Example

2020년 5월 1일부터 31일까지 5개의 페이지에 대한 정치(100)와 경제(101) 카테고리에 대한 뉴스를 수집하는 코드는 다음과 같이 짤 수 있습니다.

```python
from datetime import datetime
from pathlib import Path

from pynavernews import (
    string_date_range,
    construct_index_page_urls,
    fetch_and_store_news_raw_data,
)

date_range = string_date_range(datetime(2024, 1, 1), datetime(2024, 1, 15), 1)
index_page_urls = construct_index_page_urls([100, 101], date_range, 5)
await fetch_and_store_news_raw_data(
    index_page_urls,
    concurrent_tasks=10,
    result_path=Path("result.jsonperline"),
    timeout=20,
    extractor=None,
    proceed=True,
)
```

성공적으로 뉴스 기사가 수집되었다면, 다음과 같이 json 데이터가 한 줄에 하나씩 저장됩니다.

```json
{"original_url": "https://news.naver.com/main/list.nhn?mode=LSD&mid=shm&sid1=101&date=20240114&page=1", "image_url": "https://imgnews.pstatic.net/image/origin/018/2024/01/14/5654670.jpg?type=nf106_72", "article_url": "https://n.news.naver.com/mnews/article/018/0005654670?sid=101", "title": "중동정세 불안에 유가 ‘꿈틀’…산업부, 국내 수급상황 점검", "summary": "정부가 주말인 14일 정유 4사 등 관계기업·기관과 국내 석유·가스 수급 현황과 국제유가 영향 점검에 나섰다. 최남호(오른쪽)  …", "publisher": "이데일리", "date_string": "2024-01-14T23:16:00"}
```

이때 모든 데이터는 문자열이고 image_url는 null이 될 수 있습니다.

만약 `summery` 뿐만이 아닌 전체 기사를 불러오고 싶다면 FullExtractor를 사용하세요.

```python
from datetime import datetime
from pathlib import Path

from pynavernews import (
    string_date_range,
    construct_index_page_urls,
    fetch_and_store_news_raw_data,
    FullExtractor,
)

date_range = string_date_range(datetime(2024, 1, 1), datetime(2024, 1, 15), 1)
index_page_urls = construct_index_page_urls([100, 101], date_range, 5)
await fetch_and_store_news_raw_data(
    index_page_urls,
    concurrent_tasks=10,
    result_path=Path("result-full.jsonperline"),
    timeout=20,
    extractor=FullExtractor(),
    proceed=True,
)
```

그러면 다음과 같이 조금 더 상세한 정보와 함께 전체 데이터가 `content`에 나오게 됩니다. `summary`가 없어지진 않습니다.

```json
{"original_url": "https://news.naver.com/main/list.nhn?mode=LSD&mid=shm&sid1=101&date=20240101&page=5", "image_url": "https://imgnews.pstatic.net/image/origin/005/2024/01/01/1663580.jpg?type=nf106_72", "article_url": "https://n.news.naver.com/mnews/article/005/0001663580?sid=101", "title": "上上, 현실이 되나", "summary": "증권가는 이미 올해 코스피에 대한 장밋빛 전망이 한창이다. 주요국의 통화정책 기조 전환과 국내 수출 회복 전망 등이 맞물리면서  …", "publisher": "국민일보", "date_string": "2024-01-01T20:54:00", "reporter_name": "신재희 기자(jshin@kmib.co.kr)", "content": "증권가, 증시 장밋빛 전망 잇달아\n금리 인하·수출 회복 낙관론 우세\n코스피 2655 마감, 1년새 18.7% ↑\n올해 최대 3000선 돌파 기대감\n이미지를 크게 보려면 국민일보 홈페이지에서 여기를 클릭하세요\n증권가는 이미 올해 코스피에 대한 장밋빛 전망이 한창이다. 주요국의 통화정책 기조 전환과 국내 수출 회복 전망 등이 맞물리면서 증시에 긍정적 흐름이 이어질 것이라는 예상이다.\n1일 금융투자업계에 따르면 코스피 지수는 지난해 마지막 거래일인 28일 2655.28에 장을 마감했다. 코스피 지수는 지난달 미국 연방준비제도(Fed·연준)의 금리 인하 기대감에 힘입어 계속 상승 기세를 이어갔다. 지난해 첫 거래일 시초가와 비교한 연간 상승률은 18.7%다.\n증권가는 올해 코스피 전망 범위를 상향 조정했다. ‘코스피 3000’을 기대하는 증권사도 나왔다. 증시 전망을 가장 낙관적으로 본 곳은 대신증권으로 코스피 변동 폭을 2350~2850으로 제시했다. 특히 미국이 오는 3월 금리 인하를 단행할 경우 코스피 3000선 돌파도 가능할 것으로 봤다.\nKB증권(상단만 2810으로 제시)과 신한투자증권(2200~2800)도 코스피가 2800대까지 오를 수 있을 것으로 내다봤다. 한국투자증권(2300~2750), NH투자증권(2300~2750). 삼성증권(2200~2750)은 2750을 코스피 고점으로 예상했다. 하나증권은 코스피 변동 폭을 2350~2700으로 제시해 상단이 가장 낮았다.\n상고하저? 상저하고? 엇갈린 전망\n증권사들은 연간 시장 흐름에 대해서는 다소 엇갈린 관측을 내놨다. 주요한 ‘변곡점’으로 꼽히는 미국의 금리 인하와 대통령 선거를 기준으로 증시의 상승·하락 시점이 다를 것이라는 분석이다.\n대신증권과 NH투자증권은 하반기 반등을 기대하는 ‘상저하고’ 흐름을 예상했다. 상반기 저점을 찍고 하반기로 갈수록 기업 이익과 경제가 점차 회복되면서 증시도 함께 상승세를 탈 것이라는 예측이다. 이경민 대신증권 연구원은 “상반기는 물가 수준, 연준의 통화정책 스탠스, 시장의 금리 인하 기대가 뒤섞이며 글로벌 금융시장이 혼란스러운 흐름을 보일 것”이라며 “다만 하반기 금리 인하 사이클 진입 시 시장의 방향성은 명확해질 것”이라고 말했다.\n김병연 NH투자증권 연구원은 “미 대선이 치러지는 해의 6월과 11월은 정책 불확실성이 확대되는 가운데 통상 9월이 고점을 찍는다”며 “국내 주식시장도 1분기 낮은 지수대에서 출발해 3분기 고점을 형성할 것”이라고 말했다.\n반면 기준금리 인하를 기점으로 증시가 고점을 찍은 뒤 조정을 받을 것이라는 ‘상고하저’ 의견도 적지 않다. 한국투자증권과 신한투자증권 등은 미국 대선 등 정치 이벤트가 증시 불확실성을 키울 것으로 전망했다.\n노동길 신한투자증권 연구원은 “상반기 재고순환 사이클 회복과 반도체 경기 개선에 따른 코스피 상승세가 기대되고, 하반기에는 미국 대선을 앞둔 경계감과 경기 사이클의 하강 국면, 2025년 증시 이슈들이 부담이 될 것”이라고 예측했다. 김대준 한국투자증권 연구원도 “상반기는 금리 인하와 정부의 증시 부양책 효과가 이어지다 2분기 고점을 찍고 하반기 들어 정책효과 소멸과 대외 정치 리스크로 지수가 흔들릴 수 있다”며 ‘상고하저’ 전망에 힘을 실었다.\n다만 국내 증시가 지난해 말부터 미 연준의 금리 인하 기대감을 선반영한 측면이 있어 향후 과도한 기대감은 경계해야 한다는 목소리도 적지 않다. 정용택 IBK투자증권 연구원은 “2024년은 이미 높아진 추세적 불확실성에 선거, 지정학적 위험 등 외적 위험이 증가하는 시기”라며 “시장의 기대가 급격하게 낙관적으로 변하고 있고 주요 투자은행의 전망치가 빠르게 상향조정되고 있지만 경제와 투자환경은 (낙관하기에) 여전히 조심스럽다”고 말했다.\n올해 증시 주도는 ‘반도체’\n증권업계는 올해 증시를 이어갈 주도주로 단연 반도체를 꼽고 있다. 침체기를 맞았던 반도체 시장이 올해부터 ‘슈퍼 사이클’로 접어들 것이라는 기대감에서다. 반도체업계는 올해 전 세계 메모리 반도체 시장(D램·낸드) 규모가 지난해보다 66% 증가한 1310억 달러(약 170조원)를 기록하고, 2025년에는 전년 대비 39% 증가한 1820억 달러(약 235조원)를 기록할 것으로 예상하고 있다.\n이미 지난해 말부터 반도체주는 영향력을 확대하고 있다. SK하이닉스는 2년 만에 시총 2위를 탈환했고, 삼성전자도 증시 마지막 거래일이던 지난달 28일 7만8500원에 거래를 마치며 2년 만에 ‘8만 전자’ 탈환을 눈앞에 뒀다. 지난해 첫 거래일과 비교하면 각각 41.4%, 89.4% 오른 수치다.\n올해에도 이들 기업의 가파른 회복세가 예상된다. 금융정보업체 에프앤가이드에 따르면 삼성전자의 연결 기준 영업이익은 지난해 7조3443억원에서 올해 33조8109억원, 2025년 49조2039억원으로 늘어날 것으로 전망된다. SK하이닉스의 올해 연간 영업이익 컨센서스도 8조3671억원으로 2021년(21조4103억원) 이후 3년 만에 최대 실적이 가능할 것이라는 시장의 기대가 나온다.\n대형 반도체주뿐 아니라 소부장(소재·부품·장비) 종목에 대한 기대도 커지고 있다. 특히 주가 반등 국면에서는 상대적으로 시가총액이 적은 중소형 소부장 종목의 반등 폭이 더 클 수 있다는 관측이다."}
```

이때 모든 데이터는 문자열이고 image_url와 reporter_name은 null이 될 수 있습니다.

다시 읽을 때는 `f.readline()`을 이용하면 됩니다.

## License

pynavernews는 Apache-2.0 라이선스로 공유됩니다.

pynavernews는 [canrevan](https://github.com/affjljoo3581/canrevan) 레포지토리의 코드 중 일부를 포함하고 있습니다.

이 레포지토리의 예시와 테스트 데이터에는 위키백과, 위키피디아, 부산일보, 연합뉴스TV, KBS, YTN, 이코노미스트, 뉴시스, 데일리안, SBS Biz, 국민일보의 저작물이 포함되어 있습니다.

## Changelog

* 0.1.0: 시작
