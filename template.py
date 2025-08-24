import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s')

list_of_files = [
"src/__init__.py",
"src/helper.py",
"src/prompt.py",
".env",
"setup.py",
"app.py",
"research/trials.ipynb",
]

for file_path in list_of_files:
    filepath = Path(file_path)
    filedir,filename=os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file: {filename}")

    if not (os.path.exists(filepath) and os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as fp:
            pass
            logging.info(f"Created empty file: {file_path}")

    else:
        logging.info(f"File already exists and is not empty: {file_path}, skipping creation.")