import sys
import os
import logging
import logging.config
from tempfile import NamedTemporaryFile
from anki.lang import set_lang
from anki.collection import Collection
from anki.importing import AnkiPackageImporter
from anki import _backend

from .load import load_cards

_logger = logging.getLogger("import")


def import_apkg(col: Collection, source_path: str):
    importer = AnkiPackageImporter(col, source_path)
    importer.open()
    try:
        importer.run()
    finally:
        importer.close()


if __name__ == "__main__":
    apkg_file = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    logging.config.fileConfig(fname="reverse_anki/resources/logging_config.ini")
    _backend.print = _logger.debug
    set_lang(os.environ.get("ANKI_LANG", "en"))
    with NamedTemporaryFile(suffix=".anki2") as tmp_file:
        col = Collection(tmp_file.name)
        import_apkg(col, apkg_file)
        _logger.info("Apkg file imported")
        for deck in col.decks.all():
            deck_name = deck["name"]
            num_cards = 0
            for card in load_cards(col, deck_name):
                num_cards += 1
                if limit is not None and num_cards >= limit:
                    break
            _logger.info(f"{num_cards} card in the '{deck_name}' deck")
