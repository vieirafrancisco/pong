import setuptools

setuptools.setup(
    name="pong",
    version="0.0.1",
    url="https://github.com/vieirafrancisco/pong/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Ubuntu-20.04",
    ],
    install_requires=(
        'pygame>=2.0.0',
    ),
    python_requires='>=3.6',
)