AWS_S3_SECURE_URLS = False       # use http instead of https

AWS_QUERYSTRING_AUTH = True     # don't add complex authentication-related query parameters for requests

AWS_S3_ACCESS_KEY_ID = "AKIAJ4VKAJJM4F4KEMMQ"     # enter your access key id

AWS_S3_SECRET_ACCESS_KEY = "oWxHZaHrfkCCX3vTcq5t6YWth0k3xDxpu/yF7s5Q" # enter your secret access key

AWS_STORAGE_BUCKET_NAME = 'vhms-media'

AWS_QUERYSTRING_EXPIRE = 600

S3_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

DEFAULT_FILE_STORAGE = 'vhms.config.s3utils.MediaRootS3BotoStorage'

THUMBNAIL_DEFAULT_STORAGE = 'vhms.config.s3utils.MediaRootS3BotoStorage'

MEDIA_URL = S3_URL + "/media/"