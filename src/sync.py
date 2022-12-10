"""Provides methods around syncing and usage of AWS s3 buckets as local caches rather than individually
downloading every file"""

import os
import shutil
import boto3 as boto
import multiprocessing
import copy
import hashlib

import logging
log = logging.getLogger(__name__)


class LocalObjectCache:
    """Provides a local cache of an S3 bucket on disk, with the ability to sync up to the latest version of all files"""
    _DEFAULT_PATH = '/tmp/local_object_store/'

    def __init__(self, bucket_name, prefix='', path=None):
        """Init Method
        :param bucket_name: str, the name of the S3 bucket
        :param prefix: str, the prefix up to which you want to sync
        :param path: (optional, str) a path to store the local files
        """
        self.bucket_name = bucket_name
        self.prefix = prefix

        if not path:
            path = self._DEFAULT_PATH + self.bucket_name + '/'

        self.path = path
        os.makedirs(path, exist_ok=True)

        s3 = boto.resource('s3')
        self.bucket = s3.Bucket(self.bucket_name)

    def __enter__(self):
        """Provides a context manager which will open but not sync, then delete the cache on exit"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Provides a context manager which will open but not sync, then delete the cache on exit"""
        self.close()

    def __getstate__(self):
        # Require to pickle and un-pickle the self object between multiprocessing pools
        out = copy.copy(self.__dict__)
        out['bucket'] = None
        return out

    def __setstate__(self, d):
        # Require to pickle and un-pickle the self object between multiprocessing pools
        s3 = boto.resource('s3')
        d['bucket'] = s3.Bucket(d['bucket_name'])
        self.__dict__ = d

    def get_path(self, key):
        """Returns the local file storage path for a given file key"""
        return os.path.join(self.path, self.prefix, key)

    @staticmethod
    def calculate_s3_etag(file, chunk_size=8 * 1024 * 1024):
        """Calculates the S3 custom e-tag (a specially formatted MD5 hash)"""
        md5s = []

        while True:
            data = file.read(chunk_size)
            if not data:
                break
            md5s.append(hashlib.md5(data))

        if len(md5s) == 1:
            return '"{}"'.format(md5s[0].hexdigest())

        digests = b''.join(m.digest() for m in md5s)
        digests_md5 = hashlib.md5(digests)
        return '"{}-{}"'.format(digests_md5.hexdigest(), len(md5s))

    def _get_obj(self, key, tag):
        """Downloads an object at key to file path, checking to see if an existing file matches the current hash"""
        path = os.path.join(self.path, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        dl_flag = True
        try:
            f = open(path, 'rb')
            if tag == self.calculate_s3_etag(f):
                log.info('Cache Hit')
                dl_flag = False
            f.close()
        except FileNotFoundError as e:
            pass

        if dl_flag:
            log.info('Cache Miss')
            self.bucket.download_file(key, path)

    def sync(self):
        """Syncs the local and remote S3 copies"""
        pool = multiprocessing.Pool()
        keys = [(obj.key, obj.e_tag) for obj in self.bucket.objects.filter(Prefix=self.prefix)]
        pool.starmap(self._get_obj, keys)

    def close(self):
        """Deletes all local files"""
        shutil.rmtree(self.path)