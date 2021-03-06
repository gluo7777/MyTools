from __future__ import unicode_literals
import click
from cli.scripts.utility import CLI
from cli.scripts.config import Properties
import subprocess
import youtube_dl
import os

# Properties
props = Properties('Video')
FFMPEG_EXEC = 'ffmpeg.executable'
def YT(name): return f'youtube.{name}'


YT_PLAYLIST = YT('playlist')
YT_OUT_DIR = YT('directory')


def my_hook(d):
    if d['status'] == 'finished':
        click.echo('Done downloading, now converting ...')
    else:
        click.echo('Downloading...')


# See: https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
YT_OPTIONS = {
    'format': 'bestaudio/best', 'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }], 'progress_hooks': [my_hook], 'ignoreerrors': True, 'prefer_ffmpeg': True
}
YT_FILE_FORMAT = '%(title)s.%(ext)s'

cli = CLI(props)


@click.group(name='video')
def commands():
    pass


@commands.command('youtube', help='Download videos from youtube using ffmpeg')
@click.option('-p', '--playlist', required=False, help='Link to youtube playlist')
@click.option('-o', '--out', default='./youtube/downloads', help='Directory to place downloaded files')
@click.option('-f', '--first', type=int, required=False, default=1, help='Start playlist index. Defaults to 1')
@click.option('-l', '--last', type=int, required=False, default=-1, help='End playlist index. Defaults to last.')
def download_from_youtube(playlist, out, first, last):
    # cached
    playlist_ = cli.process_optional('YouTube playlist', YT_PLAYLIST, playlist)
    out_ = cli.process_optional('Download directory', YT_OUT_DIR, out)

    options = {}
    options.update(YT_OPTIONS)
    options.update({'playliststart': first})

    if last > -1:
        options.update({'playlistend': last})

    outdir = os.path.abspath(out_)
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    options.update({'outtmpl': f"{outdir}/{YT_FILE_FORMAT}"})

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([playlist_])
