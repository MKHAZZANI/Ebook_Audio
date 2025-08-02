from django.shortcuts import render
from django.http import FileResponse
from .core.src.ebook_parser import parse_text
from .core.src.tts_wrapper import CoquiEngine, BarkEngine
from .core.src.audio_processor import process_audio
import os

def index(request):
    if request.method == 'POST':
        ebook_file = request.FILES['ebook_file']
        tts_engine_name = request.POST['tts_engine']
        voice = request.POST['voice']

        # Create a temporary directory for output files
        output_dir = "temp_output"
        os.makedirs(output_dir, exist_ok=True)

        # Save the uploaded file temporarily
        temp_ebook_path = os.path.join(output_dir, ebook_file.name)
        with open(temp_ebook_path, 'wb+') as destination:
            for chunk in ebook_file.chunks():
                destination.write(chunk)

        # Define output file paths
        temp_audio_file = os.path.join(output_dir, "temp_audio.wav")
        output_audio_file = os.path.join(output_dir, "output.wav")

        # 1. Parse the ebook
        text = parse_text(temp_ebook_path)

        # 2. Synthesize audio
        if tts_engine_name == 'coqui':
            tts_engine = CoquiEngine()
        else:
            tts_engine = BarkEngine()
        tts_engine.synthesize(text, temp_audio_file, voice)

        # 3. Process the audio
        process_audio(temp_audio_file, output_audio_file)

        return FileResponse(open(output_audio_file, 'rb'), as_attachment=True, filename='output.wav')

    else:
        coqui_engine = CoquiEngine()
        bark_engine = BarkEngine()
        voices = {
            'coqui': coqui_engine.get_voices(),
            'bark': bark_engine.get_voices()
        }
        return render(request, 'converter/index.html', {'voices': voices})