Python app to zip directories and upload them to AWS S3.

The `mysettings.json` file let's you configure your AWS credentials and the jobs that `backupping.py` will execute. A job is simply a combination of local directory to be zipped and AWS S3 path to be uploaded to.

*Developed with: Python 3.7, Debian 10*

&nbsp;
&nbsp;

# Setup

* Before cloning the repo, create dedicated Linux user `backupping`:
    ```
    sudo adduser --shell /bin/bash --gecos "User" --home /home/backupping backupping
    ```

* Switch to user `backupping` and clone this git repo:
    ```
    sudo su - backupping
    git clone <REPO_URL> repository
    cd repository
    git config core.filemode false
    ```

* Create Python environment:
    ```
    python3 -m venv env
    ```

* Add automatic environment activation to `bashrc`:
    ```
    printf "\nsource ~/repository/env/bin/activate\n" >> ~/.bashrc
    source ~/.bashrc
    ```

* Install dependencies
    ```
    pip3 install -r requirements.txt
    ```

* Create settings file by copying template:
    ```
    cp mysettings.template.json mysettings.json
    ```

* Open `mysettings.json` and customise accordingly:
    ```
    vim mysettings.json
    ```

* Switch back to the previous user:
    ```
    exit
    ```

* Setup cron schedule:
    ```
    sudo vim /etc/crontab
    ```

    ```
    0 0 * * *   backupping   cd /home/backupping/repository; /home/backupping/repository/env/bin/python3 backupping.py >> logs/backupping.log
    ```
