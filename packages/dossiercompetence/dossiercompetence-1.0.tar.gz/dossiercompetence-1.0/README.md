# Projet Dossier Compétence

## Table of contents

- [Installation for DEV](#installation-for-dev)
  
- [Installation for USER](#installation-for-user)
  
- [Usage](#usage)
  
- [Example](#example)
  
***

## Installation for DEV

**Clone the repository and install dependencies:**

```
$ git clone https://gitlab-datalyo.francecentral.cloudapp.azure.com/dossier-de-comp-tences/dossiercompetence.git
```

**If the clone is successful, enter ```ls``` and you will see a folder named 'dossiercompetence', as shown below:**

```
$ ls
>>  dossiercompetence
```

**Change into the example folder:**

```
$ cd dossiercompetence/
```

**Create a python virtual environment for the project:**

```
$ python3 -m venv .venv
```

**If the environment is created successfully, enter `ls -a` and you will see a folder named '.venv', as shown below:**

```
$ ls -a
>> .  ..  .git  .venv  README.md  dossier_competence  dossiercompetence.egg-info  exemple  image  requirements.txt  setup.py
```

**Active the environment:**

```
$ source .venv/bin/activate
```

**Install modules:**

```
$ pip install -r requirements.txt
```

**Copy the required static files to the local computer.:**

```
$ python -m dossier_competence.init_file
>> dossier créé
>> fichiers prêt
```

**Now you have all for run this projet 😊**

**Enter the folder where ``main.py`` is located and you can follow [Example](#example) for run it:**

```
$ python -m dossier_competence.main -h
```

***

## Installation for USER

**Create a folder, for example named 'test' :**

```
$ mkdir test
```

**Go into this folder:**

```
$ cd test
```

**Create a python virtual environment for this upcoming projet:**

```
$ python3 -m venv .venv
```

**Active the environment:**

```
$ source .venv/bin/activate
```

**Install the projet:**

```
$ pip install -e ../dossiercompetence/
```

**Copy the required static files to the local computer.:**

```
$ dossier_competence_copy_file
>> dossier créé
>> fichiers prêt
```

**Now you can use it like as shown below, or you can follow [Example](#example) for run it:**

```
$ dossier_competence -i "plop.pipo/CV_modele.md" -all -style  "file_static/test.css" -all

```

***

## Usage

```
usage: 

main.py [-h] [-i INPUTMD] [-style LIENCSS] [-a] [-html] [-pdf] [-all]

Convertir le fichier Markdown en fichier HTML ou PDF.

options:
  -h, --help            show this help message and exit
  -i INPUTMD, --inputMD INPUTMD
                        Entrer le répertoire du fichier Markdown
  -style LIENCSS, --liencss LIENCSS
                        Entrer le répertoire du fichier css
  -a, --anonimize       sortir le fichier anonyme
  -html, --toHtml       sortir le fichier html
  -pdf, --toPdf         sortir le fichier pdf
  -all, --toAll         sortir tous les fichiers
```

***

## Example

```
$ python -m dossier_competence.main -i yao.xin/dataScience.md -style  "file_static/test.css" -all

$ python -m dossier_competence.main -i dossier_competence/yao.xin/dataScience.md -style  "file_static/test.css" -a -pdf

$ python -m dossier_competence.main -i dossier_competence/yao.xin/dataScience.md -style  "file_static/test.css" -a -html

$ python -m dossier_competence.main -i dossier_competence/yao.xin/dataScience.md -style  "file_static/test.css" -pdf

$ python -m dossier_competence.main -i dossier_competence/yao.xin/dataScience.md -style  "file_static/test.css" -html

```