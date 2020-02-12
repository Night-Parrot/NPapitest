import yaml
import os
import logging.config
class LogUtil:
    #创建一个字典，用户保存配置
    dictConf = {}
    #配置文件的目录
    LOGGER_CONF_PATH = './'
    #配置文件的名称
    LOGGER_CONF_NAME = 'logging.yml'
    #构造方法
    def __init__(self):
        logYamlPath = self.LOGGER_CONF_PATH + self.LOGGER_CONF_NAME
        self.dictConf = yaml.load(open(logYamlPath, 'r', encoding="utf-8").read(), Loader=yaml.SafeLoader)
    #获得一个logger
    LOGGER_NAME = 'runLogger'
    def getLogger(self,loggerName = LOGGER_NAME):
        logging.config.dictConfig(self.dictConf)
        logger = logging.getLogger(loggerName)
        return logger
