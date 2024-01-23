#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name="dossiercompetence",
    version="1.0",
    description="Anonymisation et filtrage des termes dans le CV, décoration et style des CV produits.",
    author="Xin Yao",
    author_email="xin.yao@datalyo.com",
    url="https://gitlab-datalyo.francecentral.cloudapp.azure.com/dossier-de-comp-tences/dossiercompetence",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Markdown",
        "weasyprint"
    ],
    entry_points={
        'console_scripts': [
            'dossier_competence = dossier_competence.main:main',
            'dossier_competence_copy_file = dossier_competence.init_file:main'
        ]
    },
    data_files=[
        ('/home/xin/test/dossier_competence/', ['webBlanche.html'])
        ]
)