from setuptools import setup, find_packages

setup(
    name="plagiarismdeny",
    version="0.1.1",
    author="interceptic",
    author_email="SamMaybe@fluxqol.com",
    description="Disallow plagiarism for a particular project",
    url="https://github.com/interceptic/skyblockaio",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "py-cord",
        "discord.py",
        "discord"
        
    ],
)
