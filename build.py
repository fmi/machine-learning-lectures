import os
import subprocess
import shutil
import argparse

import yaml

'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.5.0/css/print/paper.css'

NOTES_COMMAND = ('jupyter nbconvert --to html lectures/{slug}.ipynb --stdout '
                 '> compiled-lectures/{slug}.html')
SLIDES_COMMAND = ('jupyter nbconvert --to slides lectures/{slug}.ipynb '
                  '--reveal-prefix=https://cdnjs.cloudflare.com/ajax/libs/'
                  'reveal.js/3.5.0 --output-dir=slides ')


os.makedirs('compiled-lectures', exist_ok=True)
os.makedirs('slides', exist_ok=True)


parser = argparse.ArgumentParser(description='Compile lectures')
parser.add_argument('--lectures', metavar='L', type=int, nargs='+',
                    help='lecture indexes to compile as written in index.yaml',
                    required=False)
args = parser.parse_args()


INDEX = yaml.load(open('lectures/index.yml'))


def build_lecture(slug):
    notes_error_code = subprocess.call(NOTES_COMMAND.format(slug=slug),
                                       shell=True)
    slides_error_code = subprocess.call(SLIDES_COMMAND.format(slug=slug),
                                        shell=True)
    if notes_error_code:
        raise RuntimeError("Failed to compile the lectures: {}".format(
            notes_error_code))
    if slides_error_code:
        raise RuntimeError("Failed to compile the slides {}".format(
            slides_error_code))

    shutil.copy('lectures/index.yml', 'compiled-lectures/index.yml')


if args.lectures:
    for lecture_index in args.lectures:
        build_lecture(INDEX[lecture_index]['slug'])
else:
    files = [name for name in os.listdir('lectures') if name.endswith('.ipynb')]
    for lecture in files:
        slug = os.path.splitext(lecture)[0]
        build_lecture(slug)
