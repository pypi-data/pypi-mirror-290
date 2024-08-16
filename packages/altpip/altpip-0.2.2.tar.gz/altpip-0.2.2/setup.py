from setuptools import setup, find_packages
import os, json

_version = "0.2.2"
hdir = os.path.expanduser("~")
if ".apipenv" not in os.listdir(hdir):
    os.mkdir(os.path.join(hdir, '.apipenv'))
    os.mkdir(os.path.join(hdir, '.apipenv/libs'))
    with open(os.path.join(hdir, '.apipenv/config.json'), "x") as f:
        json.dump({"libs" : {}, "altpip-version" : _version}, f)
else:
    config = json.load(open(os.path.join(hdir, '.apipenv/config.json')))
    if "libs" not in config:
        config["libs"] = {}
    if "altpip-version" not in config or config['altpip-version'] != _version:
        config["altpip-version"] = _version
    
    with open(os.path.join(hdir, '.apipenv/config.json'), "w") as f: json.dump(config, f)
if 'TERMUX_VERSION' in os.environ:
    print("WARN: Termux пока-что не поддерживается! AltPIP будет работать некорректно.")

setup(
    name='altpip',
    version=_version,
    packages=find_packages(),
    author='nesquick',
    author_email='nesquary@gmail.com',
    description='AltPIP - a tool for creating projects with the required versions of libraries without using virtual environments (like venv)',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    entry_points={
        'console_scripts': [
            'altpip=altpip:cli'
        ],
    },
    install_requires=[
        'tqdm'
    ]
)