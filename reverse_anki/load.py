from anki.collection import Collection
from html.parser import HTMLParser
from pathlib import Path

class QuestionrParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._enable = False

    def feed(self, data):
        self._data = []
        super().feed(data)
        return self._data
    
    def handle_starttag(self, tag, attrs):
        if tag != 'style':
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
        if tag == 'hr' and ("id", "answer") in attrs:
            self._enable = True

    def handle_data(self, data):
        if len(data.strip()) > 0:
            if self._enable:
                self._data.append(data)
            self._enable = False

answer_parser = AnswerParser()

collection_path = str(Path.home() / "tmp" / "anki" / "collection.anki2")
col = Collection(collection_path)

query="select count(id) from cards"
learnAheadCards = col.db.scalar(query)

print("You have %s learning cards due in Anki" % learnAheadCards) 

for deck in col.decks.all():
    print(deck["name"])

deck_name = "Monthly findings"

for card in col.decks.by_name(deck_name):
    print(card)

debug = False

for card_id in col.find_cards(f'''deck:"{deck_name}"'''):
    card = col.get_card(card_id)
    question_parts = question_parser.feed(card.question())
    answer_parts = answer_parser.feed(card.answer())
    if debug:
        print(card.description())
        print("----")
        print(card.question())
        print("----")
        print(card.answer())
        print("----")
        for d in question_parts:
            print(d)    
        print("----")
        for d in answer_parts:
            print(d)
    if len(question_parts) > 0 and len(answer_parts):
        print(f"{card_id}: {question_parts[0]} -> {answer_parts[0]}")

col.close()