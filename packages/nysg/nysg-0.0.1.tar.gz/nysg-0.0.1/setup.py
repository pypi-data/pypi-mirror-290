from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRIPTION = "Una colección de funciones utiles para labo FCEN UBA Física"

# Setting up
setup(
    name="nysg",
    version=VERSION,
    author="Santiago Noya",
    author_email="<noyasantiagomail@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["opencv-python", "pyautogui", "pyaudio"],
    keywords=["python", "laboratory", "UBA", "FCEN", "Física"],
)
