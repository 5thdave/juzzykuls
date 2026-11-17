import os

MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'fayosedavid20@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'khjprznjtjzazbrj')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'fayosedavid20@gmail.com')
MAIL_CONTACT_RECIPIENT = os.environ.get('MAIL_CONTACT_RECIPIENT', 'fayosedavid20@gmail.com')