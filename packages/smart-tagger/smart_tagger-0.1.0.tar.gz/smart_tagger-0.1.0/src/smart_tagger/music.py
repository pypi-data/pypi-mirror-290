import smart_tagger.utils as utils
import os
import re
import tinytag


class MusicLibrary:
    CONFIG = utils.load_config()

    def __init__(self, path=CONFIG["DIRECTORY"]):
        self.path = self._handle_directory(path)
        self.songs = self._get_songs()

    def _handle_directory(self, path) -> str:
        """Get the music directory from the config file or the registry.

        Args:
            path (str): The path to the music directory.

        Raises:
            FileNotFoundError: If the directory is not found.

        Returns:
            str: The path to the music directory.
        """
        if 'WINDOWS:' in path:
            import winreg

            subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            music_guid = '{4BD8D571-6D19-48D3-BE97-422220080E43}'

            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey) as key:
                    return winreg.QueryValueEx(key, music_guid)[0]
            except FileNotFoundError:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey) as key:
                        return winreg.QueryValueEx(key, path.split(':')[1])[0]
                except FileNotFoundError:
                    raise FileNotFoundError(
                        "Music directory not found in registry")
        else:
            expanded_path = os.path.expanduser(path)

            if not os.path.exists(expanded_path):
                raise FileNotFoundError(
                    f"Directory not found at {expanded_path}")

            return expanded_path

    def _get_songs(self):
        """Get all the music files in the music directory.

        Returns:
            list: A list of MusicFile objects.
        """
        songs = []

        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                if filename.split('.')[-1] in tinytag.TinyTag.SUPPORTED_FILE_EXTENSIONS:
                    songs.append(MusicFile(os.path.join(root, filename)))

        return songs


class MusicFile:
    def __init__(self, path):
        self.path = path

        tags = self._get_tags()

        self.title = tags.title
        self.artist = tags.artist
        self.album = tags.album
        self.genres = self._get_genres(tags.genre)

    def _get_tags(self):
        """Get the tags from the music file.

        Returns:
            dict: The tags as a dictionary.
        """
        return tinytag.TinyTag.get(self.path)

    def _get_genres(self, genres):
        """Split the genres into a list.

        Args:
            genres (str): The genres as a string.

        Returns:
            list: The genres as a list.
        """
        if genres is None:
            return []

        return re.split(r'(,|;)\s?', genres)


if __name__ == "__main__":
    library = MusicLibrary()
    print(library.songs)
