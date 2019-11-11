Python app to zip directories and upload them to AWS S3.

The `mysettings.json` file let's you configure your AWS credentials and the jobs that `backupping.py` will execute. A job is simply a combination of local directory to be zipped and AWS S3 bucket's path to be uploaded to.

*Developed with: Python 3.5, Debian 9*

&nbsp;
&nbsp;

# Setup

This guide will show you how to setup the codebase into `/var/programs/Backupping`

* Clone repository
    ```
    mkdir -p /var/programs
    git clone <repo_url> /var/programs/Backupping
    ```

* Create and activate Python environment, install packages
    ```
    cd /var/programs/Backupping
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    ```

* Create `mysettings.json` by copying template, then open it and customise it:
    ```
    cd /var/programs/Backupping
    cp mysettings.template.json mysettings.json
    vim mysettings.json
    ```

* Set file permissions:
    ```
    sudo chmod 755 -R /var/programs/Backupping
    sudo chmod 777 -R /var/programs/Backupping/logs
    ```

* Setup cron schedule, for example:
    ```
    crontab -u <USER> -e

    0 0 * * * cd /var/programs/Backupping; /var/programs/Backupping/env/bin/python3 backupping.py >> logs/backupping.log
    ```
