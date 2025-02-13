import click
import json
from pathlib import Path
import asyncio
from typing import Optional
from .classifier.factory import ClassifierFactory
from .config.settings import Settings
from .error.exceptions import ClothingClassifierError


async def process_images(
    classifier_factory: ClassifierFactory,
    settings: Settings,
    image_path: str,
    batch: bool
) -> list:
    """
    이미지 처리 로직
    """
    try:
        classifier = classifier_factory.create_classifier(settings)

        if batch:
            if not Path(image_path).is_dir():
                raise click.UsageError("Batch mode requires a directory path")
            return await classifier.classify_batch(image_path)
        else:
            return [await classifier.classify_single(image_path)]

    except Exception as e:
        raise ClothingClassifierError(f"Error processing images: {str(e)}")


def save_results(results: list, output_path: Optional[str]) -> None:
    """
    결과 저장 또는 출력
    """
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        click.echo(f"Results saved to {output_path}")
    else:
        click.echo(json.dumps(results, indent=2, ensure_ascii=False))


@click.group()
def cli():
    """OutfitAI - AI-powered clothing classification tool"""
    pass


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--batch', '-b', is_flag=True, help='Process multiple images from directory')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def classify(
    image_path: str,
    batch: bool,
    output: Optional[str],
):
    """Classify clothing items in images"""
    try:
        settings = Settings()

        # 이미지 처리
        results = asyncio.run(
            process_images(ClassifierFactory, settings, image_path, batch)
        )

        # 결과 저장/출력
        save_results(results, output)

    except ClothingClassifierError as e:
        click.echo(f"Classification error: {str(e)}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        raise click.Abort()
