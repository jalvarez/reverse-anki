from reverse_anki.load import QuestionrParser, AnswerParser
from reverse_anki.model import CanonicalCard


def test_question_parser():
    a_question = "Why?"
    formatted_question = f"<style>color: black;</style><p>{a_question}</p>"
    parser = QuestionrParser()

    parsed_question_parts = parser.feed(formatted_question)

    assert parsed_question_parts[0] == a_question


def test_canonical_question_parser():
    a_question = "Why?"
    a_card = CanonicalCard(a_question, "Dunno")
    parser = QuestionrParser()

    parsed_question_parts = parser.feed(a_card.get_formatted_question())

    assert parsed_question_parts[0] == a_question


def test_canonical_answer_parser():
    an_answer = "Dunno"
    a_card = CanonicalCard("Why?", an_answer)
    parser = AnswerParser()

    parsed_answer_parts = parser.feed(a_card.get_formatted_answer())

    assert parsed_answer_parts[0] == an_answer
