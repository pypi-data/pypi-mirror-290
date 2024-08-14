from setuptools import setup, find_packages

setup(
    name='mendel_plotly_theme',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A custom Plotly theme package',
    readme="README.md",
    install_requires=[
        'plotly>=4.0.0',
    ],
    author='Mendel Engelaer',
    author_email='ante_stamp.0a@icloud.com',
    url='https://github.com/Mensel123/mendel-plotly-theme',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
