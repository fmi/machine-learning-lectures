import os
import subprocess
import shutil

os.makedirs('compiled-lectures', exist_ok=True)

files = [name for name in os.listdir('lectures') if name.endswith('.ipynb')]
for lecture in files:
    slug = os.path.splitext(lecture)[0]
    command = 'jupyter nbconvert --to html lectures/{slug}.ipynb --stdout' \
              '> compiled-lectures/{slug}.html'.format(slug=slug)
    error_code = subprocess.call(command, shell=True)
    if error_code:
        raise RuntimeError("Failed to compile the lectures")

    shutil.copy('lectures/index.yml', 'compiled-lectures/index.yml')
