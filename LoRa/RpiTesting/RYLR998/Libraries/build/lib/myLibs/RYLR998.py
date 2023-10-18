from myLibs import Debug
import time


class RYLR998():


    def __init__(self, comDriver, buffer, name="None"):
            # Setup debug
            self.comDriver = comDriver
            self.buffer = buffer
            self.name = name
            self.pd = Debug.prettyDebug(name=self.name)
            self.pd.LOCAL_DEBUG = True
            self.pd.LOCAL_LOG = False
            self.pd.print("INIT")
            self.responseTime = 0.1
                



    def receiveCallback(self, data):
        data = self.decodeData(data)
        self.externalCallback(data)


    def receive(self, **kwargs):
        result = self.comDriver.receive(**kwargs)
        data = self.decodeData(result)
        return data

    def open(self, callback, RadioConfig, Buffer):
        self.comDriver = self.comDriver(self.receiveCallback, **RadioConfig)
        self.buffer = self.buffer (**Buffer, name=self.name)
        self.externalCallback = callback
        return self.comDriver.open()
    


    def configure(self, config):
        self.spreadingFactor = config["sf"]
        self.bandWidth = config["bw"]
        self.codingRate = config["cr"]
        self.preambleLength = config["pl"]
        #TODO: add maxPayload to config file or something like that
        #self.maxPayload = config["maxPayload"]
        self.maxPayload = 255        
        # Configure device

        configuration =  f"AT+PARAMETER={self.spreadingFactor},{self.bandWidth},{self.codingRate},12"
        
        if not self.sendAndValidate(configuration,"+OK"):
            self.pd.print("Sending configuration ended in error")
            return False
        return True
    

    def encodeData(self, data):
        if isinstance(data, str):
            data = (data + "\r\n").encode()
        elif isinstance(data, bytes):
            data = data + "\r\n".encode()
        else: 
             self.pd.print("Unable to encode data")
        return data
    

    def dataSendandValidate(self, data, address=0):
        
        dataLength = len(data)
        # send data 
        if not self.sendAndValidate(f"AT+SEND={address},{dataLength},{data}","+OK"):
            return False
            
        return True
    

    def commandSendAndValidate(self, data, validation, **kwargs):
        data = self.encodeData(data)
        validation = self.encodeData(validation)
        result = self.comDriver.sendAndValidate(data, validation, **kwargs)
        return result

    

    def sendAndValidate(self, data, validation, **kwargs):
        data = self.encodeData(data)
        validation = self.encodeData(validation)
        result = self.comDriver.sendAndValidate(data, validation, **kwargs)
        return result


    

    def decodeData(self, data):
            return data.decode().strip()
    


    