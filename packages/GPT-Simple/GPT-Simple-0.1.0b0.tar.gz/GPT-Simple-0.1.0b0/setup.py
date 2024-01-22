from setuptools import setup, find_packages

setup(
    name='GPT-Simple',
    version='0.1.0-beta',
    author='PolyPenguin',
    author_email='polypenguindev@gmail.com',
    description='an easier to use version of the OpenAI library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=["requests"]
)