"""External interface for interacting with Object Storage buckets."""

from google.cloud import storage


class Bucket:
  __gcs_bucket_handle: storage.Bucket

  def download_as_bytes(self, object_name: str) -> bytes:
    return self.__blob(object_name).download_as_bytes()

  def download_as_text(self, object_name: str) -> str:
    return self.__blob(object_name).download_as_text()

  def download_to_file(self, object_name: str, dest_file) -> None:
    return self.__blob(object_name).download_to_file(dest_file)

  def download_to_filename(self, object_name: str, dest_filename: str) -> None:
    return self.__blob(object_name).download_to_filename(dest_filename)

  def exists(self, object_name: str) -> bool:
    return self.__blob(object_name).exists()

  def upload_from_file(self, dest_object_name: str, src_file) -> None:
    self.__blob(dest_object_name).upload_from_file(src_file)

  def upload_from_filename(self, dest_object_name: str,
                           src_filename: str) -> None:
    self.__blob(dest_object_name).upload_from_filename(src_filename)

  def upload_from_string(self,
                         dest_object_name: str,
                         src_data: str,
                         content_type="text/plain") -> None:
    self.__blob(dest_object_name).upload_from_string(src_data,
                                                     content_type=content_type)

  def __blob(self, object_name: str) -> storage.Blob:
    return self.__gcs_bucket_handle.blob(object_name)

  @staticmethod
  def _from_bucket_handle(handle: storage.Bucket) -> "Bucket":
    bucket = Bucket()
    bucket.__gcs_bucket_handle = handle
    return bucket
