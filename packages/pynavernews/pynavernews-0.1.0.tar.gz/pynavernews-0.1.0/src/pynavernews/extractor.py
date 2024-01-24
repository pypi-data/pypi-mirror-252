from __future__ import annotations
from datetime import datetime, timedelta
import logging
import string
from typing import Any, AsyncGenerator, Iterable
from bs4 import Tag

import hxsoup


class FieldMissingError(Exception):
    pass


class Extractor:
    client: hxsoup.AsyncClient

    def extract_from_string(self, string: str) -> AsyncGenerator[Any, dict[str, Any]]:
        return self.extract(hxsoup.SoupTools(string))

    async def extract(self, response: hxsoup.SoupTools) -> AsyncGenerator[Any, dict[str, Any]]:
        headlines = response.soup_select(
            "#main_content > div.list_body.newsflash_body > ul.type06_headline > li")
        for headline in headlines:
            try:
                yield await self._extract_headline(headline)
            except FieldMissingError as e:
                try:
                    title = headline.select("a")[-1].text.strip()
                except Exception:
                    title = "headline"

                logging.warning(f"Failed to parse {title} because {e} field is missing.")

    @staticmethod
    def _assert_tag(tag: Tag | None, name: str) -> Tag:
        if tag is None:
            raise FieldMissingError(name)
        return tag

    async def _extract_headline(self, headline: Tag) -> dict[str, Any]:
        if (image_tag := headline.select_one("img")) is None:
            image_url = None
        else:
            image_url = image_tag["src"]

        title_anchor = headline.select("a")[-1]
        article_url = title_anchor["href"]
        assert isinstance(article_url, str)
        title = title_anchor.text.strip()

        summary = self._assert_tag(headline.select_one("span.lede"), "summary").text
        publisher = self._assert_tag(headline.select_one("span.writing"), "publisher").text
        date_string = self._assert_tag(headline.select_one("span.date"), "date_string").text

        return {
            "image_url": image_url,
            "article_url": article_url,
            "title": title,
            "summary": summary,
            "publisher": publisher,
            "date_string": self.reformat_date(date_string).isoformat(),
        }

    @staticmethod
    def reformat_date(raw_date: str, standard_time: datetime | None = None) -> datetime:
        """네이버의 시간 포맷을 datetime으로 변경합니다.

        38분전, 14시간전, 3일전같은 단위도 파싱됩니다.

        `일전` 때문에 최대 하루까지 오차가 발생할 수 있습니다.

        >>> FullExtractor.reformat_date("2020.01.05. 오후 11:21")
        datetime.datetime(2020, 1, 5, 23, 21)
        """
        if standard_time is None:
            standard_time = datetime.now()

        raw_date = raw_date.strip()

        if raw_date.endswith("분전"):
            minutes_delta = int(raw_date.removesuffix("분전"))
            return standard_time - timedelta(minutes=minutes_delta)

        if raw_date.endswith("시간전"):
            hours_delta = int(raw_date.removesuffix("시간전"))
            return standard_time - timedelta(hours=hours_delta)

        if raw_date.endswith("일전"):
            days_delta = int(raw_date.removesuffix("일전"))
            return standard_time - timedelta(days=days_delta)

        return datetime.strptime(raw_date.replace("오후", "PM").replace("오전", "AM"),
                                 "%Y.%m.%d. %p %I:%M")


class FullExtractor(Extractor):
    def __init__(
        self,
        client: hxsoup.AsyncClient | None = None,
        normalizer: Normalizer | None = None,
    ) -> None:
        """
        client는 여기에서 정의하는 대신 사용하기 직전에 주입시켜도 됩니다.
        normalizer가 None이면 정규화를 하지 않습니다.
        """
        self.normalizer = normalizer or Normalizer(normalize=False)
        if client is not None:
            self.client = client

    async def _extract_headline(self, headline: Tag) -> dict[str, Any]:
        result = await super()._extract_headline(headline)
        result.update(await self.fetch_and_extract_article(result["article_url"]))
        return result

    async def fetch_and_extract_article(self, article_url: str) -> dict[str, Any]:
        """subclassing을 통해 직접 기능을 개선시킬 수 있습니다."""
        response = await self.client.get(article_url)
        article = "\n".join(self._assert_tag(response.soup_select_one("#dic_area"), "article").stripped_strings)

        if (reporter_name_tag := response.soup_select_one("span.byline_s")) is None:
            reporter_name = None
        else:
            reporter_name = reporter_name_tag.text

        article = self.normalizer.normalize(article) or article
        return {
            "reporter_name": reporter_name,
            "content": article,
        }


class Normalizer:
    def __init__(
        self,
        normalize: bool = True,
        remove_footer: bool = True,
    ) -> None:
        self.remove_footer = remove_footer
        self.normalize_article = normalize

    def normalize(self, content: str) -> str | None:
        if self.normalize_article and self.hangeul_ratio(content) < 0.5:
            return None

        return "\n".join(
            line
            for line in content.splitlines()
            if not self.normalize_article or line[-1] == "."
            if not self.remove_footer or not line.startswith("▶")
        )

    def hangeul_ratio(self, text: str | Iterable[str], ignore_whitespace: bool = True, normal_character_only: bool = False) -> float:
        if ignore_whitespace:
            text = (c for c in text if c not in set(string.whitespace))
        if normal_character_only:
            text = filter(self.is_normal_character, text)
        text = list(text)

        korean_characters_count = sum(1 for c in text if ord("가") <= ord(c) <= ord("힣"))
        return korean_characters_count / len(text)

    @staticmethod
    def is_normal_character(c: str) -> bool:
        return (
            ord("0") <= ord(c) <= ord("9")
            or ord("a") <= ord(c) <= ord("z")
            or ord("A") <= ord(c) <= ord("Z")
            or ord("가") <= ord(c) <= ord("힣")
        )
