#!/usr/bin/env python

"""
transfer acquisition directory from oneprefix (uri path)
    to another and track it in dispimdb
"""

import contextlib
import concurrent.futures
import logging
import shutil
import urllib.parse

import argschema

import uri_handler
import uri_handler.uri_functions

import ddbclient.acquisition

ONE_MiB = 1024 * 1024
DEFAULT_CHUNK_SIZE = 5 * ONE_MiB


# dispimdb context manager
@contextlib.contextmanager
def creates_dispimdb_acquisition_key(  # ddb_client
                                     ddb_specimen_id,
                                     ddb_acquisition_id,
                                     acquisition_key,
                                     acquisition_md={}):
    """context manager to handle data attaching data storage to a
        dispimdb acquisition

    Parameters
    -----------
    ddb_client:
      dispimdb client object
    ddb_acquisition_id:
      acquisition to which information is written
    acquisition_key:
      key used to describe data stored, e.g. "n5directory_primary"
    acquisition_md:
      additional metadata associated with this acquisition
    """
    # create key with "IN_PROGRESS" status

    base_client_data = {
        "specimen_id": ddb_specimen_id,
        "acquisition_id": ddb_acquisition_id,
    }

    # ddbclient.acquisition.Acquisition(
    #     data=dict(base_client_data, **{
    #         "data_location.{}".format(acquisition_key): dict(
    #             acquisition_md, **{"status": "IN_PROGRESS"}
    #         )})).update_in_db()

    # FIXME currently pydantic doesn't allow updates to data_location subfields
    ddbclient.acquisition.Acquisition(
        data=dict(base_client_data, **{
            "data_location": {acquisition_key: dict(
                acquisition_md, **{"status": "IN_PROGRESS"}
            )}})).update_in_db()

    try:
        yield
        # if success, exit and change to "COMPLETE" status

        # ddbclient.acquisition.Acquisition(
        #     data=dict(base_client_data, **{
        #         "data_location.{}.status".format(acquisition_key): "COMPLETE"
        #         })).update_in_db()

        # FIXME currently pydantic doesn't allow updates to data_location subfields
        ddbclient.acquisition.Acquisition(
            data=dict(base_client_data, **{
                "data_location": {acquisition_key: dict(
                    acquisition_md, **{"status": "COMPLETE"}
                )}})).update_in_db()
    # FIXME bare except
    except Exception:
        # ddbclient.acquisition.Acquisition(
        #     data=dict(base_client_data, **{
        #         "data_location.{}.status".format(acquisition_key): "ERROR"
        #         })).update_in_db()

        # FIXME currently pydantic doesn't allow updates to data_location subfields
        ddbclient.acquisition.Acquisition(
            data=dict(base_client_data, **{
                "data_location": {acquisition_key: dict(
                    acquisition_md, **{"status": "ERROR"}
                )}})).update_in_db()
        raise


def is_fileuri(uri):
    return isinstance(uri_handler.handle_uris.get_uri_handler(),
                      uri_handler.handle_uris.FileUriHandler)


def transfer_uri(src_uri, dst_uri, atomic=False,
                 chunk_size=DEFAULT_CHUNK_SIZE):
    # if atomic and dst is file, make tempfile in same location
    if atomic and is_fileuri(dst_uri):
        raise NotImplementedError

    # copy uri using smart_open
    with uri_handler.uri_functions.uri_smart_open(
             src_uri, "rb", chunk_size) as src_f:
        with uri_handler.uri_functions.uri_smart_open(
                dst_uri, "wb", chunk_size) as dst_f:
            shutil.copyfileobj(src_f, dst_f, chunk_size)

    # if atomic and dst is file, move to expected location


def ldel(string_to_edit, del_string):
    slcstart = (
        len(del_string) if string_to_edit.startswith(del_string)
        else 0)
    return string_to_edit[slcstart:]


# FIXME this should really be included in uri-handler
def get_relative_keys_uri_prefix(uri_prefix):
    for uri in uri_handler.uri_functions.uri_list_uris(uri_prefix):
        prefix_path = urllib.parse.urlparse(uri_prefix).path
        uri_path = urllib.parse.urlparse(uri).path

        yield ldel(uri_path, prefix_path).lstrip("/")


def get_srcs_dsts_uris(src_uri_prefix, dst_uri_prefix):
    for rel_key in get_relative_keys_uri_prefix(src_uri_prefix):
        src_uri = uri_handler.uri_functions.uri_join(src_uri_prefix, rel_key)
        dst_uri = uri_handler.uri_functions.uri_join(dst_uri_prefix, rel_key)
        yield src_uri, dst_uri


def list_srcs_dsts_uris(*args):
    return [*get_srcs_dsts_uris(*args)]


def transfer_uri_prefix(src_uri_prefix, dst_uri_prefix,
                        concurrency=5, transfer_kwargs={}):
    srcs_dsts_l = list_srcs_dsts_uris(src_uri_prefix, dst_uri_prefix)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as e:
        futs = [e.submit(transfer_uri, src_uri, dst_uri, **transfer_kwargs)
                for src_uri, dst_uri in srcs_dsts_l]
        for i, fut in enumerate(concurrent.futures.as_completed(futs)):
            _ = fut.result()
            logging.info("{}/{}".format(i, len(srcs_dsts_l)))


# using argschema here for convenience, but not necessary
class DispimDBAcquisition(argschema.schemas.DefaultSchema):
    acquisition_id = argschema.fields.Str(required=True)

    # FIXME currently specimen_id is required by ddbclient
    acquisition_specimen = argschema.fields.Str(required=True)


class AcquisitionTrackingSchema(argschema.ArgSchema):
    # FIXME
    # dispimdb_endpoint = argschema.fields.Str(required=False)
    # dispimdb_acquisition = argschema.fields.Nested(DispimDBAcquisition)
    acquisition_id = argschema.fields.Str(required=True)

    # FIXME currently specimen_id is required by ddbclient
    acquisition_specimen = argschema.fields.Str(required=True)


class TransferDirectoryInput(AcquisitionTrackingSchema):
    """input parameters to transfer object"""
    input_uri_prefix = argschema.fields.Str(required=True)
    output_uri_prefix = argschema.fields.Str(required=True)

    acquisition_key = argschema.fields.Str(required=True)

    concurrency = argschema.fields.Int(required=False, default=2)


class TransferDirectoryModule(argschema.ArgSchemaParser):
    """"""
    default_schema = TransferDirectoryInput

    def __init__(self):
        super().__init__()
        # self.ddb_client = self._get_ddb_client()

    def _get_ddb_client(self):
        raise NotImplementedError

    def get_metadata(self):
        # example metadata just listing relative object locations
        return {
            "uri": self.args["output_uri_prefix"],
            "contains": [
                i for i in get_relative_keys_uri_prefix(
                    self.args["input_uri_prefix"])]
        }

    def run(self):
        acq_md = self.get_metadata()
        with creates_dispimdb_acquisition_key(
                # self.ddb_client
                # self.args["dispimdb_acquisition"]["specimen_id"],
                # self.args["dispimdb_acquisition"]["acquisition_id"],
                self.args["acquisition_specimen"],
                self.args["acquisition_id"],
                self.args["acquisition_key"],
                acquisition_md=acq_md):
            transfer_uri_prefix(self.args["input_uri_prefix"],
                                self.args["output_uri_prefix"],
                                concurrency=self.args["concurrency"])


if __name__ == "__main__":
    TransferDirectoryModule().run()
