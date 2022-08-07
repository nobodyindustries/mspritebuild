#!/usr/bin/env python

from sprite_build_command import SpriteBuildCommand
from cleo import Application

msb = Application("msb.py", "0.1")
msb.add(SpriteBuildCommand())

if __name__ == '__main__':
    msb.run()
