from xml.dom import minidom
from system.log import log
import os

class Config(object):
    singleton = None
    workingpath = None
    xmlconfig = None
    
    configdict = dict()
    
    config = {
        "gui.show" : { "default": "false", "type": "bool", "label":"", "showgui":"false", "order": 0 },
        "webserverport" : { "default": "8080", "type": "int", "label":"", "showgui":"false", "order": 0}
    }
    
    def __init__(self):
        Config.singleton = self
    
    def getSingleton():
        return Config.singleton or Config()
    
    def init(self, pathname):
        pathname = pathname.strip()
        pathname.replace('\\','/')
        if pathname.endswith('/'):
            pathname = pathname[0:-1]
        Config.workingpath = pathname
        
        self.xmlconfigfile = Config.workingpath+'/config.xml'
        log.debug('Config: read config file: '+self.xmlconfigfile)
        self.xmlconfig = minidom.parse(self.xmlconfigfile)
    
        for parname in self.config:
            elements = self.xmlconfig.getElementsByTagName(parname)
            if len(elements)==0:
                self.config[parname]['value']=self.config[parname]['default']
                self.config[parname]['file']=None
                log.debug('config: couldnt find '+parname+', using defaut: '+self.config[parname]['value'])
            if len(elements)>1:
                log.warn('config: more than one '+parname+' in config!')
            if len(elements)==1:
                self.config[parname]['value']=elements[0].childNodes[0].data
                self.config[parname]['file']=elements[0].childNodes[0].data
                log.debug('config: found '+parname+': '+self.config[parname]['value'])
        
        
    def getAllParameter(self):
        return self.config;
    def setAllParameter(self,jsonparameter):
        for p in jsonparameter:
            self.config[p]['value'] = jsonparameter[p]['value']
    def defaultAllParameter(self):
        for p in self.config:
            self.config[p]['value'] = self.config[p]['default']
    def saveAllParameter(self):
        for parname in self.config:
            self.config[parname]['file']=self.config[parname]['value']
            elements = self.xmlconfig.getElementsByTagName(parname)
            if len(elements)!=1:
                log.debug('config: parameter '+parname+' not in config file?')
                # TODO: create parameter!
                
                newparam = self.xmlconfig.createElement(parname)
                newparamvalue = self.xmlconfig.createTextNode( str(self.config[parname]['file']) )
                newparam.appendChild( newparamvalue  )
                self.xmlconfig.childNodes[0].appendChild(newparam)
                linebreak = self.xmlconfig.createTextNode("\n\n    ")
            else:
                elements[0].childNodes[0].data = self.config[parname]['file']
        
        file_handle = open(self.xmlconfigfile,"w")
        self.xmlconfig.writexml(file_handle)
        # sync buffers
        os.fsync(file_handle)
        file_handle.close()
        # and sync os to prevent dataloss on powerloss
        os.sync()
        
    def cancelAllParameter(self):
        for parname in self.config:
            if self.config[parname]['file'] is not None:
                self.config[parname]['value']=self.config[parname]['file']
            else:
                self.config[parname]['value']=self.config[parname]['default']
    
    def get(self, parameterName):
        if self.config[parameterName] is not None:
            if 'value' in self.config[parameterName]:
                return self.config[parameterName]['value']
            else:
                return self.config[parameterName]['default']
        else:
            log.error('config: couldnt find '+parameterName+' in config!')
            return None

    def getBool(self, parameterName):
        value = self.get(parameterName)
        if value is None:
            return None
        if value.lower() == 'true':
            return True
        if value == '1':
            return True
        return False
    
    def getFloat(self, parameterName):
        value = self.get(parameterName)
        if value is None:
            return None
        return float(value)
    
    def getInt(self, parameterName):
        value = self.get(parameterName)
        if value is None:
            return None
        return int(value)
    
    