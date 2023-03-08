# Property Scraper

This project is a Python-based web scraper that utilizes the Scrapy framework to extract property data from https://www.openrent.co.uk. The script scans all the property pages by using property ID and logs the entries in a local CSV file as well as an online Google Drive sheet using the Google Drive API. It has been deployed on cloud platforms like Railway.




https://user-images.githubusercontent.com/71382503/223599848-2808e7a4-4540-40a6-ab94-cb978d8f34a7.mp4



# Installation

To use this scraper, you must have Python 3 installed on your system along with the Scrapy library. You will also need a Google API key for accessing the Google Drive API.

1. Clone this repository onto your local system using the following command:
```bash
Copy code
git clone https://github.com/[username]/property-scraper.git
```

2. Navigate to the project directory:
```python
Copy code
cd property-scraper
```

3.Copy your Google API key to the main folder.
Set your starting property ID in openrentupdatespider/openrentupdatespider/spiders/openrentupdatespider.py.

# Usage
Once you have installed the necessary dependencies and set your starting property ID, you can run the scraper locally or push it onto the Railway cloud server.

# Running Locally
To run the scraper locally, navigate to the project directory in your terminal and run the following command:
```
css
Copy code
python main.py
This will start the scraper and log the data in both the local CSV file and the Google Drive sheet.
```

# Deploying to Railway
To deploy the scraper to Railway, first create a new app on the Railway dashboard. Then, follow these steps:

Connect your app to this GitHub repository.
Set your Google API key as an environment variable in the Railway dashboard.
Set your starting property ID as a Railway environment variable.
Deploy the app.
Once the app is deployed, you should see the Google Drive sheet entries start increasing as the scraper runs.

