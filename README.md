# upload-post-stats

Make sure each blog post in https://poanchen.github.io/blog have stats (for example, total views).

## Why is this useful?

When user click on a blog post, they should have the ability to see how popular the blog post is and how many views it has been generated. One metric that is useful in this case is total views. To get the total views calculated on your own isn't easy, not only that, you also need to give user a correct number of views. Here is where the [Google Analytics](https://analytics.google.com) comes into play, I have been using Google Analytics to track my website performance since day one, all the data is there, I just need to call the Google's [Core Reporting API](https://developers.google.com/analytics/devguides/reporting/core/v3/) to get the total view for each post, and then show it to the user. In a nutshell, this is how it works, check out the site's sitemap.xml to get a list of blog posts, call the Google's API to get views, store it as JSON and then simply upload the file to [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/). And, of course, we need to do this once a day. (To keep the data fresh with one day old data) Of course, as a Software Engineer, we love automation. We love writing code that will help use to avoid doing the manul work. With automation, all these can be done once and for all. How does that sound?

## Getting started

### Prerequisites:
- Python 2.7 or up
- A remote web server that allows you to run a cron job

### Installation
To begin, make sure you already have a Google Analytics account, if not please create one [here](https://analytics.google.com/). Next, you would need to create a [Service Accounts](https://developers.google.com/analytics/devguides/reporting/core/v4/authorization#service_accounts) so that you can authenticate with Analytics API. At last, you would also need a Microsoft Azure account, please create one over [here](https://azure.microsoft.com/en-us/features/azure-portal/) if you do not have one.

### Development environment
Tested on Ubuntu 14.04.X LTS server but theoretically it should work for linux-based OS server as well.

### Usage
You want to change the config file to match your own settings,
```
config = {}

config['absolute_path_to_this_project'] = 'absolutePathToThisProject'
config['json_file_name'] = "fileName.json"

# XML
config['xml_url'] = 'urlToYourXml'
config['xml_file_name'] = 'yourFileName'

# Google's Core Reporting API
config['client_secret_file_name'] = 'yourFileName.json'
config['views_start_date'] = 'views_start_date' # 2020-01-01
config['views_end_date'] = 'views_end_date' # 2020-02-01

# Azure Portal
config['account_name'] = 'azureAccountName'
config['account_key'] = 'azureAccountKey'

# Azure Blob Storage
config['container_name'] = 'containerName'
```
In case you do not know what your account name, account key, or even container name, check out [this](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#copy-your-credentials-from-the-azure-portal) tutorial by [Microsoft](https://docs.microsoft.com). Please make sure not to commit your azure account key to public site like GitHub.com. Use environment variable to make it a secret while keeping the code on GitHub. If you need help on this, check out [this](https://github.com/poanchen/add-alexa-rank-ifttt#usage).

Now, all you need to do is to hook this script up with a cron job and you are done.

This is how I set up my cron job.
```
00 6 * * * cd /path/to/the/upload-post-stats; python script.py >> output.log;
```
This cron job will run the script once a day at 6am sharp. It will also record any log to the output.log for debugging purposes.
