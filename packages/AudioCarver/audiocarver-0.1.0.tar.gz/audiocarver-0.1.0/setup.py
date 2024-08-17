from setuptools import setup, find_packages

setup(
    name='AudioCarver',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'librosa',
        'soundfile',
        'numba',
        'argparse'
    ],
    author='Alicja Misiuda',
    author_email='alicjam@uw.edu',
    description='A library built to carve out minimum seams from an audio file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Aloosha2/AudioCarver',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    project_urls={
        'Record of Changes': 'https://github.com/Aloosha2/AudioCarver/CHANGELOG.md',
        'Source Code': 'https://github.com/Aloosha2/AudioCarver/AudioCarver',
    },
    entry_points={
        'console_scripts': [
            'audio_carver=audio_carver.main:main',
        ],
    },
)