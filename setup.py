from setuptools import setup, find_packages

setup(
    name='kivy_projectile',
    version='0.0.1',
    description='A professional modular framework for Kivy/KivyMD application development',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),   # بدون پارامتر where و package_dir
    install_requires=[
        'kivy>=2.3.0',
        'kivymd>=1.1.1',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    license='MIT',
    url='https://github.com/divone3/kivy_projectile',
)