from setuptools import setup

setup(
    name='cli_tool',
    version='0.1.0',
    py_modules=['cli_tool'],
    install_requires=[
        'Click',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'sil = cli_tool:cli',
        ],
    },
)