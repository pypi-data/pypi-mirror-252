import inspect
import logging
import os
import shutil
import sys
import traceback
import zipfile
from datetime import datetime
from os.path import join, abspath, isdir, exists, basename, splitext

import paramiko
from google.oauth2.service_account import Credentials

"""
To install libraries:
    pip install -r requirements.txt
"""
import google.cloud.logging
from google.cloud.logging import Resource
from google.cloud.logging_v2.handlers import CloudLoggingHandler, setup_logging

"""
Check README.md for more information
"""


class Log:
    LOGS_FOLDER = "logs"

    LOG_DIR_DATE_FORMAT = '%Y-%m-%d'
    _LOGS_DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S.%f'

    _PROJECT_NAME = os.path.basename(sys.path[1])

    ARCHIVE_SSH_CONFIG = None

    class Level:
        INFO = "I"
        ERROR = "E"
        DEBUG = "D"
        WARNING = "W"

        @staticmethod
        def logger(level):
            if level == Log.Level.INFO:
                return logging.INFO
            if level == Log.Level.ERROR:
                return logging.ERROR
            if level == Log.Level.DEBUG:
                return logging.DEBUG
            if level == Log.Level.WARNING:
                return logging.WARNING
            return logging.NOTSET

    def __init__(self, log_name=None, archive_ssh_config=None):
        self.log_name = log_name
        if archive_ssh_config:
            self.ARCHIVE_SSH_CONFIG = archive_ssh_config

        self._generate_log_name(inspect.stack()[1])
        self.log_dir = _create_dirs()
        self._create_logger()
        self._archive()

        print(f"logs can be found in {self.log_dir}")

        self.cloud_project_id = None

    def verbose(self, text, level):
        if level == self.Level.ERROR:
            text = f"{text}\n{traceback.format_exc()}"
        self.log_dir = _create_dirs()
        self._create_logger()
        self._archive()
        self.logger.log(self.Level.logger(level), text)
        if text:
            print(text)
        self._save_file(text, level)

    def info(self, text):
        self.verbose(text, self.Level.INFO)

    def warning(self, text):
        self.verbose(text, self.Level.WARNING)

    def debug(self, text):
        self.verbose(text, self.Level.DEBUG)

    def error(self, error):
        self.verbose(error, self.Level.ERROR)

    def setup_cloud_logging(self, project_id, credentials=None):
        self.cloud_project_id = project_id

        _resource = Resource(
            type="cloud_function",
            labels={
                "project_id": self.cloud_project_id,
                "function_name": self._PROJECT_NAME
            },
        )
        if credentials:
            client = google.cloud.logging.Client(
                project=self.cloud_project_id,
                credentials=Credentials.from_service_account_info(credentials)
            )
        else:
            client = google.cloud.logging.Client(project=self.cloud_project_id)
        setup_logging(self.handler)
        setup_logging(CloudLoggingHandler(client, resource=_resource))

    def _generate_log_name(self, frame):
        try:
            if not self.log_name:
                module = inspect.getmodule(frame[0])
                self.log_name = basename(module.__file__).replace(".py", "")
                if not self.log_name:
                    self.log_name = sys.argv[0]
                self.log_name = splitext(basename(self.log_name))[0]
        except Exception as e:
            print(f"Error while generating log name: {e}")

    def _create_logger(self):
        if hasattr(self, "handler") and self.log_dir in self.handler.baseFilename:
            return
        self.handler = logging.FileHandler(filename=os.path.join(self.log_dir, "any.log"), encoding='utf-8', mode='a+')
        logging.basicConfig(
            handlers=[
                self.handler
            ],
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%F %T",
            level=logging.NOTSET
        )
        self.logger = logging.getLogger(self.log_name)

    def _save_file(self, log, level):
        self.log_file = join(self.log_dir, f"{self.log_name}.log")
        with open(self.log_file, "a+") as f:
            f.write(f"{self._log_date()} {level}: {log}\n")

    def _log_date(self):
        return datetime.now().strftime(self._LOGS_DATETIME_FORMAT)[:-3]

    def _archive(self):
        today = datetime.now().strftime(self.LOG_DIR_DATE_FORMAT)
        current_year = today[:4]
        log_directories = [
            join(self.LOGS_FOLDER, directory)
            for directory in os.listdir(self.LOGS_FOLDER)
            if isdir(os.path.join(self.LOGS_FOLDER, directory))
               and directory != today
        ]

        if not log_directories:
            return

        zip_path = join(self.LOGS_FOLDER, current_year + ".zip")
        zip_mode = "a" if exists(zip_path) else "w"
        with zipfile.ZipFile(zip_path, zip_mode, zipfile.ZIP_DEFLATED) as zip_file:
            for log_directory in log_directories:
                for file in os.listdir(log_directory):
                    if file.endswith(".log"):
                        file_path = join(log_directory, file)
                        zip_file.write(file_path, arcname=join(os.path.basename(log_directory), file))
                shutil.rmtree(log_directory)

        self._clean_archives()

    def _clean_archives(self):
        archives = [file for file in os.listdir(self.LOGS_FOLDER) if file.endswith(".zip")]
        if len(archives) <= 1:
            return

        self._upload_archives(archives)
        for archive in archives:
            if datetime.now().strftime("%Y") not in archive:
                os.remove(join(self.LOGS_FOLDER, archive))

    def _upload_archives(self, archives):
        if not self.ARCHIVE_SSH_CONFIG:
            return

        ssh = None
        sftp = None
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(**self.ARCHIVE_SSH_CONFIG)

            work_dir = self.LOGS_FOLDER + "/" + self._PROJECT_NAME
            sftp = ssh.open_sftp()
            if self.LOGS_FOLDER not in sftp.listdir():
                sftp.mkdir(self.LOGS_FOLDER)
            if self._PROJECT_NAME not in sftp.listdir(self.LOGS_FOLDER):
                sftp.mkdir(work_dir)
            sftp.chdir(work_dir)
            for archive in archives:
                sftp.put(join(self.LOGS_FOLDER, archive), archive)
        except Exception as _:
            print(f"Error while uploading archives:", traceback.format_exc())
            sys.exit()

        if ssh:
            ssh.close()
        if sftp:
            sftp.close()


def _create_dirs():
    date = datetime.now().strftime(Log.LOG_DIR_DATE_FORMAT)

    log_dir = abspath(join(Log.LOGS_FOLDER, date))
    if not exists(log_dir):
        try:
            os.umask(0)
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            raise Exception(f"Error while creating {log_dir}: {e}")

    return log_dir


_create_dirs()
