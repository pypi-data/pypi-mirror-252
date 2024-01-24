from setuptools import setup

setup(
    name='bughunter9',
    version='9.20',
    py_modules=['bughunter9'],
    entry_points={
        'console_scripts': [
            'bughunter9 = bughunter9:main',
        ],
    },
    install_requires=[
        
        'requests',
        'colored==1.4.4',
        'colorama',
        'tqdm',
        'bs4',
        'beautifulsoup4',
        'dnspython',
        'retry',
        'ipcalc',
        'six',
        'ping3',
        
        ],
)
