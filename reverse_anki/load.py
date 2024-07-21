from anki.collection import Collection
from html.parser import HTMLParser
from pathlib import Path
from typing import Generator
from .model import CanonicalCard
import logging

_logger = logging.getLogger("load")


class QuestionrParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._enable = False

    def feed(self, data):
        self._data = []
        super().feed(data)
        return self._data

    def handle_starttag(self, tag, attrs):
        if tag != "style":
            self._enable = True

    def handle_data(self, data):
        if len(data.strip()) > 0:
            if self._enable:
                self._data.append(data)
            self._enable = False


question_parser = QuestionrParser()


class AnswerParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._enable = False

    def feed(self, data):
        self._data = []
        super().feed(data)
        return self._data

    def handle_starttag(self, tag, attrs):
        if tag == "hr" and ("id", "answer") in attrs:
            self._enable = True

    def handle_data(self, data):
        if len(data.strip()) > 0:
            if self._enable:
                self._data.append(data)
            self._enable = False


answer_parser = AnswerParser()


def load_cards(
    col: Collection, deck_name: str, debug: bool = False
) -> Generator[CanonicalCard, None, None]:

    for card_id in col.find_cards(f'''deck:"{deck_name}"'''):
        card = col.get_card(card_id)
        question_parts = question_parser.feed(card.question())
        answer_parts = answer_parser.feed(card.answer())
        if len(question_parts) > 0 and len(answer_parts):
            # _logger.debug(card_id)
            # _logger.debug(question_parts[0])
            # _logger.debug(answer_parts[0])
            canonical_card = CanonicalCard(card_id, question_parts[0], answer_parts[0])
            yield canonical_card


if __name__ == "__main__":
    collection_path = str(Path.home() / "tmp" / "anki" / "collection.anki2")
    deck_name = "Monthly findings"

    try:
        col = Collection(collection_path)

        for card in load_cards(collection_path, deck_name, True):
            print(card)
    finally:
        col.close()
