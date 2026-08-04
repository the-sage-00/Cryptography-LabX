"""
CryptoLabX - Menu Module
Provides the interactive command-line menu interface.
"""

import os


BANNER = r"""
  ____                  _        _          _   __  __
 / ___|_ __ _   _ _ __ | |_ ___ | |    __ _| |_|  \/  |
| |   | '__| | | | '_ \| __/ _ \| |   / _` | __| |\/| |
| |___| |  | |_| | |_) | || (_) | |__| (_| | |_| |  | |
 \____|_|   \__, | .__/ \__\___/|_____\__,_|\__|_|  |_|
            |___/|_|                           X v1.0
"""

MENU_OPTIONS = {
    "1": "Encrypt",
    "2": "Decrypt",
    "3": "Attack",
    "4": "Analyze",
    "5": "Exit",
}


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_banner():
    """Display the application banner."""
    print(BANNER)


def display_menu():
    """Display the main menu options."""
    print("=" * 50)
    print("         MAIN MENU")
    print("=" * 50)
    for key, value in MENU_OPTIONS.items():
        print(f"  [{key}] {value}")
    print("=" * 50)


def get_user_choice():
    """Prompt user for menu selection and return choice."""
    choice = input("\n  Enter your choice (1-5): ").strip()
    return choice


def handle_choice(choice):
    """
    Process the selected menu option.
    Returns False if the user chose to exit, True otherwise.
    """
    from utils.logger import log_action

    if choice not in MENU_OPTIONS:
        print("\n  Invalid choice. Please select a valid option (1-5).\n")
        return True

    log_action(MENU_OPTIONS[choice])

    if choice == "5":
        print("\n  Exiting CryptoLabX. Goodbye!\n")
        return False

    if choice == "4":
        from analysis.file_analyzer import run_file_analysis
        run_file_analysis()
        return True

    option_name = MENU_OPTIONS[choice]
    print(f"\n  [{option_name}] — Coming Soon!")
    print(f"  This feature will be available in a future update.\n")
    return True
