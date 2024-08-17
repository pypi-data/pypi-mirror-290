from pathlib import Path
from typing import Annotated, cast, get_args

import typer

from mozyq.types import Preset

app = typer.Typer()


def path_completion(incomplete: str):
    folder = Path(incomplete).parent

    return [
        f'{folder}/{file}'
        for file in folder.iterdir()]


def preset_completion():
    return get_args(Preset)


Target = Annotated[
    Path,
    typer.Argument(autocompletion=path_completion)]


PresetCompletion = Annotated[
    str,
    typer.Argument(autocompletion=preset_completion)]


@ app.command()
def build_video(
        seed: Target,
        video_mp4: Path = Path('video.mp4'),
        master_size: int = 630,
        tile_size: int = 30,
        num_transitions: int = 10,
        fps: int = 180,
        crf: int = 18,
        preset: PresetCompletion = 'medium'):

    from mozyq.builder import build_video as bv
    from mozyq.engine import save_video_json as svj

    video_mp4.parent.mkdir(parents=True, exist_ok=True)
    video_json = video_mp4.with_suffix('.json')

    svj(
        seed=seed,
        tile_folder=seed.parent,
        master_size=master_size,
        tile_size=tile_size,
        num_transitions=num_transitions,
        video_json=video_json)

    bv(
        video_json=video_json,
        video_mp4=video_mp4,
        steps_per_transition=fps,
        crf=crf,
        preset=cast(Preset, preset))


# #@app.command()
# def login():
#     import asyncio

#     from mozyq import login as lg
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(lg())


def main():
    app()
