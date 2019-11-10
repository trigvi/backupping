# -*- coding: utf-8 -*-

import boto3
import datetime
import json
import os
import sys
import subprocess


def print_and_flush(message):

    dt = datetime.datetime.now().isoformat()
    print("{} - {}".format(dt, message))
    sys.stdout.flush()


def create_backup_file(local_directory, local_zipfile, zip_exclude):

    if not os.path.exists(local_directory):
        print_and_flush("Skipping, directory does not exist: " + local_directory)
        return

    if len(local_directory.split("/")) < 3:
        print_and_flush("Skipping, only 2+ level directories supported: " + local_directory)
        return

    dir_pre     = os.path.split(local_directory)[0]
    dir_name    = os.path.split(local_directory)[1]

    exclude = ""
    for exc in zip_exclude:
        exclude += "--exclude=" + exc + " "

    command = [
        "rm " + local_zipfile,
        "cd " + dir_pre,
        "zip -r " + exclude + " " + local_zipfile + " " + dir_name,
    ]

    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            "; ".join(command),
            stdout=devnull,
            stderr=devnull,
            shell=True
        )
        process.wait()


# Read settings
try:

    settings = {}
    with open("./mysettings.json") as f:
        settings = json.load(f)

    aws_key     = settings["aws"]["key"]
    aws_secret  = settings["aws"]["secret"]
    aws_region  = settings["aws"]["region"]
    aws_bucket  = settings["aws"]["bucket"]
    jobs        = settings["jobs"]
    zip_exclude = settings["zip_exclude"]

except Exception as e:
    print_and_flush("Error reading settings - " + str(e))
    sys.exit()


# Create backup files and upload them to S3
try:

    for local_directory, remote_zipfile in jobs.items():

        # Create backup file locally
        local_zipfile = "/tmp/" + os.path.split(remote_zipfile)[1]
        print_and_flush("Creating: " + local_zipfile)
        create_backup_file(local_directory, local_zipfile, zip_exclude)


        # Upload backup file to S3
        session = boto3.Session()
        s3_client = session.client(
            "s3",
            aws_access_key_id = aws_key,
            aws_secret_access_key = aws_secret,
            region_name = aws_region,
        )

        print_and_flush("Uploading to S3 ({}): {}".format(aws_bucket, remote_zipfile))
        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer(client=s3_client, config=tc)
        t.upload_file(local_zipfile, aws_bucket, remote_zipfile)


        # Remove local file
        if os.path.exists(local_zipfile):
            os.remove(local_zipfile)

except Exception as  e:
    print_and_flush(str(e))

