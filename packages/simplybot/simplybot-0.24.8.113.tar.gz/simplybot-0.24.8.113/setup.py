from setuptools import setup, find_packages

setup(
    name='simplybot',
    version='0.24.08.113',
    packages=find_packages(include=['lib']),
    install_requires=[
        'pyTelegramBotAPI',
        'requests',
    ],
    author='adjisan',
    author_email='support@ailibytes.xyz',
    description='A Python library to build simple Telegram bots more easily',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adjidev/simplybot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
