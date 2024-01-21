from re import findall
import subprocess
from manim import *
from sympy import *
from sympy.parsing.latex import parse_latex
from num2words import num2words
from .other_functions import get_audio_duration




def expr_to_text(expr):
    if isinstance(expr, Add):
        return ' plus '.join(map(expr_to_text, expr.args))
    elif isinstance(expr, Mul):
        return ' times '.join(map(expr_to_text, expr.args))
    elif isinstance(expr, Equality):
        return expr_to_text(expr.lhs) + ' equals ' + expr_to_text(expr.rhs)
    elif isinstance(expr, Pow):
        exp = expr.exp
        if exp == 0.5:
            return ' square root of ' + expr_to_text(expr.base)
        return expr_to_text(expr.base) + ' to the power of ' + expr_to_text(expr.exp)
    elif isinstance(expr, Symbol):
        return str(expr)
    elif isinstance(expr, Number):
        return num2words(expr)
    else:
        return str(expr)


def process_tex_to_text(tex_string):
    tex_string = tex_string.replace(r'\intertext{', r'')
    tex_string = tex_string.replace(r'\\[2mm]', r'')
    tex_string = tex_string.replace(r'&', r'')
    math_expressions = findall(r'\$(.*?)\$', tex_string)
    print(math_expressions)
    for i in math_expressions:
        if i.startswith('='):
            parts = i.split('=')
            parts = [part for part in parts if part]  # remove empty strings
            eng_expr = ' equals to '.join(expr_to_text(parse_latex(part)) for part in parts)
        else:
            eng_expr = expr_to_text(parse_latex(i))
            
        tex_string = tex_string.replace(f'${i}$', eng_expr)
        
    return expr_to_text(tex_string)
    
    
def get_audio(text, key):
    audio_command = f'say -o {key}.aac {text}'
    duration = get_audio_duration(f'{key}.aac')
    subprocess.call(audio_command, shell=True) 
    return duration
    print(text)
    
       



        
        

    
    
        

            


       

        



    