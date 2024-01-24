from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Iterable, Iterator, NoReturn

from httpx._types import TimeoutTypes
import hxsoup
import tqdm

from .extractor import Extractor


def string_date_range(start_date: datetime, end_date: datetime, step: int = 1) -> Iterator[str]:
    """
    end_date를 포함하지 않는다는 점을 주의하세요.

    >>> list(Crawler.date_range(datetime(2020, 1, 1), datetime(2020, 1, 5), 1))
    ['20200101', '20200102', '20200103', '20200104', '20200105']
    """
    return (
        (start_date + timedelta(days=date_delta)).strftime("%Y%m%d")
        for date_delta in range(0, (end_date - start_date).days, step)
    )


def construct_index_page_urls(
    categories: Iterable[int],
    dates: Iterable[str],
    max_pages_per_date: int,
) -> Iterator[str]:
    return (
        f"https://news.naver.com/main/list.nhn?mode=LSD&mid=shm&sid1={category}&date={date}&page={page}"
        for date in dates
        for category in categories
        for page in range(1, max_pages_per_date + 1)
    )


async def fetch_and_store_news_raw_data(
    index_page_urls: Iterable[str],
    concurrent_tasks: int,
    result_path: Path,
    timeout: TimeoutTypes = None,
    extractor: Extractor | None = None,
    proceed: bool = True,
    progress: bool = True,
) -> None:
    """proceed가 True인 경우(기본값) 파일 내용을 삭제하지 않고 이어서 가고, False라면 내용을 제거합니다."""
    if extractor is None:
        extractor = Extractor()
    url_queue = iter(tqdm.tqdm(index_page_urls)) if progress else iter(index_page_urls)
    async with hxsoup.AsyncClient(
        headers=hxsoup.DEV_HEADERS,
        timeout=timeout,
        follow_redirects=True,
    ) as client:
        try:
            result_quene = asyncio.Queue()
            extractor.client = client
            tasks = [
                asyncio.create_task(
                    _worker(url_queue, client, extractor, result_quene)
                ) for _ in range(1, concurrent_tasks + 1)
            ]
            result_handler = asyncio.create_task(
                _result_handler(result_quene, result_path, "a" if proceed else "w")
            )
            for task in tasks:
                await task
            result_handler.cancel()
        finally:
            del extractor.client


async def _result_handler(result_quene: asyncio.Queue, result_path: Path, file_mode: str) -> NoReturn:
    with open(result_path, file_mode, encoding="utf-8") as f:
        while True:
            result = await result_quene.get()
            json.dump(result, f, ensure_ascii=False)
            f.write("\n")


async def _worker(
    url_queue: Iterator[str],
    client: hxsoup.AsyncClient,
    extractor: Extractor,
    result_quene: asyncio.Queue,
) -> None:
    while True:
        try:
            url = next(url_queue)
        except StopIteration:
            return

        response = await client.get(url)
        async for result in extractor.extract(response):
            await result_quene.put({"original_url": url} | result)
