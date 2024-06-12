from colorama import Fore, Back, Style, init
import re

init(autoreset=True)


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

    VALID_COLORS: set[str] = {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'}

    VALID_STYLES: set[str] = {'bright', 'dim', 'normal', 'reset_all'}

    VALID_ANSI_STYLES: set[str] = {'bold', 'underline', 'italic', 'normal'}

    COLOR_MAP: dict[str, str] = {color: getattr(Fore, color.upper()) for color in VALID_COLORS}

    BACKGROUND_MAP: dict[str, str] = {color: getattr(Back, color.upper()) for color in VALID_COLORS}

    STYLE_MAP: dict[str, str] = {style: getattr(Style, style.upper()) for style in VALID_STYLES}

    ANSI_STYLE_MAP: dict[str, str] = {
        'bold': '\033[1m',
        'underline': '\033[4m',
        'italic': '\033[3m',
        'normal': '\033[0m'
    }

    @staticmethod
    def ansify(text: str, ansi: str) -> str:
        """
            Apply an ANSI style to the text. 
            
            Accepts 'bold', 'underline', 'italic', 'normal' as valid styles.

            Args:
                text (str): _description_
                ansi (str): _description_

            Returns:
                str: _description_
        """
        ansi = ansi.lower()
        if not ansi in ConsoleStencil.VALID_ANSI_STYLES:
            return text
        return f"{ConsoleStencil.ANSI_STYLE_MAP[ansi]} {text} {ConsoleStencil.ANSI_STYLE_MAP['normal']}"

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
        if not color in ConsoleStencil.VALID_COLORS:
            return text
        return f"{ConsoleStencil.COLOR_MAP[color]} {text} {Style.RESET_ALL}"

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
        if not color in ConsoleStencil.VALID_COLORS:
            return text
        return f"{ConsoleStencil.BACKGROUND_MAP[color]} {text} {Style.RESET_ALL}"

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
        if not style in ConsoleStencil.VALID_STYLES:
            return text

        return f"{ConsoleStencil.STYLE_MAP[style]}{text}{Style.RESET_ALL}"

    @staticmethod
    def rainbow(text: str) -> str:
        """
            Apply a different color to each character in the text, 
            cycling through available colors.

            Args:
                text (str): The text to colorize.

            Returns:
                str: The rainbow-colored text.
        """
        colors = list(ConsoleStencil.VALID_COLORS)
        colored_chars = [ConsoleStencil.colorize(
            char, colors[i % len(colors)]) for i, char in enumerate(text)]
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
            if key == 'fg_color' and value in ConsoleStencil.VALID_COLORS:
                styled_text = f"{ConsoleStencil.COLOR_MAP[value]} {styled_text}"

            elif key == 'bg_color' and value in ConsoleStencil.VALID_COLORS:
                styled_text = f"{ConsoleStencil.BACKGROUND_MAP[value]} {styled_text}"

            elif key == 'ansi' and value in ConsoleStencil.VALID_ANSI_STYLES:
                styled_text = f"{ConsoleStencil.ANSI_STYLE_MAP[value]} { styled_text} {ConsoleStencil.ANSI_STYLE_MAP['normal']}"

            elif key == 'style' and value in ConsoleStencil.VALID_STYLES:
                styled_text = f"{ConsoleStencil.STYLE_MAP[value]} {styled_text}"

            else:
                ConsoleStencil._log_error(f"Invalid {key}: '{value}'. This style will be ignored.")

        return f'{styled_text} {Style.RESET_ALL}'

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
        ansi_style = ConsoleStencil.ANSI_STYLE_MAP[ansi]
        return text.replace(phrase,
                f"{ansi_style}{phrase}{ConsoleStencil.ANSI_STYLE_MAP['normal']}"
                )

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
        if not phrase in text or not color in ConsoleStencil.VALID_COLORS:
            return text

        color = color.lower()
        color_map = ConsoleStencil.BACKGROUND_MAP if is_background else ConsoleStencil.COLOR_MAP
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

        if color not in ConsoleStencil.VALID_COLORS:
            return text

        return regex.sub(lambda match: 
            f"{ConsoleStencil.COLOR_MAP[color]}{match.group()}{Style.RESET_ALL}",text
        )


def regex_test() -> None:
    text = "There are 3 apples and 7 oranges in the basket. The price of 2 apples is $5."
    pattern = re.compile(r'\d+')  # Matches all word characters
    colored_text = ConsoleStencil.color_regex_matches(text, pattern, 'green')
    print(colored_text)


def main() -> None:
    regex_test()


if __name__ == '__main__':
    main()




