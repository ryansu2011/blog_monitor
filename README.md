# Blog Monitor
Not all blogs provide RSS feed or other types of notification systems for new articles. This Blog Monitor project provides a one stop solution for this. With blog monitor, user can monitor multiple blog pages and get Pushbullet notifications when new articles appear.
## Getting Started
### Prerequisits
This project is developed in Python 3 and depend on Scrapy and requests packages. To install these packages with pip:
```
pip install Scrapy
pip install requests
```
The notification system rely on PushBullet service. PushBullet is a cross platform notification service. A PushBullet account is needed and PushBullet app should be installed on the device you want to receive notifications.
 
### Modify Configuration File
First, user need to provide the following information in the configuration file:
* PushBullet user token (you can get is by clicking "Create Access Token" from https://www.pushbullet.com/#settings)
* The hours (24-hour format) you want to receive notification on
* The URL of monitored pages
* The XPATH command to extract the list of articles from the page
* The XPATH command to extract the list of href attributes to destination article page

These configurations should be organized in a json format. See the example configuration file in "/config/example_config.json"
### How to Run Tests
* Modify "/config/test_config.json" file
* Run the following commands to test different components of the code:
```
python ${root_installation}/test/main.py notifier
python ${root_installation}/test/main.py scraper
python ${root_installation}/test/main.py timer
```
### How to Run the Service
* Create configuration file
* Run the following command to start the service
```
python ${root_installation}/src/main.py ${path_to_configuration_file}
```
* You will be asked which device you want to receive notifications






 