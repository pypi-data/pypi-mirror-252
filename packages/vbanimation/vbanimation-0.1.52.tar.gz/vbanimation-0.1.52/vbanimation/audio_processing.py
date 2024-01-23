from re import findall
import subprocess
from manim import *
from .other_functions import get_audio_duration
from .tex_parsing import parse_and_transform_maths


def process_tex_to_text(tex_string):
    tex_string = tex_string.replace(r'\intertext{', r'')
    tex_string = tex_string.replace(r'\\[2mm]', r'')
    tex_string = tex_string.replace(r'&', r'')
    math_expressions = findall(r'\$(.*?)\$', tex_string)
    print(math_expressions)
    for i in math_expressions:
        eng_expr = parse_and_transform_maths(f'${i}$')
        tex_string = tex_string.replace(f'${i}$', eng_expr)
        
    
    print(tex_string)
    return tex_string
    
    
def get_audio(text, key):
    try:
        audio_command = f'say -o {key}.aac {text}'
        duration = get_audio_duration(f'{key}.aac')
        subprocess.call(audio_command, shell=True) 
        return duration
    except:
        return 0.02*len(text)
    
       



        
        

    
    
        

            


       

        



    