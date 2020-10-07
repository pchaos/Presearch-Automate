# Presearch-Automate
Automate the searching on Presearch website

## Prerequisites

Basic knowledge of this module is required - 
* [Selenium](https://selenium-python.readthedocs.io/)
* pickle
* python-dotenv

## Installation

Installation of this module is required - 

1. Selenium - 
`pip install selenium`

2. python-dotenv -
`pip install -U python-dotenv`

Drivers are required for Selenium like Google Chrome Driver and Mozilla Gecko Driver, those drivers can be downloaded from [seleniumhq](https://www.seleniumhq.org/download/) website.

### Usage
**Note-** Follow the comments

1. Register for [Presearch](https://www.presearch.org/login) website.
2. ``````
     # linux shell
     cp example.env ./.env
``````
Enter your credentials - *email and password* in file ".env".

3. Change the path for json file and selenium driver.
4. Change the proxy setting.

