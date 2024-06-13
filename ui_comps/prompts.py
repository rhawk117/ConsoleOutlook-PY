from colorify import ConsoleStencil
import time 
import os 


# unicode symbols
'''
🛈
✓
?
︖

'''

class PromptUtils:
    
    @staticmethod
    def center_msg(msg: str) -> None:
        print(PromptUtils.center_str(msg))

    @staticmethod
    def center_str(msg: str) -> None:
        cols = os.get_terminal_size().columns
        return msg.center(cols, " ")
    
    @staticmethod
    def detr_center(flag: bool, msg: str) -> str:
        if flag:
            return PromptUtils.center_str(msg)
        return msg
    
    @staticmethod
    def divider(sep: str) -> None:
        cols = os.get_terminal_size().columns
        return sep * cols
    
class Prompt:
    GEN_SPACER: dict[str, str] = { 'ansi' : 'bold', 'style' : 'bright' }
    GEN_PROMPT: dict[str, str] = { 'ansi' : 'italic', 'style' : 'bright' }
    
    @staticmethod
    def info(msg: str, should_center: bool = True) -> None:
        spacer = ConsoleStencil.multi_style('[ i ]', **Prompt.GEN_SPACER)
        msg = ConsoleStencil.multi_style(msg, **Prompt.GEN_PROMPT)
        print(PromptUtils.detr_center(should_center, f'\n{spacer} {msg} {spacer}\n'))
    
    @staticmethod
    def success(msg: str, should_center: bool = True) -> None:
        spacer = ConsoleStencil.multi_style('[ ✓ ]', fg_color='green', ansi='bold', style='bright')
        msg = ConsoleStencil.multi_style(msg, **Prompt.GEN_PROMPT)
        print(PromptUtils.detr_center(should_center, f'\n{spacer} {msg} {spacer}\n'))
    
    @staticmethod
    def wait():
        spacer = ConsoleStencil.multi_style('[ * ]', **Prompt.GEN_SPACER)
        styled_msg = ConsoleStencil.multi_style('Press < ENTER > to Continue...', **Prompt.GEN_PROMPT)
        centered_msg = PromptUtils.center_str(f'\n{spacer} { styled_msg } {spacer}\n')
        input(ConsoleStencil.color_phrase(centered_msg, phrase='< ENTER >', 
            color='green')
        )

    @staticmethod
    def error(msg: str, should_center: bool = True) -> None:
        spacer = ConsoleStencil.multi_style('[ ! ]', fg_color='red', ansi='bold', style='bright')
        msg = ConsoleStencil.multi_style(msg, **Prompt.GEN_PROMPT)
        print(PromptUtils.detr_center(should_center, f'\n{ spacer } ERROR: { msg } { spacer }\n'))
    
    @staticmethod
    def ask(prompt: str, should_center: bool = True):
        spacer = ConsoleStencil.multi_style('[ ? ]', fg_color='yellow', ansi='bold', style='bright')
        msg = ConsoleStencil.multi_style(prompt, **Prompt.GEN_PROMPT)
        print(PromptUtils.detr_center(should_center, f'\n{ spacer } { msg } { spacer }\n'))
    
    @staticmethod
    def promptify(prompt: str) -> str:
        spacer = ConsoleStencil.multi_style('[ ? ]', ansi='bold', style='bright')
        return f'{spacer} {prompt} {spacer}'
        
    @staticmethod 
    def print_line(sep: str = '*') -> None:
        print(PromptUtils.divider(sep))
    
    @staticmethod
    def divider(sep: str) -> None:
        cols = os.get_terminal_size().columns
        return sep * cols
    
    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    

def prompt_demo():
    Prompt.info('This is an info message')
    Prompt.success('This is a success message')
    Prompt.error('This is an error message')
    Prompt.print_line()
    Prompt.ask('What is your name')
    Prompt.print_line()
    
def test():
    Prompt.print_line('')

def main() -> None:
    test()
        
if __name__ == "__main__":
    main()