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
DARK = {'PANEL': '#161b22', 'EDGE': '#30363d', 'TEXT': '#e6edf3'}
SVG = os.path.join(ROOT, 'docs', 'demo.svg')
DUMP = os.path.join(ROOT, 'docs', 'demo-frames.txt')

ESCAPES = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}


def escape(line):
    return ''.join(ESCAPES.get(character, character) for character in line)


def style(cycle):
    """The stylesheet, built by concatenation: no .format() to mangle the braces."""
    return '\n'.join([
        '    .panel { fill: ' + PANEL + '; stroke: ' + EDGE + '; }',
        '    .text { fill: ' + TEXT + '; }',
        '    .frame { opacity: 0; animation: step ' + str(cycle) + 's linear infinite; }',
        '    .f0 { opacity: 1; }',           # if animations never run, frame 0 still shows
        '    @keyframes step { 0% { opacity: 1 } 7.1428% { opacity: 1 }'
        ' 7.1429% { opacity: 0 } 100% { opacity: 0 } }',
        '    @media (prefers-reduced-motion: reduce) { .frame { animation: none } }',
        '    @media (prefers-color-scheme: dark) {',
        '      .panel { fill: ' + DARK['PANEL'] + '; stroke: ' + DARK['EDGE'] + '; }',
        '      .text { fill: ' + DARK['TEXT'] + '; }',
        '    }',
    ])


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
        '  <style>',
        style(cycle),
        '  </style>',
        '  <rect class="panel" x="0.5" y="0.5" width="{0}" height="{1}" rx="8"/>'
        .format(WIDTH - 1, HEIGHT - 1),
        '  <g class="text" font-family=\'{0}\' font-size="{1}">'.format(FAMILY, FONT_SIZE),
    ]
    for index, frame in enumerate(frames):
        delay = -(cycle - index * STEP)      # each frame shows in its own 0.5s slot
        parts.append('    <g class="frame f{0}" style="animation-delay: {1:g}s">'
                     .format(index, delay))
        for row, line in enumerate(frame):
            parts.append(
                '      <text x="{0}" y="{1}" textLength="{2}" '
                'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{3}</text>'.format(
                    PAD, BASELINE + row * LINE_HEIGHT, round(len(line) * ADVANCE, 2),
                    escape(line)))
        parts.append('    </g>')
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
