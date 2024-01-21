import re
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


def process_tex_to_text(tex_file):
    math_expressions = re.findall(r'\$(.*?)\$', tex_file, re.DOTALL)
    for i in math_expressions:
        eng_expr = expr_to_text(parse_latex(i))
        tex_file = tex_file.replace(f'${i}$', eng_expr)
        
    tex_file_expr = tex_file.replace(r'\intertext{', r'')
    return expr_to_text(parse_latex(tex_file_expr))
    
    
def get_audio(text, key):
    audio_command = f'say -o {key}.aac {text}'
    subprocess.call(audio_command, shell=True) 
    print(text)
    
       



        
        

    
    
        

            


       

        



    