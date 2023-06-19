# LinkedIn Jobs Notifier
LinkedIn Jobs scraper with a Discord bot "front end" written in Python

<img width="596" alt="image" src="https://github.com/hotsno/linkedin-jobs-notifier/assets/71658949/231d1819-56fb-459b-9658-ebd5b33e29cd">

## Features
- Sends new postings on LinkedIn Jobs for a given search query to a Discord channel
- Saves users time from repeat and sponsored postings
- Allows users to blacklist companies
- Provides links to a Google and [Levels.fyi](https://levels.fyi) search of the company

## Requirements
- Python >=3.10
- Git
- Chrome (or Chromium)

## Usage
> **Note**
> If the commands don't work, try `python3` and `pip3` instead, or [make sure you have them in your PATH](https://chat.openai.com/share/3bdc1325-2634-4e5b-9609-a24980c779df)

1. `git clone https://github.com/hotsno/linkedin-jobs-notifier`
2. `cd linkedin-jobs-notifier`
3. `pip install -r requirements.txt`
4. Log in to your LinkedIn account: `python log_in_to_linkedin.py`
5. Edit `.env.example`
6. Run the bot: `python bot.py`
