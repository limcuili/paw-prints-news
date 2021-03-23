Things missing from this repo due to privacy:

1. A secrets_file.py containing NEWS_API_KEY and either one of SLACK_BOT_TOKEN/WEBHOOK.
2. If you want to run this code on a scheduler:
    - clone the repo
    - create the secrets file (as in step 1)
    - create a .bat file containing "\<path to python interpreter\>" "\<path to main.py\>"
    - set the scheduler to call the .bat file.