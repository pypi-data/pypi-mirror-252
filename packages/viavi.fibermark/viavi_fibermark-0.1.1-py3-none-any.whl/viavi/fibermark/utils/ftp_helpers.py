from ftputil import FTPHost

from viavi.fibermark.utils.logging import logger


def ftp_connect(DB_URI: str, ftp_user: str, ftp_passwd: str) -> FTPHost:
    ftp_host = FTPHost(DB_URI, ftp_user, ftp_passwd)
    return ftp_host


def ftp_transfer_file(ftp_host: FTPHost, sor_filename: str, file_remote_location: str):
    try:
        ftp_host.upload(
            sor_filename,
            file_remote_location,
        )
        logger.debug("Succeeded file upload")
    except Exception as e:
        logger.warn(f"File upload failed with {e}")
