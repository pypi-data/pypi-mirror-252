from setuptools import setup, find_packages

setup(
    name='MyCreds',
    version='0.1.1',
    long_description="The MyCreds project is a python program developed for WatSPEED internal use. Given a course and section number, the program scrapes the student portal (DestinyOne) for a list of students who passed and their data. The program also produces files needed to be uploaded to MyCreds: MyCredsCertificate.csv, and PDF certificates for each passing student.",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mycreds = MyCreds.MyCredspy:__main__',
        ],
    },
    install_requires=[
        'selenium',
        'ReportLab',
    ],
)
