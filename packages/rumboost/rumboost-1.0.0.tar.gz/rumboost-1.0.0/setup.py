from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Gradient Boosting Decision Trees for Random Utility Models'
LONG_DESCRIPTION = 'A package that allows to estimate some random utility models through gradient boosting decision trees'

# Setting up
setup(
    name="rumboost",
    version=VERSION,
    author="Nicolas Salvadé, Tim Hillel",
    author_email="<nicolas.salvade.22@ucl.ac.uk>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/NicoSlvd/rumboost",
    install_requires=['lightgbm', 'matplotlib', 'seaborn', 'numpy', 
                      'pandas', 'scikit-learn', 'scipy', 'biogeme',
                      'sphinx_rtd_theme'],
    keywords=['python', 'gbdt', 'rum', 'ml'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)