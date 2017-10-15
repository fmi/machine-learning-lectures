import os
import subprocess
import shutil

os.makedirs('compiled-lectures', exist_ok=True)
os.makedirs('slides', exist_ok=True)

files = [name for name in os.listdir('lectures') if name.endswith('.ipynb')]
for lecture in files:
    slug = os.path.splitext(lecture)[0]
    notes_command = ('jupyter nbconvert --to html lectures/{slug}.ipynb --stdout '
                     '> compiled-lectures/{slug}.html').format(slug=slug)
    slides_command = ('jupyter nbconvert --to slides lectures/{slug}.ipynb '
                      '--reveal-prefix=reveal.js --output-dir=slides ').format(
                          slug=slug)
    notes_error_code = subprocess.call(notes_command, shell=True)
    slides_error_code = subprocess.call(slides_command, shell=True)
    if notes_error_code:
        raise RuntimeError("Failed to compile the lectures: {}".format(
            notes_error_code))
    if slides_error_code:
        raise RuntimeError("Failed to compile the slides {}".format(
            slides_error_code))

    shutil.copy('lectures/index.yml', 'compiled-lectures/index.yml')
