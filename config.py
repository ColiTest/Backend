import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siemens'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CAN_INTERFACE = os.environ.get('CAN_INTERFACE') or 'pcan'
    CAN_CHANNEL = os.environ.get('CAN_CHANNEL') or 'PCAN_USBBUS1'
    CAN_BITRATE = int(os.environ.get('CAN_BITRATE') or 500000)

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY