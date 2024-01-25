"""External interface for interacting with Object Storage.

This is the top-level interface which all other options should be derived from.
"""

from typing import Optional

from google.auth import identity_pool
from google.cloud import storage
import requests

from replit.storage.bucket import Bucket
from replit.storage.errors import DefaultBucketError


class Client:
  __gcs_client: storage.Client

  def __init__(self):

    creds = identity_pool.Credentials(audience="replit",
                                      subject_token_type="access_token",
                                      token_url="http://0.0.0.0:1106/token",
                                      credential_source={
                                          "url":
                                          "http://0.0.0.0:1106/credential",
                                          "format": {
                                              "type":
                                              "json",
                                              "subject_token_field_name":
                                              "access_token",
                                          },
                                      })
    self.__gcs_client = storage.Client(credentials=creds, project="")

  def bucket(self, bucket_name: Optional[str] = None) -> Bucket:
    if bucket_name is None:
      bucket_name = self.__get_default_bucket_id()

    handle = self.__gcs_client.bucket(bucket_name)
    return Bucket._from_bucket_handle(handle)

  @staticmethod
  def __get_default_bucket_id() -> str:
    response = requests.get(
        'http://0.0.0.0:1106/object-storage/default-bucket')
    try:
      response.raise_for_status()
    except requests.HTTPError as exc:
      raise DefaultBucketError("failed to request default bucket") from exc

    bucket_id = response.json().get("bucketId", "")
    if bucket_id == "":
      raise DefaultBucketError(
          "no default bucket was specified, it may need to be configured in .replit"
      )

    return bucket_id
