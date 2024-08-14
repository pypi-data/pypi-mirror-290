from setuptools import setup, find_packages
from ytdoc import __version__

setup(
    name='youtube-doc',  # Name of the package
    version=__version__,  # Initial release version
    packages=find_packages(exclude=['tests*']),  # Automatically find packages within the project
    install_requires=[
        # List your package dependencies here
        # 'some_dependency>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            # Define scripts here if needed
            'ytdoc=ytdoc.main:main',
        ],
    },
    author='Huseyin Gomleksizoglu',  # Your name
    author_email='huseyim@gmail.com',  # Your email
    description='A helper package for creating title and description for your YouTube videos based on transcription.',  # Short description of your package
    long_description=open('README.md').read(),  # Long description read from the README file
    long_description_content_type='text/markdown',  # Ensure the long description is read as markdown
    url='https://github.com/gomleksiz/youtube-doc',  # URL for your project
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Choose your license
        'Programming Language :: Python :: 3',  # Specify which Python versions you support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='youtube video helper library',  # Add keywords that describe your package
    license='MIT',  # License type
    include_package_data=True,  # Include package data files as specified in MANIFEST.in
)