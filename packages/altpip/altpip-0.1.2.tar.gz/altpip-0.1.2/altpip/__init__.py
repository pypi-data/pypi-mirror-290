"""
AltPIP - инструмент для создания полу-виртуальных сред (как venv).

AltPIP is a tool for creating semi-virtual environments (like venv).
"""

def cli():
    import sys
    from . import core
    core.main(sys.argv)