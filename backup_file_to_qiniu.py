# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu.compat import is_py2, is_py3
import time
import os

# 需要填写你的 Access Key 和 Secret Key
access_key = 'Access_Key'
secret_key = 'Secret_Key'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 当前日期和时间
date = time.strftime('%Y-%m-%d-%H-%M', time.localtime())

# 要备份的目录，多个请用空格分隔
backup_dir = '/data'

# 备份名称
backup_name = 'data'

# 要上传的空间
bucket_name = 'Bucket_Name'

# 上传到七牛后保存的文件名
key = backup_name + '_' + date + '.zip'

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

# 要上传文件的本地路径
localfile = '/tmp/' + key

cmd = 'zip -rq /tmp/' + key + ' ' + backup_dir
os.system(cmd)

ret, info = put_file(token, key, localfile)
print(ret)
print(info)

if is_py2:
    assert ret['key'].encode('utf-8') == key
elif is_py3:
    assert ret['key'] == key

assert ret['hash'] == etag(localfile)

os.system('rm -rf /tmp/' + key)
