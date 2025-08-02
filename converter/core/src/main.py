import click
from ebook_parser import parse_text
from tts_wrapper import Pyttsx3Engine
from audio_processor import process_audio

@click.group()
def cli():
    pass

@cli.command()
@click.argument("ebook_path")
@click.option("--output", default="output.wav", help="Output audio file path.")
def convert(ebook_path, output):
    """Converts an ebook to an audiobook."""
    click.echo(f"Converting {ebook_path} to {output}...")

    try:
        # 1. Parse the ebook
        text = parse_text(ebook_path)
        click.echo("Ebook parsed successfully.")

        # 2. Synthesize audio
        tts_engine = Pyttsx3Engine()
        voices = tts_engine.get_voices()
        if not voices:
            click.echo("No TTS voices found on your system.")
            return

        temp_audio_file = "temp_audio.wav"
        tts_engine.synthesize(text, temp_audio_file, voices[0])
        click.echo("Audio synthesized successfully.")

        # 3. Process the audio
        process_audio(temp_audio_file, output)
        click.echo("Audio processed successfully.")

        click.echo(f"Audiobook saved to {output}")

    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    cli()