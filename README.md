# NP-CCA-web-scraper

## Project Description

A scrub attempt to scrape something using selenium and python. 

This project aims to scrape the Co-Curricular Activities (CCA) or club information
from [Ngee Ann Polytechnic's web page](https://www.np.edu.sg/studentlife/Pages/ccas.aspx)

## Project Setup

1. Clone this project
2. Install Python `(preferably version 3.7)`
3. Install dependencies in `requirements.txt` via:

```
pip install -r requirements.txt
```

### Run the web scraper

Run the following command to start the web scraper:

```
python main.py
```

By default, the web scraper will launch a browser when the script is executed. Add the `--browser-option` or `-bo` flag
with the value `headless` to the end of the command:

```
python main.py --browser_options="headless"

or 

python main.py -bo="headless"
```

### Note:
Some post processing on the data is required after running the web scraper!

Feel free to provide feedback or any issues encountered by opening an issue in the repository! Pull requests accepted as well!