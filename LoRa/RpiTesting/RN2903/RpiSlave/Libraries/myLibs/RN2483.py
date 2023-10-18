import time
import math
from . import Debug

class RN2483:
    #------------------------------------------------------------------
    #   CLASS VARIABLES
    #------------------------------------------------------------------
    _MODULE=""
    _VERSION=""
    _EUI=""
    _MACPAUSE=""
    
    def __init__(self, comDriver, buffer, name="None"):
        # Setup debug
        self.comDriver = comDriver
        self.buffer = buffer
        self.name = name
        self.pd = Debug.prettyDebug(name=self.name)
        self.pd.LOCAL_DEBUG = False
        self.pd.LOCAL_LOG = False
        self.pd.print("INIT")
    
    def open(self, callback, RadioConfig, Buffer):
        self.comDriver = self.comDriver(self.receiveCallback, **RadioConfig)
        self.buffer = self.buffer (**Buffer, name=self.name)
        self.externalCallback = callback
        return self.comDriver.open()
    
    def close(self):
        return self.comDriver.close()
    
    def receive(self, **kwargs):
        result = self.comDriver.receive(**kwargs)
        data = self.decodeData(result)
        return data

    def commandSendAndReceive(self, data, **kwargs):
        data = self.encodeData(data)
        result = self.comDriver.sendAndReceive(data, **kwargs)
        data = self.decodeData(result)
        return data
    
    def commandSendAndValidate(self, data, validation, **kwargs):
        data = self.encodeData(data)
        validation = self.encodeData(validation)
        result = self.comDriver.sendAndValidate(data, validation, **kwargs)
        return result
    
    def dataSend(self, data):
        MaxDataSize = self.maxPayload - len(self._EUI) - 5   # 5 = 2 bytes for the packageCount 1 byte for '-" and 2 bytes for currentpackage
        dataChunks = [data[i:i+MaxDataSize] for i in range(0, len(data), MaxDataSize)]
        packageCount = len(dataChunks)

        # send data packages
        for i, chunk in enumerate(dataChunks):
            data = self._EUI.encode() + packageCount.to_bytes(2, 'big') + "-".encode() + (i+1).to_bytes(2, 'big') + chunk.encode()
            result = self.dataSendAndValidate(f"radio tx {data.hex()}","radio_tx_ok",self.transmitTime)
            if not result:
                return False
        return True
            
    def dataSendAndValidate(self, data, validation, loopTime):
        self.comDriver.stopThreads()
        start_time = time.time()
        while time.time() - start_time < loopTime:
            if self.commandSendAndValidate(data, "ok"):
                start_time2 = time.time()
                while time.time() - start_time2 < loopTime:
                    try:
                        result = self.receive()
                    except Exception:
                        result = ""
                    if result == validation:
                        self.comDriver.resumeThreads()
                        return True
            time.sleep(self.transmitTime/10)
        self.comDriver.resumeThreads()
        return False
    
    def sendToBuffer(self, data, **kwargs):
        self.data = data + "\r\n"
        return self.comDriver.sendToBuffer(self.data, **kwargs)
    
    def getDeviceInfo(self):
        # Get device information from device
        self._MODULE, self._VERSION = self.commandSendAndReceive("sys get ver").split(maxsplit=2)[:2]
        self._EUI = self.commandSendAndReceive("sys get hweui")
        return self._MODULE, self._VERSION, self._EUI
    
    def factoryReset(self):
        self._MODULE, self._VERSION = self.commandSendAndReceive("sys factoryRESET",timeout=5.0).split(maxsplit=2)[:2]
        return self._MODULE, self._VERSION
    
    def encodeData(self, data):
        if isinstance(data, str):
            data = (data + "\r\n").encode()
        elif isinstance(data, bytes):
            data = data + "\r\n".encode()
        return data
    
    def decodeData(self, data):
        return data.decode().strip()
    
    def timeOnAir(self, spreadfactor, bandwidth, codingrate, header, optimization, payload_size, preamble_length):
        # Convert input parameters to appropriate values
        sf = int(spreadfactor[2:])
        bw = bandwidth * 1000
        cr_num, cr_denom = map(int, codingrate.split('/'))
        h = 1 if header.lower() == "on" else 0
        opt = 1 if optimization.lower() == "on" else 0
        # Calculate symbol duration
        tsym = (2 ** sf) / bw
        # Calculate number of preamble symbols
        preamble_symbols = preamble_length + 4.25
        # Calculate preamble duration
        preamble_duration = tsym * preamble_symbols
        # Calculate number of payload symbols
        payload_symbols = 8 + math.ceil(
            (
                (8 * payload_size - 4 * sf + 28 + 16 - 20 * h + 8 * opt)
                / (4 * (sf - 2 * opt))
            )
        ) * (cr_num + 4)
        # Calculate payload duration
        payload_duration = tsym * payload_symbols
        # Calculate total airtime (LoRa packet duration)
        airtime = preamble_duration + payload_duration
        return airtime
    
    def configure(self):
        raise NotImplementedError
    
    def receiveCallback(self, data):
        raise NotImplementedError
    
class RN2483_Radio(RN2483):
    def __init__(self, comDriver, buffer, name="None"):
        super().__init__(comDriver, buffer,name)
    
    def configure(self, config):
        self.mode = config['mode']
        self.frequency = config['frequency']
        self.spreadingFactor = config["spreadingFactor"]
        self.bandWidth = config["bandwidth"]
        self.codingRate = config["codingRate"]
        self.power = config["power"]
        self.maxPayload = config["maxPayload"]
        self.transmitTime = self.timeOnAir(self.spreadingFactor, self.bandWidth, self.codingRate, "off", "off", self.maxPayload, 8)
        
        # Configure device
        configuration = [
            f"radio set mod {self.mode}",
            f"radio set freq {self.frequency}",
            f"radio set sf {self.spreadingFactor}",
            f"radio set bw {self.bandWidth}",
            f"radio set cr {self.codingRate}",
            f"radio set pwr {self.power}",
            "radio set wdt 0"
        ]
        
        self._MACPAUSE = self.commandSendAndReceive("mac pause")
        for line in configuration:
            if not self.commandSendAndValidate(line,"ok"):
                self.pd.print(f"Config: Device configutation '{line}' ended in error")
                return False
        return True
    
    def receiveCallback(self, data):
        data = self.decodeData(data)
        self.externalCallback(data)
        
    def startReceive(self):
        if self.commandSendAndValidate("radio rx 0","ok"):
            time.sleep(0.1)
            return True
        return False
        
    def stopReceive(self):
        if self.commandSendAndValidate("radio rxstop","ok"):
            time.sleep(0.1)
            return True
        return False
        
class RN2483_Lora(RN2483):
    def __init__(self, config, comDriver, buffer, name="None"):
        super().__init__(config, comDriver,buffer,name)
    
    def configure(self):
        print("Configure")
    
    def receiveCallback(self, data):
        self.externalCallback(data)