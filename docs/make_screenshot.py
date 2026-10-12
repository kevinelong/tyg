"""Regenerate docs/demo.gif and docs/demo-frames.txt from the real game frames.

The frames come from pilot.demo, which drives pilot's own Game.draw(), so the
picture cannot show anything the program does not print. pilot/test.py
recomputes the frames and fails when docs/demo-frames.txt is stale.

Run from the repository root, anywhere ffmpeg and DejaVuSansMono are present
(WSL has both):

    python3 docs/make_screenshot.py

Styling matches the rest of the README: white panel, 18px padding, 14px
DejaVu Sans Mono at 21px per line, the same numbers as the SVG card this
replaced. A GIF carries one palette, so it cannot follow the reader's theme.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from pilot import demo                                                    # noqa: E402

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
WIDTH, HEIGHT = 440, 268      # even: lavfi's colour source will not give an odd height
PAD = 18
LINE_HEIGHT = 21
FONT_SIZE = 14
TOP = 22                       # centres the 11 line block in the panel
PANEL, TEXT = '0xffffff', '0x1f2328'
RATE = 2                       # frames per second -> a 0.5s GIF delay per frame
GIF = os.path.join(ROOT, 'docs', 'demo.gif')
DUMP = os.path.join(ROOT, 'docs', 'demo-frames.txt')


def drawtext(line, y):
    return ('drawtext=fontfile={0}:textfile={1}:fontcolor={2}:fontsize={3}'
            ':x={4}:y={5}'.format(FONT, line, TEXT, FONT_SIZE, PAD, y))


def render(frame, index, directory):
    """One PNG per frame: a panel, then one drawtext per line of the frame."""
    filters = []
    for row, line in enumerate(frame):
        path = os.path.join(directory, 'line_{0:02d}.txt'.format(row))
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(line)
        filters.append(drawtext(path, TOP + row * LINE_HEIGHT))
    png = os.path.join(directory, 'frame_{0:03d}.png'.format(index))
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'lavfi',
        '-i', 'color=c={0}:s={1}x{2}'.format(PANEL, WIDTH, HEIGHT),
        '-vf', ','.join(filters), '-frames:v', '1', png,
    ], check=True)
    return png


def encode(pngs, target):
    """Join the frames into one looping GIF with a crisp, dithered-free palette."""
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-framerate', str(RATE), '-i',
        os.path.join(os.path.dirname(pngs[0]), 'frame_%03d.png'),
        '-vf', 'split[a][b];[a]palettegen=max_colors=4[p];'
               '[b][p]paletteuse=dither=none',
        '-loop', '0', target,
    ], check=True)


def main():
    frames = demo.frames()
    with open(DUMP, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(demo.text_dump())

    directory = tempfile.mkdtemp(prefix='tyg-frames-')
    try:
        pngs = [render(frame, index, directory) for index, frame in enumerate(frames)]
        encode(pngs, GIF)
    finally:
        shutil.rmtree(directory, ignore_errors=True)

    print('{0} frames at {1}fps -> {2} ({3} bytes)'.format(
        len(frames), RATE, os.path.relpath(GIF, ROOT), os.path.getsize(GIF)))
    print('text of the same frames -> {0}'.format(os.path.relpath(DUMP, ROOT)))


if __name__ == '__main__':
    main()
