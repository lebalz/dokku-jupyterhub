def new_save(self, savefile):
    """Do the TTS API request and write result to file.

    Args:
        savefile (string): The path and file name to save the ``mp3`` to.

    Raises:
        :class:`gTTSError`: When there's an error with the API request.

    """
    from pathlib import Path
    savefile = Path(savefile)
    savefile = str(Path(get_ipython().home_dir, 'work', savefile.name))
    with open(str(savefile), 'wb') as f:
        self.write_to_fp(f)
        log.debug("Saved to %s", savefile)

gTTS.save = new_save