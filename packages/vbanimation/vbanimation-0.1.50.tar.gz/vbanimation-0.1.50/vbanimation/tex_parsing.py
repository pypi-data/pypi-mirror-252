from lark import Lark, Transformer, LarkError

latex_grammar = """
    start: "$" command "$"
    command: frac | sqrt | power | subscript | equality | addition | subtraction | multiplication | vector | unit_vector | scalar_vector | cross_product | dot_product | product | WORD | NUMBER
    frac: "\\dfrac{" command "}{" command "}"
    sqrt: "\\sqrt{" command "}"
    power: command "^" command
    subscript: command "_" command
    equality: command "=" command
    addition: command "+" command
    subtraction: command "-" command
    multiplication: command "*" command
    vector: "\\vec{" command "}"
    unit_vector: "\\hat{" command "}"
    scalar_vector: NUMBER vector
    cross_product: command "\\pimes" command
    dot_product: command "\\cdot" command
    product: WORD WORD+ | command command+
    
    NUMBER: /\d+/
    WORD: /[a-zA-Z]+/
    %ignore " "
"""
class LaTeXTransformer(Transformer):
    def frac(self, items):
        return f"{items[0]} upon {items[1]}"

    def sqrt(self, items):
        return f"square root of {items[0]}"

    def power(self, items):
        return f"{items[0]} to the power of {items[1]}"

    def subscript(self, items):
        return f"{items[0]} subscript {items[1]}"

    def equality(self, items):
        return f"{items[0]} equals to {items[1]}"

    def addition(self, items):
        return f"{items[0]} plus {items[1]}"

    def subtraction(self, items):
        return f"{items[0]} minus {items[1]}"

    def multiplication(self, items):
        return f"{items[0]} times {items[1]}"

    def vector(self, items):
        return f"vector {items[0]}"
    
    def unit_vector(self, items):
        return f"{items[0]} cap "
    
    def scalar_vector(self, items):
        return f"{items[0]} times {items[1]}"
    
    def cross_product(self, items):
        return f"{items[0]} cross {items[1]}"
    
    def dot_product(self, items):
        return f"{items[0]} dot {items[1]}"

    def product(self, items):
        return " times ".join(str(item) for item in items)

    def command(self, items):
        return str(items[0])

    def NUMBER(self, items):
        return str(items[0])

def parse_and_transform(latex_expression):
    try:
        # Create the parser and transformer
        latex_parser = Lark(latex_grammar, start='start', parser='lalr', lexer='standard')
        transformer = LaTeXTransformer()

        # Parse the LaTeX expression and print the parse tree
        parse_tree = latex_parser.parse(latex_expression)
        print(parse_tree.pretty())

        # Transform the parse tree into an English representation
        english_representation = transformer.transform(parse_tree)
        print(english_representation)

        return english_representation.children[0]
    except LarkError as e:
        print(f"An error occurred while parsing or transforming the LaTeX expression: {e}")
        return None