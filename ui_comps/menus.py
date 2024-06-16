import os
import keyboard
from colorify import ConsoleStencil, TextStyle
import time
from typing import Callable
from prompts import Prompt

class MenuUtils:
    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')


class MenuDefaults:
    UNSELECTED = TextStyle(fg_color='black', bg_color='white', ansi='bold', style='bright')
    SELECTED = TextStyle(fg_color='white', bg_color='black', ansi='italic', style='dim')
    PROMPT = TextStyle(fg_color='white', bg_color='black', ansi='italic', style='bright')
    NAV = TextStyle(fg_color='white', bg_color='black', ansi='italic', style='dim')

    @staticmethod
    def create_default():
        return MenuStyle(MenuDefaults.PROMPT, MenuDefaults.NAV, 
        MenuDefaults.SELECTED, MenuDefaults.UNSELECTED)

    

class MenuStyle:
    def __init__(self, prompt_style: TextStyle = None, nav_style: TextStyle = None, slcted_style: TextStyle = None,
    unslcted_style: TextStyle = None) -> None:
        self.prompt: TextStyle = self.__validate(prompt_style, MenuDefaults.PROMPT)
        self.nav: TextStyle = self.__validate(nav_style, MenuDefaults.NAV)
        self.selected: TextStyle = self.__validate(slcted_style, MenuDefaults.SELECTED)
        self.unselected: TextStyle = self.__validate(unslcted_style, MenuDefaults.UNSELECTED)

    def __validate(self, style: TextStyle, default: TextStyle):
        """ Validate individual style with a fallback to default if validation fails """
        return style if style and style.validate() else default
    
    def option_stylize(self, is_selected: bool, option: str) -> TextStyle:
        if is_selected:
            return self.selected.apply(f'⟹ {option}')
        
        return self.unselected.apply(f'{option}')
    

class Option:
    def __init__(self, title: str, value, icon: str = '') -> None:
        self.title: str = title
        self.icon: str = icon
        self.value = value

    
class SimpleMenu:
    def __init__(self, options: list[str], prompt: str, menu_style: MenuStyle = None, should_divide: bool = True) -> None:
        self.style = menu_style if menu_style else MenuDefaults.create_default()
        self.options: list = options
        self.prompt: str = self.style.prompt.apply(prompt)
        self.__set_menu_options(should_divide)
        
    def __set_menu_options(self, should_divide: bool) -> None:
        self.highlight: int = 0
        self.running: bool = False
        self._should_divide: bool = should_divide
        self._divider: str = '*'
        self.option_formatter = lambda option: f'   [ {option} ]'

        
    
    def set_option_format(self, option_format: Callable[[str], str]) -> None:
        '''
            Sets the format of how each options are displayed in the menu.
            Pass a function that takes a string (option) and returns a string.
            
            More useful for ValueMenus that accept Option objects for
            the options list that have an attribute titled 'value'
            which can be set to an object with attributes you'd like to
            display with the option.
            
            -For Simple Menus the default format is (f'   [ {option} ]')
            
        '''
        self.option_formatter = option_format
        
    def set_divider(self, divider: str) -> None:
        if len(divider) == 1:
            self._divider = divider
    
    
    def render_routine(self, idx: int, item) -> None:
        print(self.style.option_stylize(idx == self.highlight, 
            self.option_formatter(item)
            )
        )

        if self._should_divide:
            Prompt.print_line(self._divider)

    
    def render(self) -> None:
        Prompt.clear()
        print(self.prompt)
        for idx, item in enumerate(self.options):
            self.render_routine(idx, item)
            
    
    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        if key.name == 'up' or key.name == 'w':
            self.highlight = (self.highlight - 1) % len(self.options)

        elif key.name == 'down' or key.name == 's':
            self.highlight = (self.highlight + 1) % len(self.options)

        elif key.name == 'enter':
            self.running = False
    
    def run(self) -> str:
        '''
            Simple Menu returns the string of 
            the selected option once the menu
            stops.
        '''
        self.ui_loop()
        return self.options[self.highlight]
    
    def ui_loop(self) -> None:
        self.running = True
        while self.running:
            self.render()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue    
            self.handle_keys(key)
            time.sleep(0.01)

