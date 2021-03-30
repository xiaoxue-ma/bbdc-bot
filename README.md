# bbdc-bot
A bot to get notifications via telegram when slots available in bbdc

## Dependencies
- requirements.txt
- Install ChromeDriver based on your chrome version [here](https://chromedriver.chromium.org/downloads) to current directory
  - You could also specify the path in main.py

## Prepare cookie from bbdc
Rename cookie.example.json to cookie.json and replace the value with cookies you get from browser after login
- This script can only be run successfully when the cookies are valid
- You will need to change the cookies every 20min - 2h

## Prepare api secrets for telegram bot
Rename telegram_secrets.example.json to telegram_secrets.json and replace the value with your API secrets
- You will need to verify via OTP during the first time you run this script
- You will only need to setup this once

## Start the bot!
```
python main.py
```
