from setuptools import find_packages, setup

setup(
    name="DMBotTools",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Angels And Demons dev team",
    author_email="dm.bot.adm@gmail.com",
    description="Инструменты используемые для проектов DMBot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AngelsAndDemonsDM/DM-Bot-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    license="GPL-3.0",
)
