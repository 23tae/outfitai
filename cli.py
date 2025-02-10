import click
import asyncio
from pathlib import Path
import json
from classify_openai import OpenAIClassifier


@click.group()
def cli():
    """AI Fashion Classifier CLI tool."""
    pass


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--batch', is_flag=True, help='Process multiple images')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def classify(image_path: str, batch: bool, output: str):
    """Classify clothes in images."""
    async def run():
        classifier = OpenAIClassifier()

        if batch:
            # If directory, process all images
            if Path(image_path).is_dir():
                image_paths = [
                    str(p) for p in Path(image_path).glob("*")
                    if p.suffix.lower() in ['.jpg', '.jpeg', '.png']
                ]
                results = await classifier.classify_batch(image_paths)
            else:
                click.echo("Specified path is not a directory")
                return
        else:
            # Process single image
            results = [await classifier.classify_single(image_path)]

        # Output results
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(results, indent=2))

    asyncio.run(run())
