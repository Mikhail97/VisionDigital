import os
import sys
#sys.path.insert(0,'/home/mikhail/it-academy/github/EasyOCR/trainer/')
import torch.backends.cudnn as cudnn
import yaml
import pandas as pd
import argparse
cudnn.benchmark = True
cudnn.deterministic = False


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-trainer_path', type=str, required=True)
    parser.add_argument('-yaml_path', type=str, required=True)
    #parser.add_argument('-saved_model_path', type=str, required=True)
    return parser

def get_config(file_path):
    with open(file_path, 'r', encoding="utf8") as stream:
        opt = yaml.safe_load(stream)
    opt = AttrDict(opt)
    if opt.lang_char == 'None':
        characters = ''
        for data in opt['select_data'].split('-'):
            csv_path = os.path.join(opt['train_data'], data, 'labels.csv')
            df = pd.read_csv(csv_path, sep='^([^,]+),', engine='python', usecols=['filename', 'words'], keep_default_na=False, dtype=str)
            all_char = ''.join(df['words'])
            characters += ''.join(set(all_char))
        characters = sorted(set(characters))
        opt.character= ''.join(characters)
    else:
        opt.character = opt.number + opt.symbol #+ opt.lang_char
    os.makedirs(f'./saved_models/{opt.experiment_name}', exist_ok=True)
    return opt

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    trainer_path = namespace.trainer_path
    yaml_path = namespace.yaml_path
    #saved_model_path = namespace.saved_model_path

    sys.path.insert(0,trainer_path)
    from train import train
    from utils import AttrDict

    #Запускаем обучение
    #opt = get_config("/home/mikhail/it-academy/github/EasyOCR/trainer/config_files/custom_example_colab.yaml")
    opt = get_config(yaml_path)

    #print(opt)
    train(opt, amp=False)