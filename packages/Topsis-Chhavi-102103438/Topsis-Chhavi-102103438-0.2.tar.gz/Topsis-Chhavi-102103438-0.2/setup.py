from setuptools import setup, find_packages

setup(
    name='Topsis-Chhavi-102103438',
    version='0.2',
    packages=find_packages(include=['topsis*', 'topsis.*']),
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'topsis-cli = toppers.topsis:perform_topsis',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
