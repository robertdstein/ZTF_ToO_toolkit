import os
import logging
from ztfquery import io

# AMPEL API credentials

API_BASEURL = "https://ampel.zeuthen.desy.de"
API_ZTF_ARCHIVE_URL = API_BASEURL + "/api/ztf/archive"
API_CATALOGMATCH_URL = API_BASEURL + "/api/catalogmatch"
API_CUTOUT_URL = API_BASEURL + "/api/ztf/archive/cutouts"

# Manage ztfquery logins from environment variables


def load_credentials(name):
    """ZTFquery wrapper for loading credentials.
    """
    return io._load_id_(name)


try:
    io.set_account("ampel_api",
                   username=os.environ["AMPEL_API_USER"],
                   password=os.environ["AMPEL_API_PASSWORD"])
    logging.info('Set up "ampel_api" credentials')

except KeyError:
    logging.info('No Credentials for AMPEL API found in environment'
                 'Assume they are set.')

try:
    io.set_account("irsa",
                   username=os.environ["IRSA_USER"],
                   password=os.environ["IRSA_PASSWORD"])
    logging.info('Set up "irsa" credentials')

except KeyError:
    logging.info('No Credentials for "irsa" found in environment'
                 'Assuming they are set.')

try:
    io.set_account("skyvision",
                   username=os.environ["SKYVISION_USER"],
                   password=os.environ["SKYVISION_PASSWORD"])
    logging.info('Set up "skyvision" credentials')

except KeyError:
    logging.info('No Credentials for "skyvision" found in environment'
                 'Assuming they are set.')
