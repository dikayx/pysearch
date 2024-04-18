import os
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime

import fnmatch
import psutil
from simple_term_menu import TerminalMenu

def main():
    developer = "Dan Koller"
    version = "1.0.0"
    note = f"Version {version} by {developer}"
    banner = f"""
    ---------------------------------------------------
     _____        _____                     _     
    |  __ \      / ____|                   | |    
    | |__) |   _| (___   ___  __ _ _ __ ___| |__  
    |  ___/ | | |\___ \ / _ \/ _` | '__/ __| '_ \ 
    | |   | |_| |____) |  __/ (_| | | | (__| | | |
    |_|    \__, |_____/ \___|\__,_|_|  \___|_| |_|
            __/ |                                 
           |___/                                  

    {note}
    ---------------------------------------------------
    """
    print(banner)

    options = ["Search in a drive or volume", "Search in a directory", "Exit"]
    main_menu = TerminalMenu(options, menu_cursor_style=("fg_green", "bold"))
    menu_entry_index = main_menu.show()

    if menu_entry_index == 0:
        search_in_volume()
    elif menu_entry_index == 1:
        search_in_directory()
    elif menu_entry_index == 2:
        exit()
    else:
        # This should never happen
        print("Invalid option selected. Exiting the program...")
        sys.exit(1)

def get_results_file():
    """Generate a results file name with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    results_file = f"results-{timestamp}.txt"
    return results_file

def get_volumes():
    """Get the list of volumes on the system."""
    partitions = psutil.disk_partitions(all=True)
    volumes = [partition.mountpoint for partition in partitions]
    return volumes

def select_volume():
    volume_names = get_volumes()
    volume_names.append("Exit")
    volume_menu = TerminalMenu(volume_names, menu_cursor_style=("fg_green", "bold"))
    menu_entry_index = volume_menu.show()
    volume_name = volume_names[menu_entry_index]
    if not volume_name == "Exit":
        return volume_name
    else:
        exit()

def search_in_volume():
    volume = select_volume()
    default_pattern = "*.*"
    search_pattern = input(f"Enter the search pattern or press Enter to use the default pattern ({default_pattern}): ")
    if search_pattern == "":
        search_pattern = default_pattern
    search(volume, search_pattern)

def get_default_home_directory():
    try:
        if os.name == "nt":
            return os.path.expanduser("~user")
        else:
            return os.path.expanduser("~")
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def select_path():
    default_home_dir = get_default_home_directory()
    while True:
        selected_path = input(f"Enter the path or press Enter to use the default home directory ({default_home_dir}): ")
        if selected_path == "":
            selected_path = default_home_dir
        if os.path.exists(selected_path):
            return selected_path
        else:
            print("Invalid path. Please try again.")

def search_in_directory():
    search_path = select_path()
    default_pattern = "*.*"
    search_pattern = input(f"Enter the search pattern or press Enter to use the default pattern ({default_pattern}): ")
    if search_pattern == "":
        search_pattern = default_pattern
    search(search_path, search_pattern)

def display_spinner(stop_event):
    """Display a spinner animation until stop event is set."""
    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧"]
    spinner_index = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rSearching... {spinners[spinner_index]}")
        sys.stdout.flush()
        time.sleep(0.1)
        spinner_index = (spinner_index + 1) % len(spinners)

def search(location, search_pattern):
    """
    Search for files matching the search pattern in the given location and save results to a file.

    Args:
        location (str): The directory to search in.
        search_pattern (str): The pattern to search for.
    """
    print(f"Querying {location} for files matching {search_pattern}")
    results_file = get_results_file()
    search_terms = search_pattern.split()

    # Create a stop event for the spinner
    stop_event = threading.Event()

    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.start()

    # Search for the files
    try:
        with open(results_file, "w") as f:
            for root, _, files in os.walk(location):
                for file in files:
                    for term in search_terms:
                        if fnmatch.fnmatch(file, term):
                            result_path = os.path.join(root, file)
                            f.write(result_path + "\n")
    except PermissionError as e:
        print(f"Cannot access some files due to permission error: {e}")

    # Stop the spinner after the search is complete
    stop_event.set()
    spinner_thread.join()

    count = sum(1 for _ in open(results_file))
    sys.stdout.write(f"\rSearch completed. Found {count} files.{' ' * 20}\n")
    sys.stdout.flush()
    open_file(results_file)

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def copy_result(results_file):
    # Ask the user if they want to copy the results to another location
    if os.path.getsize(results_file) == 0:
        return

    copy_results = input("Do you want to copy the results to a folder? (Y/N): ").upper()
    if copy_results == "Y":
        copy_results_to_folder(results_file)
    elif copy_results == "N":
        pass
    else:
        print("Invalid input. Please enter Y or N.")

def copy_results_to_folder(results_file):
    # Copy the results to another location
    while True:
        copy_path = input("Enter the path to copy the results to: ")
        if os.path.isdir(copy_path):
            with open(results_file) as f:
                for line in f:
                    src_file = line.strip()
                    dest_file = os.path.join(copy_path, os.path.basename(src_file))
                    if os.path.exists(dest_file):
                        overwrite = input(f"File {os.path.basename(src_file)} already exists. Overwrite? (Y/N): ").upper()
                        if overwrite != "Y":
                            continue
                    try:
                        shutil.copy(src_file, copy_path)
                    except Exception as e:
                        print(f"Error copying file: {e}")
                    else:
                        print(f"File {os.path.basename(src_file)} copied to {copy_path}.")
            break
        else:
            print("Invalid path. Please provide a valid path like C:\\Users\\ or ~/Documents.")

def exit():
    print("Goodbye!")
    sys.exit(0)


if __name__ == "__main__":
    main()
