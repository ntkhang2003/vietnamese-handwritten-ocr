import matplotlib.pyplot as plt
from PIL import Image

from vietocr.vietocr.tool.config import Cfg
from vietocr.vietocr.model.trainer import Trainer
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/')
    parser.add_argument('--config', type=str, default='config/config.yml')
    parser.add_argument('--device', type=str, default='cuda:0', help='cuda:0 or cpu')
    parser.add_argument('--weight_path', type=str, default='weights/transformer_ocr.pth')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    data_path = args.data_path
    device = args.device
    weight_path = args.weight_path
    config = args.config
    config = Cfg.load_config_from_file(config)
    dataset_params = {
        'name':'hw',
        'data_root':data_path,
        'train_annotation':'train_annotation.txt',
        'valid_annotation':'val_annotation.txt',
        'image_height':128,
    }

    params = {
            'print_every':100,
            'valid_every':15*100,
            'iters':15000,
            'checkpoint':'./checkpoint/transformerocr_checkpoint.pth',
            'export':'./weights/transformerocr.pth',
            'metrics': 10000,
            'batch_size': 16
            }

    config['trainer'].update(params)
    config['dataset'].update(dataset_params)
    config['device'] = device
    config['pretrain'] = weight_path
    trainer = Trainer(config, pretrained=True)
    trainer.config.save('config.yml')
    trainer.train()
    print(trainer.precision())

if __name__ == "__main__":
    main()