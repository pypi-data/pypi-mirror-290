# setup.py
from setuptools import setup, find_packages

setup(
    name='checkBest',  # نام بسته
    version='0.1',  # نسخه اولیه
    packages=find_packages(),  # به طور خودکار تمام بسته‌ها را پیدا می‌کند
    install_requires=[
        'regex==2023.10.3',
        'jdatetime==4.1.1',
    ],
    author='Bestsenator',
    author_email='senator136019@gmail.com',
    description='A collection of Python functions designed to validate various types of input. These functions can be used to ensure that user inputs such as passwords, emails, and other required fields meet specific criteria.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Bestsenator/checkBest',  # آدرس مخزن گیت‌هاب
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # نسخه پایتونی که بسته شما نیاز دارد
)
