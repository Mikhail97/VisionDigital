import os
import argparse
import sys
import pandas as pd

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-datapath', type=str, required=True)
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    datapath = namespace.datapath


    path = datapath #'/home/mikhail/it-academy/Diplom_project/data/Dataset/data/train'
    #val_path = datapath #'/home/mikhail/it-academy/Diplom_project/data/Dataset/data//val'

    data = [(name, name.split('_')[0]) for name in os.listdir(path)]

    with open(path +'/labels.csv','w') as f:
      f.writelines('filename,words'+'\n')
      for filename, words in data:
        if filename !='labels.csv' and filename !='.ipynb_checkpoints':
          f.writelines(filename+','+words+'\n')

    df = pd.read_csv(path +'/labels.csv', sep=',', dtype=str)
    print(df)