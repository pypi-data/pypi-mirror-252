from re import findall
import subprocess
from manim import *
from sympy import *
from sympy.parsing.latex import parse_latex
from num2words import num2words





def expr_to_text(expr):
    if isinstance(expr, Add):
        return ' plus '.join(map(expr_to_text, expr.args))
    elif isinstance(expr, Mul):
        return ' times '.join(map(expr_to_text, expr.args))
    elif isinstance(expr, Pow):
        return expr_to_text(expr.base) + ' to the power of ' + expr_to_text(expr.exp)
    elif isinstance(expr, Symbol):
        return str(expr)
    elif isinstance(expr, Number):
        return num2words(expr)
    else:
        return str(expr)


def process_tex_to_text(tex_string):
    math_expressions = findall(r'\$(.*?)\$', tex_string)
    for i in math_expressions:
        eng_expr = expr_to_text(parse_latex(i))
        tex_string = tex_string.replace(f'${i}$', eng_expr)
        
    tex_string_expr = tex_string.replace(r'\intertext{', r'')
    return expr_to_text(parse_latex(tex_string_expr))
    
    
def get_audio(text, key):
    audio_command = f'say -o {key}.aac {text}'
    subprocess.call(audio_command, shell=True) 
    print(text)
    
       



        
        

    
    
        

            


       

        



    