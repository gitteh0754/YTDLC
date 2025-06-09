from pytubefix import YouTube
import subprocess
import os
import typer
from rich import print
import sys

app = typer.Typer(name="ytdlc")

@app.command()
def download(link, mediatype):
    mdt = mediatype.lower()
    if mdt not in ["audio", "video"]:
        raise ValueError("argument MEDIATYPE must be \"audio\" or \"video\".")
    else:
        yt = YouTube(link)
        
        vstreams = yt.streams.filter(mime_type="video/mp4").order_by(attribute_name="resolution")
        astreams = yt.streams.filter(only_audio=True, mime_type="audio/mp4").order_by(attribute_name="abr")
        
        vstream = vstreams.last()
        astream = astreams.last()
        
        astream.download()
        if mdt == "video":
            vstream.download()
        
            audio_file = os.getcwd() + "/" + yt.title + ".m4a"
            video_file = os.getcwd() + "/" + yt.title + ".mp4"
            final_output = os.getcwd() + "/" + yt.title + ".final.mp4"

            FFMPEG_BIN = ""
            if getattr(sys, "frozen", False):
                FFMPEG_BIN = os.path.dirname(sys.executable) + "/ffmpeg.exe"
            elif __file__:
                FFMPEG_BIN = os.path.dirname(__file__) + "/ffmpeg.exe"
            else:
                FFMPEG_BIN = os.getcwd() + "/ffmpeg.exe"

            command = [
                    FFMPEG_BIN, '-fflags', '+genpts', '-i', video_file, '-i', audio_file,
                    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', final_output
            ]    

            if os.path.exists(final_output):
                out = "x"
                while out not in "yn":
                    out = input("Overwrite {}? [y/N] ".format(yt.title + ".final.mp4")).lower()
                if out == "y":
                    os.remove(final_output)
                elif out == "n":
                    pass
        
            subprocess.call(command, stdout=open(os.devnull, "wb"), stderr=open(os.devnull, 'wb'))
            
            if os.path.exists(final_output):
                print(f"[bright_green]Merging complete![/bright_green]")
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                if os.path.exists(video_file):
                    os.remove(video_file)

            else:
                print("[red]Error: Merging failed.[/red]")
    


@app.command()
def version():
    print("[red]You[/red]Tube Download CLI - by [blue]Parteh[/blue] - version 1.0.0")

if __name__ == '__main__':
    app()