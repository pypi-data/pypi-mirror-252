from setuptools import setup, find_packages

setup(
    name='my_math_lib_my',
    version='0.1.2',
    packages=find_packages(),
    description='A simple math library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_math_lib_my',
    license='MIT',
    install_requires=[
        # List your package dependencies here
        # e.g., 'numpy', 'pandas'
    ],
    classifiers=[
        # Classifiers help users find your package
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
