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

Next, download the web driver file of your browser from the relevant official website and place it in the `driver` directory of this project.

> Currently, the scraper supports only [`Chrome`](https://chromedriver.chromium.org/), [`Edge Chromium`](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/), [`Firefox`](https://github.com/mozilla/geckodriver), [`Opera`](https://github.com/operasoftware/operachromiumdriver) and [`Safari (comes with mac)`](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari) browsers. Only Edge chromium is tested so far but the rest should work.

Once the webdriver is downloaded and added to the directory, specify the **type** of webdriver that you are using and the **name** of webdriver file in the `driver_config.yaml`. The yaml file can be found in the root of the project.

An example of valid configuration in `driver_config.yaml`:

```
type:
    edge
name:
    msedgedriver
```

The types of driver specified **must** be one of the following and is case insensitive:

```
Google chrome or Chrome
Edge chromium or Edge
Firefox
Opera
Safari
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

Feel free to provide feedback or any issues encountered by opening an issue in the repository. Pull requests accepted as well!
