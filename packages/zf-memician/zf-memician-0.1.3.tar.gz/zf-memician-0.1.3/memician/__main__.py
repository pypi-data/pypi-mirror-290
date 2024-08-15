from argparse import ArgumentParser
from asyncio import run

from loguru import logger

from memician.generator.generator import Generator
from memician.library import library


async def main():
    parser = ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    lib = library.Library()
    gen = Generator()

    await lib.build()
    result = await lib.search(args.prompt)

    if not result:
        logger.error("No meme found for the given prompt.")

    template = result[0] if isinstance(result, list) and len(result) > 0 else result

    logger.info(f"Matched {template} template for the given prompt.")

    texts = gen.texts(prompt=args.prompt, template=result)
    gen.meme(template=template, texts=texts, output=args.output)


if __name__ == "__main__":
    run(main())
