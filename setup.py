from setuptools import setup, find_packages

def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name='kivy_projectile',
    version='0.0.1',
    description='A professional modular framework for Kivy/KivyMD application development',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/divone3/kivy_projectile',
    license='MIT',
    packages=find_packages(include=["kivy_projectile", "kivy_projectile.*"]),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'kivy>=2.3.0',
        'kivymd>=1.1.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Kivy',
        'Framework :: KivyMD',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='kivy kivymd framework modular ui orm',
    package_data={
        "kivy_projectile": ["*.py", "*/*.py"],
    },
    # اگر فایل‌های داده غیر پایتونی دارید می‌توانید اضافه کنید:
    # data_files=[("config", ["kivy_projectile/app/settings.py"])]
)