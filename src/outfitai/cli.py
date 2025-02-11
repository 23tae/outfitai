import click
from pathlib import Path
import json
from .classifier.openai_classifier import OpenAIClassifier
import asyncio


@click.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--batch', '-b', is_flag=True, help='Process multiple images')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def cli(image_path: str, batch: bool, output: str):
    """Classify clothing items in images."""
    try:
        classifier = OpenAIClassifier()

        async def process():
            if batch:
                if not Path(image_path).is_dir():
                    click.echo("Specified path is not a directory")
                    return
                return await classifier.classify_batch(image_path)
            else:
                return [await classifier.classify_single(image_path)]

        results = asyncio.run(process())

        # Output results
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(results, indent=2))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()
