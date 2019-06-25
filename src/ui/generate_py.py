#!/usr/bin/env python3
import os

for file in [i for i in os.listdir('.') if i.endswith('.ui')]:
    os.system('pyuic5 --from-imports {} -o ../pyqdpt/views/ui_{}.py'.format(file, file.rstrip('.ui')))

os.system('pyrcc5 -no-compress {} -o ../pyqdpt/views/assets_rc.py'.format('../../assets/assets.qrc'))
