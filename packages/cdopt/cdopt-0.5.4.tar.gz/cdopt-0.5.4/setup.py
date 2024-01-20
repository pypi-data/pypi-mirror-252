import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdopt", 
    version="0.5.4",
    author="Nachuan Xiao, Xiaoyin Hu, Xin Liu, Kim-Chuan Toh",
    author_email="xnc@lsec.cc.ac.cn",
    description="A Python package for optimization on closed Riemannian manifolds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cdopt.github.io/",
    packages=setuptools.find_packages(),
    keywords=("Optimization, Riemannian optimization"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['numpy>=1.16', 'scipy>=1.7.0', 'autograd'],
    data_files=[
            "LICENSE",
            "README.md"]
)