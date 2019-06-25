#!/usr/bin/env python3
import os

for file in [i for i in os.listdir('src/ui') if i.endswith('.ui')]:
    print(file)
    os.system('pyuic5 --from-imports src/ui/{} -o src/pyqdpt/views/ui_{}.py'.format(file, file.rstrip('.ui')))

os.system('pyrcc5 -no-compress {} -o src/pyqdpt/views/assets_rc.py'.format('assets/assets.qrc'))
