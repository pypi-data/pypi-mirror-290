from argparse import ArgumentParser

from loguru import logger

from memician.generator.generator import Generator
from memician.library import db, library
from memician.library.utils import MEMICIAN_PATH

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    lib = library.Library()
    meme_templates = list(lib.meme_templates.values())
    logger.debug(f"Loaded {len(meme_templates)} meme templates: {meme_templates}")

    db = db.Database(meme_templates)
    results = db.search_meme(args.prompt)

    if results:
        top_result = results[0]
        top_meme = meme_templates[top_result[0]]

        logger.info(f"Matched meme {top_meme.name} with distance {top_result[1]}")

        g = Generator(f"{MEMICIAN_PATH}/memician/memes")
        texts = g.texts(prompt=args.prompt, model_class=top_meme.schema_class)

        g.meme(top_meme.name, texts, args.output)
    else:
        logger.error("No meme found for the given prompt.")
