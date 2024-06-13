from colorama import Fore, Back, Style, init
import re

init(autoreset=True)


class StencilData:
    """
        A class to store the static settings for ConsoleStencil.
    """
    VALID_COLORS: set[str] = {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'}

    VALID_STYLES: set[str] = {'bright', 'dim', 'normal', 'reset_all'}

    VALID_ANSI_STYLES: set[str] = {'bold', 'underline', 'italic', 'normal'}

    COLOR_MAP: dict[str] = {color: getattr(Fore, color.upper()) for color in VALID_COLORS}
    
    BACKGROUND_MAP: dict[str] = {color: getattr(Back, color.upper()) for color in VALID_COLORS}
    
    STYLE_MAP: dict[str] = {style: getattr(Style, style.upper()) for style in VALID_STYLES}
    
    ANSI_STYLE_MAP = {
        'bold': '\033[1m',
        'underline': '\033[4m',
        'italic': '\033[3m',
        'normal': '\033[0m'
    }
    
    SETTINGS = {
        'VALID_COLORS': VALID_COLORS,
        'VALID_STYLES': VALID_STYLES,
        'VALID_ANSI_STYLES': VALID_ANSI_STYLES,
        'COLOR_MAP': COLOR_MAP,
        'BACKGROUND_MAP': BACKGROUND_MAP,
        'STYLE_MAP': STYLE_MAP,
        'ANSI_STYLE_MAP': ANSI_STYLE_MAP
    }

class TextStyle:
    def __init__(self, fg_color: str = None, bg_color: str = None, ansi: str = None, style: str = None) -> None:
        '''
            A class to store the settings for a multi text style if you prefer to use an object.
            
            All values supplied must be valid or the object will not be valid and won't work 
            with the multi_style method.
            
            o	ansi (str, optional): The text style such as 'bold', 'underline', etc. 
                [Accepts 'bold', 'underline', 'italic', 'normal']
                
            o	fg_color (str, optional): The foreground color. 
                [Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',  'white', 'black' as valid colors]

            o	bg_color (str, optional): The background color 
                [Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',  'white', 'black' as valid colors]

            o	style (str, optional): A Colorama style 
                [Accepts 'bright', 'dim', 'normal', 'reset_all']
        '''
        self.fg_color: str = fg_color
        self.bg_color: str = bg_color
        self.ansi: str = ansi
        self.style: str = style
    
    def unpack(self) -> dict[str, str]:
        return {k: v for k, v in vars(self).items() if v is not None}
    
    def validate(self) -> bool:
        if self.fg_color is not None and self.fg_color.lower() not in StencilData.VALID_COLORS:
            return False

        if self.bg_color is not None and self.bg_color.lower() not in StencilData.VALID_COLORS:
            return False

        if self.ansi is not None and self.ansi.lower() not in StencilData.VALID_ANSI_STYLES:
            return False

        if self.style is not None and self.style.lower() not in StencilData.VALID_STYLES:
            return False
        
        return True
    
    def apply(self, text: str) -> str:
        if not self.validate():
            return text
        return ConsoleStencil.custom_style(text, self)

    
        

class ConsoleStencil:
    '''
        A collection of static methods for applying color and style to text in the console.
        The ConsoleStencil class is meant to simplify the process of stylzing text in the 
        Console with a simple method call. This acheieved using the Colorama library and 
        Ansi escape codes.
        
        VALID_COLORS: set[str]: A set of valid colors that can be applied to text.
        
        VALID_STYLES: set[str]: A set of valid styles that can be applied to text.
        
        VALID_ANSI_STYLES: set[str]: A set of valid ANSI styles that can be applied to text.
        
        COLOR_MAP: dict[str, str]: A dictionary mapping color names to their respective Colorama
        Attribute names.
        
        BACKGROUND_MAP: dict[str, str]: A dictionary mapping color names to their respective Colorama
        Background Attribute names.
        
        STYLE_MAP: dict[str, str]: A dictionary mapping style names to their respective Colorama
        Style Attribute names.
        
        ANSI_STYLE_MAP: dict[str, str]: A dictionary mapping ANSI style names to their respective
        ANSI escape codes.
    '''

    @staticmethod
    def ansify(text: str, ansi: str) -> str:
        """
            Apply an ANSI style to the text. 
            
            Accepts 'bold', 'underline', 'italic', 'normal' as valid styles.

            Args:
                text (str): text to apply ansi style to
                ansi (str): type of style to apply

            Returns:
                str: ansified string
        """
        ansi = ansi.lower()
        if not ansi in StencilData.VALID_ANSI_STYLES:
            return text
        return f"{StencilData.ANSI_STYLE_MAP[ansi]} {text} {StencilData.ANSI_STYLE_MAP['normal']}"

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """
            Applies a foreground color to the text of string
            passed.

            If the color is not valid, the text is returned as is.
            
            Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 
            'white', 'black' as valid colors.

            Args:
                text (str): text to colorize
                color (str): color to apply

        """
        color = color.lower()
        if not color in StencilData.VALID_COLORS:
            return text
        return f"{StencilData.COLOR_MAP[color]} {text} {Style.RESET_ALL}"

    def bg_colorize(text: str, color: str) -> str:
        """
        Applies color to the background of the text

        Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',
        'white', 'black' as valid colors.

        If the color is not valid, the text is returned as is.
        
        Args:
            text (str): text to colorize
            color (str): color to apply
        """
        color = color.lower()
        if not color in StencilData.VALID_COLORS:
            return text
        return f"{StencilData.BACKGROUND_MAP[color]} {text} {Style.RESET_ALL}"

    @staticmethod
    def font_variant(text: str, style: str) -> str:
        """
        Apply a colorama style to the entire text.
        
        If the variant is not valid, the text is returned as is.
        
        Args:
            text (str): The text to style.
            style (str): The style to apply ('bright', 'dim', 'normal', 'reset_all').
        
        Returns:
            str: The styled text.
        """
        style = style.lower()
        if not style in StencilData.VALID_STYLES:
            return text

        return f"{StencilData.STYLE_MAP[style]}{text}{Style.RESET_ALL}"

    @staticmethod
    def rainbow(text: str) -> str:
        """
            Apply a different color to each character in the text, cycling through available colors.

            Args:
                text (str): The text to colorize.

            Returns:
                str: The rainbow-colored text.
        """
        colors = list(StencilData.VALID_COLORS)
        colored_chars = [ConsoleStencil.colorize(char, colors[i % len(colors)]) for i, char in enumerate(text)]
        return ''.join(colored_chars)

    @staticmethod
    def multi_style(text: str, **kwargs) -> str:
        """
            Apply styles to text using keyword arguments for maximum flexibility.

            Keyword Args:
                text (str): The text to style.

                ansi (str, optional): The text style such as 'bold', 'underline', etc.

                fg_color (str, optional): The foreground color.

                bg_color (str, optional): The background color.

                style (str, optional): The colorama style such as 'bright', 'dim', etc.

            Returns:
                str: The stylized text.
        """
        styled_text = text
        for key, value in kwargs.items():
            value = value.lower()
            if key == 'fg_color' and value in StencilData.VALID_COLORS:
                styled_text = f"{StencilData.COLOR_MAP[value]} {styled_text}"

            elif key == 'bg_color' and value in StencilData.VALID_COLORS:
                styled_text = f"{StencilData.BACKGROUND_MAP[value]} {styled_text}"

            elif key == 'ansi' and value in StencilData.VALID_ANSI_STYLES:
                styled_text = f"{StencilData.ANSI_STYLE_MAP[value]} {styled_text} {StencilData.ANSI_STYLE_MAP['normal']}"

            elif key == 'style' and value in StencilData.VALID_STYLES:
                styled_text = f"{StencilData.STYLE_MAP[value]} {styled_text}"


        return f'{styled_text} {Style.RESET_ALL}'
    
    @staticmethod
    def custom_style(text: str, style: TextStyle) -> str:
        """
            Applies a custom style to the text passed using a 
            Text Style object instead of kwargs.

            -If any styles are not valid the text is returned as is.
            
            Args:
                text (str): The text to style.
                style (TextStyle): The TextStyle object containing the style settings.

            Returns:
                str: The text with the style applied.
        """
        if not style.validate():
            return text

        return ConsoleStencil.multi_style(text, **style.unpack())

    @staticmethod
    def highlight_phrase(text: str, phrase: str, ansi: str) -> str:
        """
            Highlight all occurrences of 'phrase' in 'text' with the specified ANSI style.

            -If the phrase is not found in the text, the text is returned as is.
            
            -If the style is not valid, the text is returned as is.
            
            Args:
                text (str): The full text in which to highlight the phrase.
                phrase (str): The phrase within the text to highlight.
                style (str): The ANSI style to apply ('bold', 'underline', 'italic').

            Returns:
                str: The text with the phrase highlighted.
        """
        if not phrase in text or not ansi in ConsoleStencil.VALID_ANSI_STYLES:
            return text

        ansi = ansi.lower()
        ansi_style = StencilData.ANSI_STYLE_MAP[ansi]
        return text.replace(phrase, 
                f"{ansi_style}{phrase}{StencilData.ANSI_STYLE_MAP['normal']}")

    @staticmethod
    def bold(text: str) -> str:
        """
            Returns a bolded version of a string passed.

            Args:
                text (str): The text to bold.
        """
        return ConsoleStencil.ansify(text, style='bold')

    @staticmethod
    def underline(text: str) -> str:
        """
            Returns an underlined version of string passed.

            Args:
                text (str): The text to underline.
        """
        return ConsoleStencil.ansify(text, ansi='underline')

    @staticmethod
    def italicize(text: str) -> str:
        """
            Returns an italicized version of the string passed.

            Args:
                text (str): The text to italicize.
        """
        return ConsoleStencil.ansify(text, ansi='italic')

    @staticmethod
    def color_phrase(text: str, phrase: str, color: str, is_background: bool = False) -> str:
        """
            Colors either the foreground or background of a specific phrase within the string. 
            Is Case Sensitive.
            
            Args:
                text (str): The full text that features the phrase.
                phrase (str): The phrase within the text to colorize.
                color (str): The color to apply to the phrase.
                is_background (bool): If True, the color is applied to the background.
            
            Returns:
                str: The text with the phrase colorized.
        """
        if not phrase in text or not color in StencilData.VALID_COLORS:
            return text

        color = color.lower()
        color_map = StencilData.BACKGROUND_MAP if is_background else StencilData.COLOR_MAP
        color_code = color_map[color]
        return text.replace(phrase, f'{color_code}{phrase}{Style.RESET_ALL}')

    @staticmethod
    def brighten(text: str) -> str:
        """
            Brighten the text passed.

            Args:
                text (str): The text to brighten.
        """
        return ConsoleStencil.font_variant(text, 'bright')

    @staticmethod
    def dim(text: str) -> str:
        """
            Dims the text passed.

            Args:
                text (str): The text to dim.
        """
        return ConsoleStencil.font_variant(text, 'dim')

    @staticmethod
    def color_regex_matches(text: str, regex: re.Pattern, color: str) -> str:
        """
        Colors all occurrences of the given regex pattern in the text.

        Args:
            text (str): The text in which to color the regex matches.
            regex (re.Pattern): The pre-compiled regex pattern.
            color (str): The color to apply to the matches.

        Returns:
            str: The text with the regex matches colored.
        """
        if not isinstance(regex, re.Pattern) or not re.search(regex, text):
            return text

        color = color.lower()

        if color not in StencilData.VALID_COLORS:
            return text

        return regex.sub(lambda match:
            f"{StencilData.COLOR_MAP[color]}{match.group()}{Style.RESET_ALL}", text
        )


def test_color_phrase():
    print(ConsoleStencil.color_phrase(
        'The word blood is red here because red is blood', 'gay', 'red'))
    print(ConsoleStencil.color_phrase(
        'The word cum is white here because cum is white', 'cum', 'white', is_background=True))


def ansi_methods():
    print(ConsoleStencil.ansify('Hello, World! (bold)', 'bold'))
    print(ConsoleStencil.ansify('Hello, World! (underline)', 'underline'))
    print(ConsoleStencil.ansify('Hello, World! (italic)', 'italic'))
    print(ConsoleStencil.ansify('Hello, World! (normal)', 'normal'))


def color_methods():
    print(ConsoleStencil.colorize('Hello, World! (red)', 'red'))
    print(ConsoleStencil.colorize('Hello, World! (green)', 'green'))
    print(ConsoleStencil.colorize('Hello, World! (blue)', 'blue'))
    print(ConsoleStencil.colorize('Hello, World! (yellow)', 'yellow'))
    print(ConsoleStencil.colorize('Hello, World! (magenta)', 'magenta'))
    print(ConsoleStencil.colorize('Hello, World! (cyan)', 'cyan'),)
    print(ConsoleStencil.colorize('Hello, World! (white)', 'white'))
    print(ConsoleStencil.colorize('Hello, World! (black)', 'black'))
    print(ConsoleStencil.rainbow('Hello, World! (rainbow)'))
    print(ConsoleStencil.bg_colorize('Hello, World! (red bg)', 'red'))


def font_vars():
    print(ConsoleStencil.font_variant('Hello, World! (bright)', 'bright'))
    print(ConsoleStencil.font_variant('Hello, World! (dim)', 'dim'))


def multi_style():
    print(ConsoleStencil.multi_style(
        "Hello, World! (info: fg_color='red', bg_color='blue', ans='bold)', fg_color='red'", bg_color='blue', ansi='bold'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='green', bg_color='yellow', ansi='unerline)'",
          fg_color='green', bg_color='yellow', ansi='underline'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='magenta', bg_color='cyan', ansi=italic)'",
          fg_color='magenta', bg_color='cyan', ansi='italic'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='white', bg_color='black', style=bright)'",
          fg_color='white', bg_color='black', style='bright'))


def run_test(test_name, method_calls):
    print('Running Test for ' + test_name)
    method_calls()
    input('Press Enter to Continue')

def run_all():
    run_test('Color Phrase', test_color_phrase)
    run_test('ANSI Methods', ansi_methods)
    run_test('Color Methods', color_methods)
    run_test('Font Variants', font_vars)
    run_test('Multi Style', multi_style)
    




def regex_test() -> None:
    text = "There are 3 apples and 7 oranges in the basket. The price of 2 apples is $5."
    pattern = re.compile(r'\d+')  # Matches all word characters
    colored_text = ConsoleStencil.color_regex_matches(text, pattern, 'green')
    print(colored_text)

def text_style() -> None:
    style = TextStyle(ansi='bold', fg_color='red') 
    print(style.apply('Hello, World!'))



def main() -> None:
    text_style()
    # regex_test()


if __name__ == '__main__':
    main()




