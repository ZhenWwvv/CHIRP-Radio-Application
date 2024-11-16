import linecache

def check_whitelist_for_artist_name(artist_name: str, whitelist_file: str ="data/whitelist") -> int:
    """Checks the whitelist for a given artist name, returning True if the name is found and False if not.

    Args:
        artist_name (str): The artist name to check for
        whitelist_file (str, optional): Relative path to the whitelist file. Defaults to "data/whitelist"
    Returns:
        int: The line in the whitelist where the artist is, or 0 if none
    """

    # Gets the number of artists present in the whitelist file so we can do a binary search
    artists_count = linecache.getline(whitelist_file, 1).strip()
    try:
        artists_count = int(artists_count)
    except ValueError:
        raise ValueError(f"The first line of the whitelist must be an integer representing the number of artists, got {artists_count}")
    
    # Perform a binary search
    low = 2
    high = artists_count

    while low <= high:
        middle = (low+high)//2
        middle_artist = linecache.getline(whitelist_file, middle).strip()

        if middle_artist == artist_name:
            return middle
        elif artist_name < middle_artist:
            high = middle-1
        else:
            low = middle+1

    return 0

def whitelist_alphabetize(whitelist_file) -> None:
    # Alphabetizes the provided file. Helper function.
    with open(whitelist_file, "r") as f:
        lines = f.readlines()

    lines.sort()

    with open(whitelist_file, "w") as f:
        f.writelines(lines)

print(check_whitelist_for_artist_name("The Beatles"))
print(check_whitelist_for_artist_name("!!!"))
print(check_whitelist_for_artist_name("Fleetwood Mac"))