import os
import sys
import keyboard

class MenuOption:
    def __init__(self, label, action):
        self.label = label
        self.action = action

    def execute(self):
        self.action()

# TODO
# Add Paging for larger strings of text.
# - Only included when the size of the header + text + bottom menu exceeds the terminal size.
# Refactor the Menu displayed at the bottom into a seperate object
# Optimize Current Design and storing of sizes into variables
# Refactor 'MenuOption' to include more of the work and add bindings directly from
# Text Editor Class for Sending and Recieving Emails
# Refactor using the Prompt Class 

class TextViewer:
    def __init__(self, text: str, header: str = None, options: list[str] = None) -> None:
        self.text: list[str] = text.split('\n')
        self.header: str = header or ""
        self.options: list[MenuOption] = [MenuOption(option, lambda: print(f"{option} selected")) for option in options] if options else []
        self.current_line: int = 0
        self.max_lines: int = os.get_terminal_size().lines - len(self.header.split('\n')) - 4  
        self.key_bindings: dict = {}
        self.selected_option: int = 0
        self.active: bool = False

    def bind_key(self, key, action) -> None:
        self.key_bindings[key] = action

    def run(self) -> None:
        self.active = True
        while self.active:
            self.display()
            self.handle_input()

    def display(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_header()
        self.show_text()
        self.show_menu()

    def show_header(self) -> None:
        header_lines = self.header.split('\n')
        print('\n'.join(header_lines))
        print('=' * os.get_terminal_size().columns)  

    def show_text(self) -> None:
        start_line = max(0, self.current_line - self.max_lines // 2)
        end_line = min(len(self.text), start_line + self.max_lines)
        for i, line in enumerate(self.text[start_line:end_line], start=start_line):
            if i == self.current_line:
                print(f"\033[1;32m{line}\033[0m")
            else:
                print(line)

    def show_menu(self):
        terminal_width = os.get_terminal_size().columns
        menu_width = sum(len(option.label) for option in self.options) + len(self.options) * 4  
        start_x = (terminal_width - menu_width) // 2
        print("\n" + "=" * terminal_width)  
        print(" " * start_x, end="")
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                print(f"[ \033[1;34m{option.label}\033[0m ]", end="  ")
            else:
                print(f"[ {option.label} ]", end="  ")  
        print()

    def handle_input(self):
        key = keyboard.read_key()
        if key == 'up':
            self.current_line = (self.current_line - 1) % len(self.text)
        elif key == 'down':
            self.current_line = (self.current_line + 1) % len(self.text)
        elif key == 'right':
            self.selected_option = (
                self.selected_option + 1) % len(self.options)
        elif key == 'left':
            self.selected_option = (
                self.selected_option - 1) % len(self.options)
        elif key == 'enter':
            if self.selected_option is not None:
                self.options[self.selected_option].execute()
                
        elif key in self.key_bindings:
            self.key_bindings[key]()
        elif key == 'q':
            self.exit()

    def add_option(self, label, action) -> None:
        self.options.append(MenuOption(label, action))

    def exit(self) -> None:
        self.active = False


def main():
    # Example usage
    long_text = """
    This is a longer string of text to test the TextViewer class. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed auctor, eros vel faucibus finibus, turpis ex fringilla mauris, vel hendrerit mauris sapien vitae mauris. Nullam pellentesque sit amet lacus vel efficitur. Mauris vel posuere nisl, eget tincidunt neque. Praesent tristique mollis magna, id placerat augue facilisis ut. Nulla pellentesque, leo eget mattis volutpat, est justo vehicula quam, vel finibus est quam et massa. Phasellus eu sem sit amet mi bibendum bibendum nec ac lacus. Cras luctus bibendum ultrices. Donec sollicitudin, nibh sed mattis fermentum, purus ex tristique turpis, in posuere lorem elit sed odio. Ut eu justo molestie, bibendum magna eget, dictum nunc.

    Sed a feugiat eros, sit amet dictum augue. Aenean a interdum orci. Nulla facilisi. Morbi in varius magna. Suspendisse et mauris bibendum, ultricies mauris id, iaculis mauris. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed eu tellus ac sem pellentesque hendrerit. Mauris accumsan turpis a augue ullamcorper, vitae eleifend dolor ullamcorper. Nulla vitae mauris dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel velit eu lorem posuere dictum a sit amet lectus. Donec nec neque iaculis, laoreet velit a, maximus dui. Cras aliquam condimentum hendrerit. Donec elementum enim vel risus tincidunt, at tincidunt nibh molestie.

    Mauris finibus lobortis hendrerit. Suspendisse potenti. Aliquam tempor dictum dolor ac gravida. In hac habitasse platea dictumst. Nunc eget leo sit amet orci maximus pulvinar. Etiam vitae urna vitae metus eleifend venenatis. Sed vel congue magna. Aliquam efficitur lorem sapien, quis iaculis nulla dictum ac. Fusce vel risus vitae leo sagittis cursus ac vel risus. Nunc tristique aliquam eros, ac dapibus velit egestas in. Aliquam eget convallis felis.

    Integer placerat magna in turpis molestie, eget interdum arcu rutrum. Donec interdum, magna eget pretium tincidunt, nunc velit finibus magna, nec tempus nisi nulla vel mi. Suspendisse potenti. Sed porta magna ut velit congue, vel luctus lacus efficitur. Praesent lacus ante, efficitur at blandit at, ullamcorper euismod risus. Aliquam erat volutpat. Nunc vitae porta mi. Maecenas in tempus ante, in feugiat mauris. Nullam vel sapien tortor. Etiam euismod, nisl non pulvinar congue, risus arcu pharetra ante, a condimentum sem odio eget nisi.

    Press 'q' to quit the text viewer.
    """

    header = "Example Header"
    options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

    viewer = TextViewer(long_text, header, options)

    def custom_action():
        print("Custom action executed!")

    viewer.add_option("Custom Option", custom_action)

    viewer.run()


if __name__ == "__main__":
    main()