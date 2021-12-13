Installation
---------------------
Download project from github
git clone https://github.com/panostraf/search_engine_term_project.git
python -m venv venv
venv\Scripts\activate (for Windows)
source venv/bin/activate (mac/linux)


Run Crawler
--------------------
in the main directory execute:
python techradar/main.py

Notes
-------------------
It is structured like that because it has been deployed to heroku.com in order to scrap website remotely
The spider that is actually scrape the data is the reviews.py
