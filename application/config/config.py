import os

#basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '/tmp/LCT.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