class ValueMenu(SimpleMenu):
    def __init__(self, options: list[Option], prompt: str, menu_style: MenuStyle = None, should_divide: bool = True) -> None:
        super().__init__(options, prompt, menu_style)
        self.option_formatter = lambda option: f'   [ {option.title} ]'
    
       
    def get_choice(self):
        return self.options[self.highlight].value
    
    def choice_title(self):
        return self.options[self.highlight].title
    
    def __detr_option_style(self, is_selected: bool, option: str) -> str:
        return super().__detr_option_style(is_selected, self.option_formatter(option))

    def run(self) -> None:
        '''
            Only performs UI Loop for the menu
            to get the select choice call 'get_choice_value'
            after the menu has stopped.
        '''
        self.ui_loop()
    
    def add_option(self, option: Option) -> None:
        self.options.append(option)    
    

class SimplePagedMenu(SimpleMenu):
    def __init__(self, options: list[str], prompt: str, page_size: int = 5, menu_style: MenuStyle = None) -> None:
        super().__init__(options, prompt, menu_style)
        self.nav_txt = self.style.nav.apply("[ < i > Move ↑ / ↓  | Page ← / → | Select -> Enter  < i > ]")
        self.__setup_menu(page_size)

    def __setup_menu(self, page_size: int) -> None:
        self.page_size = page_size
        self.total_pages = (len(self.options) + page_size - 1) // page_size
        self._current_page = 1

    @property
    def current_page_options(self):
        start = (self._current_page - 1) * self.page_size
        end = start + self.page_size
        return self.options[start : end]

    def render(self) -> None:
        Prompt.clear()
        print(f'{self.prompt} - {self.nav_txt}')
        for idx, option in enumerate(self.current_page_options):
            self.render_routine(idx, option)

    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        super().handle_keys(key)
        if key.name == 'left':
            self._current_page = (self._current_page - 1) % self.total_pages or self.total_pages
            
        elif key.name == 'right':
            self._current_page = (self._current_page + 1) % self.total_pages or 1 
            

    def run(self):
        super().run()
        return self.current_page_options[self.highlight]

class PageUtils:
    @staticmethod
    def get_page_options(paged_menu):
        start = (paged_menu._current_page - 1) * paged_menu.page_size
        end = start + paged_menu.page_size
        return paged_menu.options[start:end]
    
    @staticmethod
    def handle_paging(paged_menu, key):
        if key.name == 'left':
            paged_menu._current_page -= 1 
            
        elif key.name == 'right':
            paged_menu._current_page += 1 
    
        
    
class SimplePagedMenu(SimpleMenu):
    def __init__(self, options: list[str], prompt: str, page_size: int = 5, menu_style: MenuStyle = None) -> None:
        super().__init__(options, prompt, menu_style)
        self.nav_txt = self.style.nav.apply("[ < i > Move ↑ / ↓  | Page ← / → | Select -> Enter  < i > ]")
        self.__setup_menu(page_size)

    def __setup_menu(self, page_size: int) -> None:
        self.page_size = page_size
        self.total_pages = (len(self.options) + page_size - 1 ) // page_size
        self._current_page = 1

    @property
    def current_page_options(self):
        return PageUtils.get_page_options(self)

    def render(self) -> None:
        Prompt.clear()
        print(f'{ self.prompt } - { self.nav_txt } | Page { self._current_page }/{ self.total_pages }')
        for idx, option in enumerate(self.current_page_options):
            self.render_routine(idx, option)

    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        super().handle_keys(key)
        if key.name == 'left' or key.name == 'a':
            self._current_page = (self._current_page - 1) % self.total_pages or self.total_pages
        elif key.name == 'right' or key.name == 'd':
            self._current_page = (self._current_page + 1) % self.total_pages or 1
        

    def run(self):
        super().run()
        return self.current_page_options[self.highlight]
    


