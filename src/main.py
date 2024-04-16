from simple_term_menu import TerminalMenu
import sys
import psutil
import time


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


def get_volumes():
    partitions = psutil.disk_partitions(all=True)
    volumes = [partition.mountpoint for partition in partitions]
    return volumes

def search_in_volume():
    volume_names = get_volumes()
    volume_names.append("Exit")
    volume_menu = TerminalMenu(volume_names, menu_cursor_style=("fg_green", "bold"))
    menu_entry_index = volume_menu.show()
    volume_name = volume_names[menu_entry_index]
    if not volume_name == "Exit":
        print(f"Searching in {volume_name}...")
        simulate_search(volume_name, "test.txt")
    else:
        exit()

def search_in_directory():
    pass

def simulate_search(location, search_pattern):
    # Simulate index files in the drive (5 seconds) and add a little spinner animation
    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧"]
    spinner_index = 0
    for _ in range(20):
        sys.stdout.write(f"\rIndexing files in {location} please wait... {spinners[spinner_index]}")
        sys.stdout.flush()
        time.sleep(0.1)
        spinner_index = (spinner_index + 1) % len(spinners)
    sys.stdout.write("\n")
    sys.stdout.flush()

    print(f"Searching in {location} for {search_pattern}")

def exit():
    # Terminate the program
    print("Goodbye!")
    sys.exit(0)


if __name__ == "__main__":
    main()
