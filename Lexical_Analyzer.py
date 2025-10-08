import re
import os
from enum import Enum
from colorama import init, Fore, Back, Style
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

class TokenType(Enum):
    KEYWORD = "Keyword"
    IDENTIFIER = "Identifier"
    OPERATOR = "Operator"
    LITERAL = "Literal"
    PUNCTUATION = "Punctuation"
    SPECIAL_CHAR = "Special Character"
    CONSTANT = "Constant"
    ERROR = "Error"

# Color mapping for token types
TOKEN_COLORS = {
    TokenType.KEYWORD: Fore.GREEN,
    TokenType.IDENTIFIER: Fore.CYAN,
    TokenType.OPERATOR: Fore.MAGENTA,
    TokenType.LITERAL: Fore.YELLOW,
    TokenType.PUNCTUATION: Fore.BLUE,
    TokenType.SPECIAL_CHAR: Fore.WHITE,
    TokenType.CONSTANT: Fore.LIGHTYELLOW_EX,
    TokenType.ERROR: Fore.RED
}

def token_test_menu(analyzer):
    """Menu for testing specific token types"""
    while True:
        clear_screen()
        
        print_header("Token Type Testing")
        
        print(Fore.CYAN + "\nAvailable Token Types:")
        for i, token_type in enumerate(TokenType, 1):
            if token_type != TokenType.ERROR:
                color = TOKEN_COLORS.get(token_type, Fore.WHITE)
                print(f"{i}. {color}{token_type.value}")
        
        print(f"\n{len(TokenType)}. Return to main menu")
        
        try:
            choice = int(input(Fore.YELLOW + "\nSelect token type to test: " + Fore.WHITE))
            if choice == len(TokenType):
                break
            elif 1 <= choice < len(TokenType):
                selected_type = list(TokenType)[choice-1]
                test_token_type(analyzer, selected_type)
            else:
                print(Fore.RED + "Invalid choice!")
        except ValueError:
            print(Fore.RED + "Please enter a number!")
        
        input(Fore.YELLOW + "\nPress Enter to continue...")

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title, color=Fore.CYAN):
    """Print a simple header"""
    print(color + Style.BRIGHT + f"\n{'=' * 50}")
    print(f"{title.upper()}".center(50))
    print(f"{'=' * 50}\n")


def test_token_type(analyzer, token_type):
    """Test if input text matches specified token type"""
    clear_screen()
    print_header(f"Test {token_type.value}")
    
    color = TOKEN_COLORS.get(token_type, Fore.WHITE)
    print(f"\nEnter text to check if it's a {color}{token_type.value}{Style.RESET_ALL}:")
    text = input(Fore.WHITE + "> " + Style.RESET_ALL)
    
    if analyzer.is_token_of_type(text, token_type):
        print(Fore.GREEN + f"\n'{text}' IS a valid {token_type.value}!")
    else:
        print(Fore.RED + f"\n'{text}' is NOT a valid {token_type.value}!")
    
    # Show examples if the test failed
    if not analyzer.is_token_of_type(text, token_type):
        print(Fore.YELLOW + "\nExamples of valid {token_type.value}s:")
        if token_type == TokenType.KEYWORD:
            print(Fore.WHITE + ", ".join(list(analyzer.keywords)[:5]) + "...")
        elif token_type == TokenType.IDENTIFIER:
            print(Fore.WHITE + "myVar, _temp, x1, counter, user_input")
        elif token_type == TokenType.OPERATOR:
            print(Fore.WHITE + ", ".join(list(analyzer.operators)[:5]) + "...")
        elif token_type == TokenType.LITERAL:
            print(Fore.WHITE + '"Hello", 42, 3.14, a', "true")
        elif token_type == TokenType.PUNCTUATION:
            print(Fore.WHITE + ", ".join(analyzer.punctuations))
        elif token_type == TokenType.SPECIAL_CHAR:
            print(Fore.WHITE + ", ".join(analyzer.special_chars))
        elif token_type == TokenType.CONSTANT:
            print(Fore.WHITE + ", ".join(analyzer.constants))
            
class Token:
    def __init__(self, token_type, value, line_number):
        self.type = token_type
        self.value = value
        self.line_number = line_number
    
    def __str__(self):
        color = TOKEN_COLORS.get(self.type, Fore.WHITE)
        return f"{color}{self.type.value}: {self.value} (Line {Style.BRIGHT}{self.line_number}{Style.NORMAL})"
    
    def to_row(self):
        color = TOKEN_COLORS.get(self.type, Fore.WHITE)
        return [
            color + self.type.value,
            color + self.value,
            Style.BRIGHT + str(self.line_number)
        ]

