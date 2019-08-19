#!/usr/bin/env python

import os
import os.path as osp
import json
import shutil
import sys
import io
import yaml

prev_version='1.0'
config_version='1.0'

def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_config_file(configs_dir):
    config_file = os.path.join(configs_dir, 'configs.yml')

    home_dir = os.path.join(os.environ['HOME'])
    configurations = {
        'MUSIC_DIRS': [os.path.join(home_dir, 'Music')],
        'DOWNLOAD_DIR': os.path.join(home_dir, 'Music/LeoMP3/Downloads')
    }

    with io.open(config_file, 'w', encoding='utf8') as outfile:
        yaml.dump(configurations, outfile, default_flow_style=False, allow_unicode=True)

def configure():
    # Create configuration directory and file
    home_dir = os.path.expanduser('~')
    shared_dir = osp.join(home_dir, 'Music', 'LeoMP3')
    sub_dirs = ['Downloads', 'Configs']

    for d in sub_dirs:
        create_dirs(osp.join(shared_dir, d))

    configs_dir = osp.join(shared_dir, "Configs")

    create_config_file(configs_dir)

    icon_pack = "icon_pack"
    icon_folder = osp.join(configs_dir, 'Icons')
    create_dirs(icon_folder)


    for icon in os.listdir(icon_pack):
        icon_path_src = osp.join(icon_pack, icon)
        icon_path_dst = osp.join(icon_folder, icon)
        if osp.exists(icon_folder):
            if not os.path.exists(icon_path_dst):
                    shutil.copy2(icon_path_src, icon_path_dst)


if __name__ == "__main__":
    configure()
