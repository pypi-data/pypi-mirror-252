from setuptools import setup, find_packages

setup(
    name='xss_scanner',
    version='1.0.0',
    description='CVE-2023-29489: XSS Bug scanner for WebPentesters and Bugbounty Hunters',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'pyyaml',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'xss_scanner=xss_scanner.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