class LexicalAnalyzer:
    def __init__(self):
        # Extended keyword list including common I/O functions
        self.keywords = {
            'int', 'float', 'double', 'char', 'void', 'bool', 'true', 'false',
            'if', 'else', 'while', 'for', 'do', 'switch', 'case', 'default',
            'break', 'continue', 'return', 'class', 'struct', 'new', 'delete',
            'public', 'private', 'protected', 'static', 'const', 'virtual',
            'try', 'catch', 'throw', 'namespace', 'using', 'include', 'define',
            'auto', 'enum', 'extern', 'goto', 'register', 'sizeof', 'typedef',
            'union', 'volatile', 'and', 'or', 'not', 'xor', 'bitand', 'bitor',
            'compl', 'and_eq', 'or_eq', 'not_eq', 'xor_eq', 'cout', 'cin',
            'printf', 'scanf', 'endl'
        }
        
        # Standard C/C++ operators
        self.operators = {
            '+', '-', '*', '/', '%', '=', '!', '&', '|', '^', '~', '<', '>',
            '==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '*=',
            '/=', '%=', '&=', '|=', '^=', '<<', '>>', '<<=', '>>=', '->', '::',
            '.*', '->*'
        }
        
        # Punctuation marks
        self.punctuations = {
            '{', '}', '[', ']', '(', ')', ',', ';', ':', '.', '?', '#'
        }
        
        # Special characters (not operators or punctuation)
        self.special_chars = {
            '@', '$', '`', '\\'
        }
        
        # Predefined constants
        self.constants = {
            'NULL', 'nullptr', 'EOF', 'TRUE', 'FALSE', 'MAX_PATH', 'PI'
        }
        
        self.tokens = []
        self.errors = []
        
        # Regular expression patterns (ordered by priority)
        self.patterns = [
            # Comments (to be ignored)
            (None, r'//.*|/\*.*?\*/'),
            
            # String literals (including escape sequences)
            (TokenType.LITERAL, r'"(?:\\.|[^"\\])*"'),
            
            # Character literals
            (TokenType.LITERAL, r"'(?:\\.|[^'\\])'"),
            
            # Numeric literals (integers, floats, scientific notation)
            (TokenType.LITERAL, r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fFuUlL]*'),
            
            # Constants (predefined)
            (TokenType.CONSTANT, r'\b(?:' + '|'.join(re.escape(c) for c in self.constants) + r')\b'),
            
            # Keywords
            (TokenType.KEYWORD, r'\b(?:' + '|'.join(re.escape(kw) for kw in self.keywords) + r')\b'),
            
            # Operators (longest first to ensure proper matching)
            (TokenType.OPERATOR, r'<<=|>>=|->\*|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||\+=|-=|\*=|/=|%=|&=|\|=|\^=|::|->|\+\+|\-\-|\+|\-|\*|/|%|=|!|&|\||\^|~|<|>|\?|:|\.[*]'),
            
            # Punctuations
            (TokenType.PUNCTUATION, r'[{}[\]();,:.#]'),
            
            # Special characters
            (TokenType.SPECIAL_CHAR, r'[@$`\\]'),
            
            # Identifiers (must start with letter/underscore, can contain numbers)
            (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*')
        ]
        
    def is_token_of_type(self, text, token_type):
        """Check if text matches a specific token type pattern"""
        if token_type == TokenType.KEYWORD:
            return text in self.keywords
        elif token_type == TokenType.IDENTIFIER:
            return bool(re.fullmatch(r'[a-zA-Z_]\w*', text))
        elif token_type == TokenType.OPERATOR:
            return text in self.operators
        elif token_type == TokenType.LITERAL:
            return (bool(re.fullmatch(r'".*"', text)) or  # String literal
                   bool(re.fullmatch(r"'.'", text)) or    # Char literal
                   bool(re.fullmatch(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fFuUlL]*', text)))  # Numeric
        elif token_type == TokenType.PUNCTUATION:
            return text in self.punctuations
        elif token_type == TokenType.SPECIAL_CHAR:
            return text in self.special_chars
        elif token_type == TokenType.CONSTANT:
            return text in self.constants
        return False
        
    def analyze(self, code):
        self.tokens = []
        self.errors = []
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            while line:
                matched = False
                
                # First check for patterns to ignore (like comments)
                ignore_pattern = r'//.*|/\*.*?\*/'
                ignore_match = re.match(ignore_pattern, line)
                if ignore_match:
                    line = line[len(ignore_match.group(0)):].lstrip()
                    continue
                
                for token_type, pattern in self.patterns:
                    if token_type is None:  # Skip ignore patterns
                        continue
                        
                    match = re.match(pattern, line)
                    if match:
                        value = match.group(0)
                        self.tokens.append(Token(token_type, value, line_num))
                        line = line[len(value):].lstrip()
                        matched = True
                        break
                
                if not matched:
                    if line[0].isspace():
                        line = line[1:]
                    else:
                        # Find the next whitespace or known symbol
                        next_space = len(line)
                        for symbol in self.operators.union(self.punctuations).union(self.special_chars):
                            idx = line.find(symbol)
                            if 0 < idx < next_space:
                                next_space = idx
                        
                        if next_space == len(line):
                            invalid_token = line
                            line = ""
                        else:
                            invalid_token = line[:next_space]
                            line = line[next_space:]
                        
                        if invalid_token:
                            self.errors.append(Token(TokenType.ERROR, invalid_token, line_num))
    
    def get_tokens_by_type(self, token_type):
        return [token for token in self.tokens if token.type == token_type]
    
    def get_token_counts(self):
        counts = {}
        for token_type in TokenType:
            if token_type != TokenType.ERROR:
                counts[token_type.value] = len(self.get_tokens_by_type(token_type))
        counts["Total"] = len(self.tokens)
        return counts
    
    def save_tokens_to_file(self, filename="Token.txt"):
        with open(filename, 'w') as f:
            # Write token counts first
            counts = self.get_token_counts()
            f.write("TOKEN COUNTS:\n")
            for token_type, count in counts.items():
                f.write(f"{token_type}: {count}\n")
            
            # Write all tokens
            f.write("\nALL TOKENS:\n")
            for token in self.tokens:
                f.write(f"{token.type.value}: {token.value} (Line {token.line_number})\n")
    
    def save_errors_to_file(self, filename="Error.txt"):
        with open(filename, 'w') as f:
            f.write(f"Total Errors: {len(self.errors)}\n\n")
            for error in self.errors:
                f.write(f"Error: {error.value} (Line {error.line_number})\n")
    
    def display_tokens_table(self, tokens=None):
        clear_screen()
        if tokens is None:
            tokens = self.tokens
        
        print_header("Token Analysis Results")
        
        if not tokens:
            print(Fore.YELLOW + "No tokens to display.")
            return
        
        # Display token counts
        counts = self.get_token_counts()
        print(Fore.CYAN + Style.BRIGHT + "\nTOKEN COUNTS:")
        for token_type, count in counts.items():
            if token_type == "Total":
                print(Fore.WHITE + f"{token_type}: {Fore.CYAN}{count}")
            else:
                color = next((v for k, v in TOKEN_COLORS.items() if k.value == token_type), Fore.WHITE)
                print(f"{color}{token_type}: {Fore.WHITE}{count}")
        
        # Display token details
        print(Fore.CYAN + Style.BRIGHT + "\nTOKEN DETAILS:")
        headers = [Fore.WHITE + Style.BRIGHT + "Type", 
                  Fore.WHITE + Style.BRIGHT + "Value", 
                  Fore.WHITE + Style.BRIGHT + "Line"]
        
        rows = [token.to_row() for token in tokens]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def display_errors_table(self):
        clear_screen()
        print_header("Error Analysis")
        
        if not self.errors:
            print(Fore.GREEN + "No errors found!")
            return
        
        print(Fore.RED + Style.BRIGHT + f"Total Errors: {len(self.errors)}\n")
        
        headers = [Fore.RED + Style.BRIGHT + "Error Type", 
                  Fore.RED + Style.BRIGHT + "Invalid Token", 
                  Fore.RED + Style.BRIGHT + "Line"]
        
        rows = [error.to_row() for error in self.errors]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
def display_menu():
    clear_screen()
    print_header("Lexical Analyzer Menu")
    
    menu_items = [
        "1. Load Source Code",
        "2. Analyze Code",
        "3. View Token Types",
        "4. Show Errors",
        "5. Export Files",
        "6. Test Token Type",  
        "7. Exit"
    ]
    
    for item in menu_items:
        print(Fore.WHITE + item)

def token_type_submenu(analyzer):
    while True:
        clear_screen()
        print_header("View Token Types")
        
        submenu_items = [
            "1. Keywords",
            "2. Identifiers",
            "3. Numbers",
            "4. Operators",
            "5. Punctuations",
            "6. All Tokens",
            "7. Return to main menu"
        ]
        
        for item in submenu_items:
            print(Fore.WHITE + item)
        
        choice = input(Fore.YELLOW + "\nEnter your choice: " + Fore.WHITE).strip()
        
        if choice == '1':
            tokens = analyzer.get_tokens_by_type(TokenType.KEYWORD)
            analyzer.display_tokens_table(tokens)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '2':
            tokens = analyzer.get_tokens_by_type(TokenType.IDENTIFIER)
            analyzer.display_tokens_table(tokens)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '3':
            tokens = analyzer.get_tokens_by_type(TokenType.LITERAL)
            analyzer.display_tokens_table(tokens)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '4':
            tokens = analyzer.get_tokens_by_type(TokenType.OPERATOR)
            analyzer.display_tokens_table(tokens)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '5':
            tokens = analyzer.get_tokens_by_type(TokenType.PUNCTUATION)
            analyzer.display_tokens_table(tokens)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '6':
            analyzer.display_tokens_table()
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '7':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
            input(Fore.YELLOW + "Press Enter to continue...")

def load_code_menu():
    clear_screen()
    print_header("Load Source Code")
    
    submenu_items = [
        "1. Enter code manually",
        "2. Load from file",
        "3. Return to main menu"
    ]
    
    for item in submenu_items:
        print(Fore.WHITE + item)
    
    choice = input(Fore.YELLOW + "\nEnter your choice: " + Fore.WHITE).strip()
    return choice

def main():
    analyzer = LexicalAnalyzer()
    source_code = ""
    
    while True:
        display_menu()
        choice = input(Fore.YELLOW + "\nEnter your choice: " + Fore.WHITE).strip()
    
        if choice == '1':
            load_choice = load_code_menu()
            
            if load_choice == '1':
                clear_screen()
                print_header("Enter Code")
                print(Fore.WHITE + "Enter your code (press Enter then Ctrl+D or Ctrl+Z on empty line to finish):\n")
                lines = []
                while True:
                    try:
                        line = input("    ")
                        lines.append(line)
                    except EOFError:
                        break
                source_code = '\n'.join(lines)
                clear_screen()
                print(Fore.GREEN + "Code loaded successfully!")
                input(Fore.YELLOW + "\nPress Enter to continue...")
            elif load_choice == '2':
                clear_screen()
                print_header("Load From File")
                filename = input(Fore.YELLOW + "\nEnter filename: " + Fore.WHITE).strip()
                try:
                    with open(filename, 'r') as f:
                        source_code = f.read()
                    clear_screen()
                    print(Fore.GREEN + f"Code loaded successfully from {filename}!")
                    input(Fore.YELLOW + "\nPress Enter to continue...")
                except FileNotFoundError:
                    clear_screen()
                    print(Fore.RED + f"File '{filename}' not found!")
                    input(Fore.YELLOW + "\nPress Enter to continue...")
            elif load_choice == '3':
                continue
            else:
                clear_screen()
                print(Fore.RED + "Invalid choice. Please try again.")
                input(Fore.YELLOW + "\nPress Enter to continue...")
        
        elif choice == '2':
            if not source_code:
                clear_screen()
                print(Fore.RED + "No source code loaded. Please load code first.")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                continue
            
            analyzer.analyze(source_code)
            clear_screen()
            print_header("Analysis Complete")
            print(Fore.GREEN + "Code analyzed successfully!")
            print(Fore.CYAN + f"\nTotal tokens found: {len(analyzer.tokens)}")
            print(Fore.YELLOW + f"Total errors found: {len(analyzer.errors)}")
            input(Fore.YELLOW + "\nPress Enter to continue...")
        
        elif choice == '3':
            if not analyzer.tokens and not analyzer.errors:
                clear_screen()
                print(Fore.YELLOW + "No analysis performed yet. Please analyze code first.")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                continue
            token_type_submenu(analyzer)
        
        elif choice == '4':
            if not analyzer.errors:
                clear_screen()
                print(Fore.GREEN + "No errors found!")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                continue
            
            analyzer.display_errors_table()
            input(Fore.YELLOW + "\nPress Enter to continue...")
        
        elif choice == '5':
            if not analyzer.tokens and not analyzer.errors:
                clear_screen()
                print(Fore.YELLOW + "No analysis performed yet. Please analyze code first.")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                continue
            
            analyzer.save_tokens_to_file()
            analyzer.save_errors_to_file()
            clear_screen()
            print_header("Files Exported")
            print(Fore.GREEN + "Token and error files exported successfully!")
            print(Fore.WHITE + f"\n- Token.txt (contains {len(analyzer.tokens)} tokens)")
            print(Fore.WHITE + f"- Error.txt (contains {len(analyzer.errors)} errors)")
            input(Fore.YELLOW + "\nPress Enter to continue...")
            
        elif choice == '6':  # New token testing functionality
            token_test_menu(analyzer)
        
        elif choice == '7':
            clear_screen()
            print_header("Thank You")
            print(Fore.WHITE + "Lexical Analyzer has been terminated.")
            break
        
        else:
            clear_screen()
            print(Fore.RED + "Invalid choice. Please try again.")
            input(Fore.YELLOW + "\nPress Enter to continue...")

if __name__ == "__main__":
    # Check for required packages
    try:
        from colorama import init, Fore, Back, Style
        from tabulate import tabulate
        main()
    except ImportError:
        print("Required packages not found. Please install:")
        print("pip install colorama tabulate")
        input("Press Enter to exit...")