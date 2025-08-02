import flet as ft
import flet_audio as fa
from converter.core.src.ebook_parser import parse_text
from converter.core.src.tts_wrapper import Pyttsx3Engine, EdgeTtsEngine
from converter.core.src.audio_processor import process_audio
import os

def main(page: ft.Page):
    page.title = "Ebook to Audiobook Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    audio_player = fa.Audio(
        src="",
        autoplay=False,
    )
    page.overlay.append(audio_player)

    tts_engines = {"pyttsx3": Pyttsx3Engine(), "edge-tts": EdgeTtsEngine()}
    selected_engine = tts_engines["edge-tts"] # Default to edge-tts

    def get_voices_for_engine(engine_name):
        engine = tts_engines.get(engine_name)
        if engine:
            return engine.get_voices()
        return []

    def pick_file_result(e: ft.FilePickerResultEvent):
        selected_file.value = e.files[0].path if e.files else ""
        selected_file.update()

    def convert_ebook(e):
        if not selected_file.value:
            return

        convert_button.disabled = True
        progress_ring.visible = True
        audio_controls.visible = False
        page.update()

        try:
            output_dir = "temp_output"
            os.makedirs(output_dir, exist_ok=True)

            temp_audio_file = os.path.join(output_dir, "temp_audio.wav")
            output_audio_file = os.path.join(output_dir, "output.wav")

            text = parse_text(selected_file.value)

            selected_voice = voice_dropdown.value
            if not selected_voice:
                raise ValueError("Please select a voice.")

            selected_engine.synthesize(text, temp_audio_file, selected_voice)

            process_audio(temp_audio_file, output_audio_file)

            audio_player.src = output_audio_file
            audio_controls.visible = True
            page.update()

        except ValueError as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {err}"))
            page.snack_bar.open = True
        finally:
            convert_button.disabled = False
            progress_ring.visible = False
            page.update()

    def play_audio(e):
        audio_player.resume()

    def pause_audio(e):
        audio_player.pause()

    def restart_audio(e):
        audio_player.seek(0)
        audio_player.resume()

    def update_voices(e):
        nonlocal selected_engine
        selected_engine = tts_engines[engine_dropdown.value]
        voices = get_voices_for_engine(engine_dropdown.value)
        voice_dropdown.options = [ft.dropdown.Option(voice) for voice in voices]
        voice_dropdown.update()

    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)

    selected_file = ft.TextField(label="Selected Ebook", read_only=True)
    engine_dropdown = ft.Dropdown(label="Select TTS Engine", options=[
        ft.dropdown.Option("edge-tts"),
        ft.dropdown.Option("pyttsx3"),
    ], on_change=update_voices, value="edge-tts")
    voice_dropdown = ft.Dropdown(label="Select Voice")
    convert_button = ft.ElevatedButton(text="Convert to Audiobook", on_click=convert_ebook)
    progress_ring = ft.ProgressRing(visible=False)
    
    audio_controls = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.PLAY_ARROW, on_click=play_audio),
            ft.IconButton(icon=ft.Icons.PAUSE, on_click=pause_audio),
            ft.IconButton(icon=ft.Icons.REPLAY, on_click=restart_audio),
        ],
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        ft.Row(
            [
                selected_file,
                ft.ElevatedButton(
                    "Select Ebook",
                    on_click=lambda _: pick_file_dialog.pick_files(
                        allow_multiple=False, allowed_extensions=["txt", "pdf", "docx"]
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row([engine_dropdown, voice_dropdown], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([convert_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
        audio_controls,
    )

    # Initial voice population
    update_voices(None)

ft.app(target=main)