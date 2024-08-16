import os



def get_paths(freq, dataset):
    freq_identifier = f'_{freq}.csv'
    return [path for path in os.listdir(os.path.join('datasets', dataset)) if path.endswith(freq_identifier)]


def rename_files_in_directory(directory, replacements):
    # List all files in the given directory
    for file in os.listdir(directory):
        # Construct the full path to the file
        old_path = os.path.join(directory, file)

        # Apply all replacements to the filename
        new_name = file
        for old_string, new_string in replacements:
            new_name = new_name.replace(old_string, new_string)

        # Construct the full path with the new file name
        new_path = os.path.join(directory, new_name)

        # Rename the file if the name has changed
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed '{old_path}' to '{new_path}'")