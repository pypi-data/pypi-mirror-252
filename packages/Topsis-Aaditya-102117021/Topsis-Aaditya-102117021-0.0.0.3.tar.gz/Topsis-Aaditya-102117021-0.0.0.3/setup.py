from setuptools import setup, find_packages

VERSION = '0.0.0.3'
DESCRIPTION = 'Implementing TOPSIS'
LONG_DESCRIPTION = 'Technique for Order of Preference by Similarity to Ideal Solution is a multi-criteria decision analysis method'

# Setting up
setup(
    name="Topsis-Aaditya-102117021",
    version=VERSION,
    author="intrinsicvardhan (Aaditya Vardhan)",
    author_email="intrinsicvardhan@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'':['docs/*']},
    install_requires=['pandas', 'numpy'],
    keywords=['topsis', 'decision-analysis', 'similarity'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)