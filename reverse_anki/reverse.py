import sys
import logging
from anki.collection import Collection, ExportAnkiPackageOptions, DeckIdLimit
from anki.decks import Deck
from .load import load_cards
from .model import CanonicalCard

_logger = logging.getLogger(__name__)


def create_deck(col: Collection, deck_name: str, remove_existing: bool = False) -> Deck:
    if remove_existing:
        existing_deck = col.decks.by_name(deck_name)
        if existing_deck:
            col.decks.remove([existing_deck["id"]])
    deck_id = col.decks.id(deck_name)
    return col.decks.get(deck_id)


def add_card_to_deck(col: Collection, deck_name: str, card: CanonicalCard):
    default_note_type = {"name": "Basic", "id": 1650405100350}
    deck_dict = col.decks.by_name(deck_name)
    deck_id = deck_dict["id"]
    new_note = col.new_note(default_note_type)
    new_note.fields = [
        card.get_formatted_question(),
        card.get_formatted_answer(),
        "",
        "",
    ]
    col.addNote(new_note)
    col.set_deck(new_note.card_ids(), deck_id)
    return new_note


def reverse_deck(collection_path: str, deck_name: str) -> str:
    num_processed_cards = 0
    try:
        col = Collection(collection_path)
        new_deck_name = f"Reversed {deck_name}"
        create_deck(col, new_deck_name)
        existing_cards = load_cards(col, deck_name)
        for card in existing_cards:
            num_processed_cards += 1
            add_card_to_deck(col, new_deck_name, card.reverse())
        _logger.info(f"Number of processed cards: {num_processed_cards}")
        return new_deck_name
    finally:
        col.close()


def export(collection_path: str, deck_name: str, out_path: str):
    try:
        col = Collection(collection_path)
        options = ExportAnkiPackageOptions()
        deck = col.decks.by_name(deck_name)
        limit = DeckIdLimit(deck_id=deck["id"])
        col.export_anki_package(out_path=out_path, options=options, limit=limit)
    finally:
        col.close()


if __name__ == "__main__":
    collection_path = sys.argv[1]
    deck_name = sys.argv[2]
    out_path = sys.argv[3]

    logging.basicConfig(level=logging.INFO)
    _logger.info(f"source collection: {collection_path}")
    new_deck_name = reverse_deck(collection_path, deck_name)
    _logger.info(f"Reversed cards in the '{new_deck_name} 'deck of {out_path}")
    export(
        collection_path,
        new_deck_name,
        out_path,
    )
