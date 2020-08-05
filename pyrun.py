#!/usr/bin/python3

import sys
import os

cmds = {
    'run': 'python3 -m src.apis.vagas.vagas_api',
    'test': ''
}

os.system(cmds[sys.argv[1]])
