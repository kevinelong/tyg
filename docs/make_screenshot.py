"""Regenerate docs/demo.svg and docs/demo-frames.txt from the real game frames.

The frames come from pilot.demo, which drives pilot's own Game.draw(), so the
picture cannot show anything the program does not print. pilot/test.py
recomputes both files and fails when either is stale.

    python3 docs/make_screenshot.py

The animation is vector text on a rounded panel: it stays crisp at any zoom,
needs no palette and no image codec, carries its frames as text so a diff shows
what changed, and regenerating it byte for byte needs nothing but Python.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from pilot import demo                                                    # noqa: E402

FAMILY = ('ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace')
WIDTH, HEIGHT = 440, 224
PAD = 18
LINE_HEIGHT = 17              # DejaVu Sans Mono's own line box at 14px: no extra
                              # leading, the way a terminal packs rows
FONT_SIZE = 14
BASELINE = 30                 # first baseline, so the 11 line block sits centred
ADVANCE = 8.4                 # per character, forced through textLength
STEP = 0.5                    # seconds each frame is held
PANEL, EDGE, TEXT = '#ffffff', '#d1d9e0', '#1f2328'
SVG = os.path.join(ROOT, 'docs', 'demo.svg')
DUMP = os.path.join(ROOT, 'docs', 'demo-frames.txt')

ESCAPES = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}


def escape(line):
    return ''.join(ESCAPES.get(character, character) for character in line)


def frame_markup(index, frame, cycle):
    """One frame: shown only in its own slot, and frame 0 shows if SMIL is off."""
    delay = -(cycle - index * STEP)
    held = round(STEP / cycle, 6)
    released = round(held + 0.00001, 6)
    return [
        '    <g class="frame" opacity="{0}">'.format(1 if index == 0 else 0),
        '      <animate attributeName="opacity" calcMode="discrete"'
        ' values="1;1;0;0" keyTimes="0;{0:g};{1:g};1" dur="{2:g}s" begin="{3:g}s"'
        ' repeatCount="indefinite"/>'.format(held, released, cycle, delay),
    ] + [
        '      <text x="{0}" y="{1}" textLength="{2}" lengthAdjust="spacingAndGlyphs"'
        ' xml:space="preserve">{3}</text>'.format(
            PAD, BASELINE + row * LINE_HEIGHT, round(len(line) * ADVANCE, 2),
            escape(line))
        for row, line in enumerate(frame)
    ] + ['    </g>']


def svg(frames=None):
    """The whole document, as text, with no timestamps: byte-for-byte stable."""
    frames = demo.frames() if frames is None else frames
    cycle = len(frames) * STEP
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" '
        'viewBox="0 0 {0} {1}" role="img" aria-labelledby="title desc">'.format(WIDTH, HEIGHT),
        '  <title id="title">tyg running in a terminal</title>',
        '  <desc id="desc">A 9x9 board of dots with the character ^ and a treasure x,'
        ' over the lines "Treasures: 0 of 10" and "a/d turn  s step  h j k l or arrows'
        ' move  q quit". The animation walks the character up and right onto the'
        ' treasure, turns it in place, steps it forward, and bumps it into the top edge,'
        ' where it turns 180 degrees.</desc>',
        '  <rect x="0.5" y="0.5" width="{0}" height="{1}" rx="8" fill="{2}" stroke="{3}"/>'
        .format(WIDTH - 1, HEIGHT - 1, PANEL, EDGE),
        '  <g font-family=\'{0}\' font-size="{1}" fill="{2}">'.format(FAMILY, FONT_SIZE, TEXT),
    ]
    for index, frame in enumerate(frames):
        parts += frame_markup(index, frame, cycle)
    parts += ['  </g>', '</svg>', '']
    return '\n'.join(parts)


def main():
    frames = demo.frames()
    with open(SVG, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(svg(frames))
    with open(DUMP, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(demo.text_dump())
    print('{0} frames over a {1:g}s loop -> {2} ({3} bytes)'.format(
        len(frames), len(frames) * STEP, os.path.relpath(SVG, ROOT), os.path.getsize(SVG)))
    print('text of the same frames -> {0}'.format(os.path.relpath(DUMP, ROOT)))


if __name__ == '__main__':
    main()
