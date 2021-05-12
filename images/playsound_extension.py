

from IPython.display import Audio
from pathlib import Path

def _playsoundJupyter(sound, block=True):
   sound = Path(sound)
   sound = str(Path(get_ipython().home_dir, 'work', sound.name))
   audio = Audio(sound, autoplay=False)
   display(audio)

from platform import system
system = system()

if system == 'Windows':
    playsound = _playsoundWin
elif system == 'Darwin':
    playsound = _playsoundOSX
else:
    playsound = _playsoundJupyter