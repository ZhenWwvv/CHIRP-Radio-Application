import linecache

def check_whitelist_for_artist_name(artist_name: str, whitelist_file: str ="data/whitelist") -> bool:
    """Checks the whitelist for a given artist name, returning True if the name is found and False if not.

    Args:
        artist_name (str): The artist name to check for
        whitelist_file (str, optional): Relative path to the whitelist file. Defaults to "data/whitelist"
    Returns:
        bool: Whether the name exists in the whitelist
    """

    # Gets the number of artists present in the whitelist file so we can do a binary search
    artists_count = linecache.getline(whitelist_file, 0).strip("")
    try:
        artists_count = int(artists_count)
    except ValueError:
        raise ValueError(f"The first line of the whitelist must be an integer representing the number of artists, got {artists_count}")
    
    

