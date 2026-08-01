"""
CryptoLabX - Cryptography Laboratory Toolkit
Course: Cryptography Laboratory (22CPP307)

Entry point for the command-line interface.
Run: python main.py
"""

from utils.menu import (
    clear_screen,
    display_banner,
    display_menu,
    get_user_choice,
    handle_choice,
)


def main():
    """Main application loop."""
    clear_screen()
    display_banner()

    running = True
    while running:
        display_menu()
        choice = get_user_choice()
        running = handle_choice(choice)

        if running:
            input("  Press Enter to continue...")
            clear_screen()
            display_banner()


if __name__ == "__main__":
    main()
