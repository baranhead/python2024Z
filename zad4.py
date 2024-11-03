import json
import sys
from functools import reduce

def ipynb_to_py(in_name):

#otwarcie pliku wejsciowego
    with open(in_name, 'r', encoding='utf-8') as input:
            data = json.load(input)

#przetworzenie komorek
    lines = []
    for cell in data['cells']:

        if cell['cell_type'] == 'markdown':
            text = ''.join(map(lambda line: f"# {line}", cell['source']))
            lines.append(f"{text}\n\n")

        elif cell['cell_type'] == 'code':
            code = ''.join(map(str, cell['source']))
            lines.append(f"{code}\n\n")

#zapis do pliku .py
    out_name = in_name.replace('.ipynb', '.py')
    with open(out_name, 'w', encoding='utf-8') as output:
            print(*lines, file=output, sep='', end='')

#zliczenie liczby cwiczen
    exercise_cells = filter(lambda cell: cell['cell_type'] == 'markdown' and cell['source'] and "# Ćwiczenie" in cell['source'][0], data['cells'])
    print (f"Liczba ćwiczeń: {sum(1 for _ in exercise_cells)}")
    

#funkcja main
if __name__ == "__main__":

#weryfikacja poprawnosci wejscia
    if len(sys.argv) != 2:
        print("Niepoprawne uruchomienie programu!")
        sys.exit(1)

    in_name = sys.argv[1]
    if not in_name.endswith('.ipynb'):
        print("Plik nie ma rozszerzenia .ipynb!")
        sys.exit(1)

    ipynb_to_py(in_name)
