from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
media_directory=os.path.join(BASE_DIR)
print(media_directory)