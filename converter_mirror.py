from pathlib import Path
import os

from_code = input('Введите код пары, которую вы хотите отзеркалить')

base_dir = Path(__file__).resolve().parent
data_dir = os.path.join(base_dir,'Data')
os.makedirs(os.path.join(base_dir,'converter_output'),exist_ok=True)
temp_dir = os.path.join(base_dir,'converter_output')
if os.path.isdir(os.path.join(data_dir,from_code)):
    reverse_code = '_'.join(from_code.split('_')[::-1])
    os.makedirs(os.path.join(temp_dir,reverse_code))
    reverse_dir = os.path.join(temp_dir,reverse_code)
    vocab_dirs = ['sentences','vocab']
    for d in vocab_dirs:
        files = os.listdir(os.path.join(data_dir,from_code,d))
        os.makedirs(os.path.join(reverse_dir,d))
        for f in files:
            result = ''
            with open(os.path.join(data_dir,from_code,d,f),encoding='utf-8') as file:
                for line in file.readlines():
                    result += ';'.join(line.strip().split(';')[::-1])+'\n'
            with open(os.path.join(reverse_dir,d,f),mode='w',encoding='utf-8') as file:
                file.write(result)
    print('Успех!')
else:
    print('Такой директории нет')
