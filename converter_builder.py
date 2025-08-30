from pathlib import Path
import os
first_pair = input('введите первую пару ')
second_pair = input('Введите вторую пару ')
variants =  first_pair.split('_') + second_pair.split('_')
even_pair = f'{variants[0]}_{variants[2]}'
if input(f'Вы хотите сделать {even_pair}? ') == 'да':
    from_code = variants[0]
    to_code = variants[2]
    even = True
    result_pair = even_pair
else:
    odd_pair = f'{variants[1]}_{variants[3]}'
    if input(f'Вы хотите сделать {odd_pair}? ') == 'да':
        from_code = variants[1]
        to_code = variants[3]
        even = False
        result_pair = odd_pair
    else:
        exit()
base_dir = Path(__file__).resolve().parent
data_dir = os.path.join(base_dir,'Data')
os.makedirs(os.path.join(base_dir,'converter_output'),exist_ok=True)
temp_dir = os.path.join(base_dir,'converter_output')
if os.path.isdir(os.path.join(data_dir,first_pair)) and os.path.isdir(os.path.join(data_dir,second_pair)):
    os.makedirs(os.path.join(temp_dir, result_pair))
    result_dir = os.path.join(temp_dir, result_pair)
    vocab_dirs = ['sentences', 'vocab']
    for d in vocab_dirs:
        first_files = set(os.listdir(os.path.join(data_dir,first_pair,d)))
        second_files = set(os.listdir(os.path.join(data_dir, second_pair, d)))
        os.makedirs(os.path.join(result_dir,d))
        files = first_files.intersection(second_files)
        for f in files:
            vocab_first = {}

            with open(os.path.join(data_dir, first_pair, d, f), encoding='utf-8') as file:
                for line in file.readlines():
                    s = line.split(';')
                    if even:
                        vocab_first[s[1].strip()] = s[0]
                    else:
                        vocab_first[s[0]] = s[1].strip()
            vocab_second = {}

            with open(os.path.join(data_dir, second_pair, d, f), encoding='utf-8') as file:
                for line in file.readlines():
                    s = line.split(';')
                    if even:
                        vocab_second[s[1].strip()] = s[0]
                    else:
                        vocab_second[s[0]] = s[1].strip()
            result = ''
            for v in vocab_first:
                if v in vocab_second:
                    result += f'{vocab_first[v]};{vocab_second[v]}\n'
            with open(os.path.join(result_dir, d, f), mode='w', encoding='utf-8') as file:
                file.write(result)


