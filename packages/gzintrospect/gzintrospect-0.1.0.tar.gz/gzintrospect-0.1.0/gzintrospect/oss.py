import os
import pandas as pd
import re


class OSS:
    # PREFIX='oss://offline-training-model/'
    PREFIX = ''
    TOKEN = 'CAISjQJ1q6Ft5B2yfSjIr5WBLM7+obV75ImZV2DpskcgSPkduavsoDz2IHhLf3JvBusXtv42mmpR5/kflrNoS5JDV0zDcNttxoRW+AShZIzOoMyoq7cDjcVL34ZQ50epsvXJasDVEfn/GJ70GX2m+wZ3xbzlD0bAO3WuLZyOj7N+c90TRXPWRDFaBdBQVGAAwY1gQhm3D/u2NQPwiWf9FVdhvhEG6Vly8qOi2MaRmHG85R/YsrZK992sfcT6MZA0ZckmDIyPsbYoJvab4kl58ANX8ap6tqtA9Arcs8uVa1sruE3ZaLGLrYY+dFUgOPJjSvEZtoT7m/N8u+re0pjtwhdLPOdaFjjaXJAlPB1KogFUXRqAAWOrnlxAvaULBlTB3cAcA9Ej8Z5NclqRdRBHjBl4HG7qV5Xcwx5U2c0/1HCHBlKARWMAIHYWx512gT8YtvJFXlc7UGYwjK13b68YWERS171lyURGKvuy83r7ler5vfPEMucuuCgYFAv103o71aEbmTjJnca86anetEnEpXhxdtwV'
    AccessKeyId = "STS.NV4gtJLjZSKrUFXVGuDv1VnGB"
    AccessKeySecret = "7b3eeVwHmHfeicZEZey4DhYwweiKvrsfpwHYThVLGPXP"

    def __init__(self) -> None:
        pass

    @staticmethod
    def parse(example_command):
        parts = example_command.strip().split()
        for k, v in zip(parts[:-1], parts[1:]):
            if k == '-t':
                OSS.TOKEN = v
            if k == '-i':
                OSS.AccessKeyId = v
            if k == '-k':
                OSS.AccessKeySecret = v

        return OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret

    @staticmethod
    def list_dir(path, include=None, exclude=None):
        cmd = "ossutilmac64 -t {} -i {} -k {} ls {} -d".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret,
                                                               os.path.join(OSS.PREFIX, path, ''))
        print(cmd)
        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                if not line.startswith(OSS.PREFIX):
                    continue
                line = line.strip()
                line = line.replace(OSS.PREFIX, '')
                if include and include not in line:
                    continue
                res.append(line)
        return res

    @staticmethod
    def list_model(path):
        # cmd = "coscmd list -a %s" % path
        cmd = "ossutilmac64 -t {} -i {} -k {} ls {} -d".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret,
                                                               os.path.join(OSS.PREFIX, path, ''))
        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                if (len(line) < 30):
                    continue
                model = re.search("(model.ckpt.py-\d+)", line)
                if model:
                    res.append(os.path.join(path, model.groups()[0]))
        res = list(set(res))
        res = sorted(res)
        return res

    @staticmethod
    def copy(src, dest, is_dir=False):
        flag = '-r' if is_dir else ''
        cmd = "ossutilmac64 -t {} -i {} -k {} cp {} {} {}".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret, flag,
                                                                  os.path.join(OSS.PREFIX, src, ''),
                                                                  os.path.join(OSS.PREFIX, dest, ''))
        print(cmd)
        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    @staticmethod
    def upload(src, dest, is_dir=False):
        flag = '-r' if is_dir else ''
        cmd = "ossutilmac64 -f -t {} -i {} -k {} cp {} {} {}".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret,
                                                                     flag, src, os.path.join(OSS.PREFIX, dest, ''))
        print(cmd)
        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    @staticmethod
    def download(src, dest, is_dir=True):
        if is_dir:
            cmd = "ossutilmac64 -t {} -i {} -k {} cp -r {} {}".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret,
                                                                      os.path.join(OSS.PREFIX, src, ''), dest)
            print(cmd)
            res = []
            with os.popen(cmd, 'r') as fr:
                for line in fr:
                    line = line.strip()
                    res.append(line)
            return res
        else:
            for e in src:
                cmd = "ossutilmac64 -t {} -i {} -k {} cp -r {} {}".format(OSS.TOKEN, OSS.AccessKeyId,
                                                                          OSS.AccessKeySecret,
                                                                          os.path.join(OSS.PREFIX, e), dest)
                print(cmd)
                with os.popen(cmd, 'r') as fr:
                    for line in fr:
                        print(line)

    @staticmethod
    def delete(path, folder=False):
        if folder:
            flag = '-r'
        else:
            flag = ''
            for e in path:
                cmd = "ossutilmac64 -t {} -i {} -k {} rm {}".format(OSS.TOKEN, OSS.AccessKeyId, OSS.AccessKeySecret,
                                                                    os.path.join(OSS.PREFIX, e))
                print(cmd)
                with os.popen(cmd, 'r') as fr:
                    for line in fr:
                        print(line)