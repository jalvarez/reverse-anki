from dataclasses import dataclass
from anki.cards import Card


@dataclass
class CanonicalCard:
    id: str
    question: str
    answer: str

    def reverse(self) -> "CanonicalCard":
        return CanonicalCard(self.id, self.answer, self.question)

    def get_formatted_question(self) -> str:
        return """<style>.card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                    }
                    </style><b>%s</b>
                """ % (
            self.question
        )

    def get_formatted_answer(self) -> str:
        return """<style>.card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                    }
                    </style><b>%s</b>

                    <hr id=answer>

                    <div>%s</div>
                """ % (
            self.question,
            self.answer,
        )
