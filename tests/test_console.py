from colorama import Fore
from colorama import Style
from pipfreezer import print_message
from pipfreezer import print_not_installed_packages
from pipfreezer import print_updated_packages


def test_print_message(capfd):
    print_message(Fore.GREEN, "Test message")
    captured = capfd.readouterr()
    assert captured.out == f"{Fore.GREEN}Test message{Fore.RESET}\n"


def test_print_updated_packages(capfd):
    print_updated_packages(["requests==2.25.1", "flask==1.1.2"])
    captured = capfd.readouterr()
    expected_output = (
        f"{Fore.GREEN}The following packages have updated pinned versions:{Fore.RESET}\n"
        f"{Style.DIM}requests==2.25.1\nflask==1.1.2{Fore.RESET}\n"
    )
    assert captured.out == expected_output


def test_print_not_installed_packages(capfd):
    print_not_installed_packages(["requests==2.25.1", "flask==1.1.2"])
    captured = capfd.readouterr()
    expected_output = (
        f"{Fore.YELLOW}\nThe following packages are referenced in requirements, but are not installed:{Fore.RESET}\n"
        f"{Style.DIM}requests==2.25.1\nflask==1.1.2{Fore.RESET}\n"
    )
    assert captured.out == expected_output
