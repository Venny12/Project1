Project Name:- Exercise: Package a Utility Library and Kick Off Project 1 (QE Foundations)

One-sentence purpose - Today's exercise we create a Git repository called qe-foundations containing the importable packages.

-------------------------------------------------
Project 1 milestone - Week 2, Monday Section
-------------------------------------------------
Project 1 milestone (Monday): "Kickoff - repo + structure." By the end of today you own ONE Git repository called qe-foundations containing the importable package qe_foundations/ with its first sub-package qe_foundations/utils/, a documented virtual-environment setup, requirements.txt / requirements-dev.txt, and empty placeholder folders for the rest of the week. This same repo is used all week (Tue qe_foundations/ingestion/, Wed logging + unit tests in tests/, Thu sql/ validation queries, Fri joins validation + integration). Keep the names exactly as written here.

-------------------------------------------------
Setup Section
-------------------------------------------------
1. Create a Virtual Environment - Create venv 
    py -m venv .venv
    python -m venv .venv
2. Activate the Virtual Environment
    Windows- .venv\Scripts\Activate.ps1 
    MacOS- source .venv/bin/activate
3. Install  Dependencies
    python -m pip install -r requirements.txt   
    python -m pip install -r requirements-dev.txt
4. Verify
    python smoke_utils.py 

-------------------------------------------------    
Usage example
-------------------------------------------------
///////CODE///////
from qe_foundations.utils import slugify, mask_email
print(slugify("Hello World"))
print(mask_email("tester@example.com"))

///////EXPECTED OUTPUT///////
hello-world
t***@example.com