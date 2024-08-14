""" 
Programa : Utils module for Canvas
Fecha Creacion : 07/08/2024
Fecha Update : None
Version : 1.0.0
Actualizacion : None
Author : Jaime Gomez
"""

import re
import unicodedata

# Function to clean HTML tags from the text
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def remove_tilde(text):
    # Normalize the text to decompose characters into base characters and diacritics
    normalized_text = unicodedata.normalize('NFD', text)
    # Filter out the diacritic marks
    filtered_text = ''.join([char for char in normalized_text if not unicodedata.combining(char)])
    return filtered_text