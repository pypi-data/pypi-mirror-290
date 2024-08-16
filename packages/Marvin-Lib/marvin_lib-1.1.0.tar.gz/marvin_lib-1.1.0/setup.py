from setuptools import setup, find_packages

setup(
    name='Marvin-Lib',
    version='1.1.0',
    author='NexVark Industries',
    author_email='kattavishwaksenareddy@gmail.com',
    description='Marvin Lib is a lightweight library designed to simplify and accelerate Marvin code development.')

packages = find_packages()

install_requires = [
        'selenium',
        'webdriver_manager',
        'numpy',
        'flask',
        'pyttsx3',
        'pandas',
        'requests',
        'pyserial',
        'matplotlib',
        'pytest',
        'pyautogui',
]