class ValuePagedMenu(ValueMenu):
    def __init__(self, options: list[Option], prompt: str, page_size: int = 5, menu_style: MenuStyle = None) -> None:
        super().__init__(options, prompt, menu_style)
        self.nav_txt = self.style.nav.apply("[ < i > Move ↑ / ↓  | Page ← / → | Select -> Enter  < i > ]")
        self.__setup_menu(page_size)

    def __setup_menu(self, page_size: int) -> None:
        self.page_size = page_size
        self.total_pages = (len(self.options) + self.page_size - 1) // self.page_size
        self._current_page = 1
    
    @property
    def current_page(self) -> int:
        return self._current_page

    @current_page.setter
    def current_page(self, value: int) -> None:
        ''''
            Allows the current page to bounce on first and last 
        '''
        if value < 1:
            self._current_page = self.total_pages

        elif value > self.total_pages:
            self._current_page = 1

        else:
            self._current_page = value

        self.highlight = 0

    @property
    def current_page_options(self):
        return PageUtils.get_page_options(self)

    def render(self) -> None:
        Prompt.clear()
        print(f'{self.prompt} - {self.nav_txt} | Page {self._current_page}/{self.total_pages}')
        for idx, option in enumerate(self.current_page_options):
            self.render_routine(idx, option)

    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        super().handle_keys(key)
        if key.name == 'left' or key.name == 'a':
            self._current_page = (self._current_page - 1) % self.total_pages
        elif key.name == 'right' or key.name == 'd':
            self._current_page = (self._current_page + 1) % self.total_pages

    def run(self):
        super().run()
        return self.get_choice


class Animal:
    def __init__(self, name: str, sound: str) -> None:
        self.name = name
        self.sound = sound

    def speak(self) -> None:
        print(f'{self.name} says {self.sound}')



def simple_menu():
    options = [f'Option {i}' for i in range(10)]
    
    prompt_style = TextStyle(fg_color='yellow', bg_color='black', ansi='bold', style='bright')
    nav_style = TextStyle(fg_color='white', bg_color='black', ansi='italic', style='dim')
    selected_style = TextStyle(fg_color='white', bg_color='black', ansi='italic', style='bright')
    unselected_style = TextStyle(fg_color='black', bg_color='white', ansi='bold', style='bright')
    
    menu_style = MenuStyle(prompt_style, nav_style, selected_style, unselected_style)
    menu = SimpleMenu(options, 'Select an option', menu_style)
    choice = menu.run()
    print(f'You selected: {choice}')
    input()
    
    
    menu = SimpleMenu(options, 'Select an option')
    choice = menu.run()
    print(f'You selected: {choice}')
    
def value_menu():
    
    animals = [Animal('Dog', 'Woof'), Animal('Cat', 'Meow'), Animal('Cow', 'Moo')]
    option_formatter = lambda option: f'   [ {option.value.name} ({option.value.sound}) ]'
    options = [Option('animal', animal) for animal in animals]
    
    menu = ValueMenu(options, 'Select an animal')
    menu.set_option_format(option_formatter)
    menu.run()
    animal = menu.get_choice()
    animal.speak()
    
def simple_paged_menu():
    options = [f'Option {i}' for i in range(51)]
    menu = SimplePagedMenu(options, 'Select an option', 10)
    choice = menu.run()
    print(f'You selected: {choice}')   
    
def value_paged_menu():
    animals = [Animal('Dog', 'Woof'), Animal('Cat', 'Meow'), Animal('Cow', 'Moo')]
    options = [Option('animal', animal) for animal in animals]
    menu = ValuePagedMenu(options, 'Select an animal', 2)
    menu.run()
    animal = menu.get_choice
    animal.speak()

    



def demo_simple():
    options = [Option(f'Option {i}', i) for i in range(10)]
    menu = SimpleMenu(options, 'Select an option')
    choice = menu.run()
    print(f'You selected: { choice.title }')

def demo_all():
    simple_menu()
    input()
    value_menu()
    input()
    simple_paged_menu()
    input()
    value_paged_menu()




def main() -> None:
    demo_all()


if __name__ == "__main__":
    main()
