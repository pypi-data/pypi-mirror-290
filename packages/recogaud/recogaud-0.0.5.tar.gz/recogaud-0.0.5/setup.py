from setuptools import setup, find_packages

setup(
    name='recogaud',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'speechrecognition',
        'pydub',
        'telethon',
        'asyncio',
    ],
    python_requires='>=3.7',
    description='A library for speech recognition and Telegram integration.',
    author='Alex',
    author_email='firi8228@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
