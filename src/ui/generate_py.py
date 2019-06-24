#!/usr/bin/env python3
import os

for file in [i for i in os.listdir('.') if i.endswith('.ui')]:
    os.system('pyuic5 {} -o ../pyqdpt/views/ui_{}.py'.format(file, file.rstrip('.ui')))
