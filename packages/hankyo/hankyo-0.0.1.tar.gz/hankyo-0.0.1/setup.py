import setuptools

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name="hankyo", # Replace with your own username
    version="0.0.1",
    author="Hankyo Jeong",
    author_email="tkfka1@korea.com",
    install_requires=[],
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tkfka1/hankyo_pypi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# install_requires=['tqdm', 'pandas', 'scikit-learn',],
# keywords=['teddynote', 'teddylee777', 'python datasets', 'python tutorial', 'pypi'],
# package_data={},
# zip_safe=False,
# classifiers=[
#     'Programming Language :: Python :: 3.6',
#     'Programming Language :: Python :: 3.7',
#     'Programming Language :: Python :: 3.8',
#     'Programming Language :: Python :: 3.9',
# ],