from moviepy.editor import VideoFileClip
from openai import OpenAI
import click
import os
from pydub import AudioSegment
import math
from ytdoc import __version__

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

def extract_audio(video_path, output_path):
    try:
        # Load the video file
        video = VideoFileClip(video_path)
        
        # Extract the audio
        audio = video.audio
        
        # Write the audio to an MP3 file
        audio.write_audiofile(output_path, codec='mp3')
        
        print(f"Audio extracted successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def transcribe_audio_chunk(audio_path):
    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        prompt='keep the filling words and aaa eee hmmms'
    )
    return transcript.text

def transcribe_audio(audio_path, chunk_length=600):  # chunk_length in seconds, default is 10 minutes
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) / 1000  # Duration in seconds
    chunks = math.ceil(duration / chunk_length)
    all_transcripts = []

    for i in range(chunks):
        start_time = i * chunk_length * 1000
        end_time = start_time + chunk_length * 1000
        chunk = audio[start_time:end_time]
        chunk_path = audio_path.replace(".mp3", f"_chunk{i}.mp3")
        chunk.export(chunk_path, format="mp3")
        print(f"Transcribing chunk {i+1}/{chunks}...")
        transcript_text = transcribe_audio_chunk(chunk_path)
        all_transcripts.append(transcript_text)
        os.remove(chunk_path)  # Remove chunk file after processing to save space
    
    full_transcript = " ".join(all_transcripts)
    return full_transcript

# Other functions remain the same ...

def rewrite_script(input_text):
    messages = [
        {"role": "system", "content": "You are an expert scriptwriter with a flair for making stories more exciting and engaging. Your goal is to improve the storytelling and excitement of the given script."},
        {"role": "user", "content": "Please rewrite the following script to make it more exciting and help me improve my storytelling capabilities."},
        {"role": "user", "content": f"Original Script: {input_text}"},
        {"role": "user", "content": "Please provide the rewritten script below:"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        # max_tokens=2048,
        stop=None,
        temperature=0.1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    corrected_text = response.choices[0].message.content.strip()
    return corrected_text.strip()

def correct_transcription(input_text):
    messages = [
        {"role": "system", "content": "You are an assistant proficient in correcting transcription errors and understanding the context of technical terms and acronyms."},
        {"role": "user", "content": f"This is a transcription correction task. Certain terms have been incorrectly transcribed. Please correct these errors and ensure the final text accurately reflects the terminology and context."},
        {"role": "user", "content": f"Original Transcription: {input_text}"},
        {"role": "user", "content": "1. Review the provided text.\n2. Identify key terms and context.\n3. Correct misinterpretations.\n4. Enhance the accuracy.\nOriginal errors include misinterpreting like 'RPA' as 'IPA'."},
        {"role": "user", "content": "Please provide the corrected text below:"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        # max_tokens=2048,
        stop=None,
        temperature=0.1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    corrected_text = response.choices[0].message.content.strip()
    return corrected_text.strip()

def generate_youtube_title_description(corrected_transcription, additional_prompt):
    with open("static_prompt.txt") as f:
        static_prompts = f.readlines()
    
    messages = [
        {"role": "system", "content": "You are an expert in creating compelling YouTube titles and descriptions to attract viewers."},
        {"role": "user", "content": "Based on the following corrected transcription, generate a compelling YouTube video title and a detailed video description."},
    ]
    
    for static_prompt in static_prompts:
        messages.append({"role":  "user",  "content":  static_prompt})

    if additional_prompt:
        {"role": "user", "content": "Please include the following additional context when creating the YouTube title and description: " + additional_prompt},
    
    messages += [
        {"role": "user", "content": f"Corrected Transcription: {corrected_transcription}"},
        {"role": "user", "content": "Please provide the title and description below."}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1024,
        stop=None,
        temperature=0.1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    corrected_text = response.choices[0].message.content.strip()
    return corrected_text.strip()

@click.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.argument('additional_prompt', type=str)
@click.option("--no-extract", is_flag=True, show_default=True, default=False)
@click.option("--no-transcribe", is_flag=True, show_default=True, default=False)
@click.option("--no-fix", is_flag=True, show_default=True, default=False)
@click.option("--rewrite", is_flag=True, show_default=True, default=False)
def main(video_path, output_path, additional_prompt, no_extract, no_transcribe, no_fix, rewrite):
    """
    Extract audio from a video file and save it as an MP3 file.

    VIDEO_PATH: Path to the input video file.
    OUTPUT_PATH: Path to save the extracted audio file (mp3).
    """
    # Extract audio from the provided video file
    if not no_extract:
        extract_audio(video_path, output_path)
    else:
        output_path = video_path
    if not no_transcribe:
        print("Transcribing audio...")
        output_text = transcribe_audio(output_path)
        print(output_text)
        with open(output_path + ".txt", "w") as file:
            file.write(output_text)
    else:
        with open(output_path + ".txt", "r") as file:
            output_text = file.read()
        print(output_text)
    
    if not no_fix:
        # Correct transcription
        print("Correcting transcription...")
        correct_text = correct_transcription(output_text)
        with open(output_path + "_fixed.txt", "w") as file:
            file.write(correct_text)
    else:
        with open(output_path + "_fixed.txt", "r") as file:
            correct_text = file.read()
    
    click.echo(click.style(correct_text, fg='yellow'))

    if rewrite:
        correct_text = rewrite_script(correct_text)
        with open(output_path + "_rewrite.txt", "w") as file:
            file.write(correct_text)
        click.echo(click.style(correct_text, fg='yellow'))
    # Generate YouTube title and description
    print("Generating YouTube title and description...")
    youtube_text = generate_youtube_title_description(correct_text, additional_prompt)
    with open(output_path + "_youtube.txt", "w") as file:
        file.write(youtube_text)
    click.echo(click.style(youtube_text, fg='green'))

if __name__ == "__main__":
    main()