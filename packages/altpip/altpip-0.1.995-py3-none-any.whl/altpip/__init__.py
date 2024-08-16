"""
AltPIP - инструмент для создания полу-виртуальных сред (как venv).

AltPIP is a tool for creating semi-virtual environments (like venv).
"""

def cli():
    from . import core
    import sys
    core.main(sys.argv)