from setuptools import setup, find_packages

setup(
    name='lhackerkarimos',
    version='1.0',
    author='Jaballah Karim',
    author_email='Jaballahkarim233@gmail.com.com',
    description='Package for image classification using a pre-trained model',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0.0',
        'numpy',
    ],
)