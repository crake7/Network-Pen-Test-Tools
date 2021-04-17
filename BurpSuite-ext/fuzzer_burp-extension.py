from burp import IBurpExtender                          # Mandatory for every extension
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator 

from java.util import List, ArrayList

import random

# Make sure to check the BURP API documentation to understand the mandatory classes
# and expand the capability of the fuzzer. 
# For additional info, check the Extender, APIs tab. 

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    ''' This class extends the Extender and Payload Generator Factory classes '''

    def registerExtenderCallbacks(self, callbacks):
        # Get invoked when extension is loaded 
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()

        # Registers our class so the Intruder tool can generate the payloads
        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return "Da Payload Generator"

    def createNewInstance(self, attack):
        # Returns an instance of the Intruder Payload Generator class
        return Fuzzer(self, attack)

class Fuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender      = extender
        self._helpers       = extender._helpers
        self._attack        = attack
        self.max_payloads   = 10
        self.num_iterations = 0

        return  

    def hasMorePayloads(self):
        # Could also always be True
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):
        ''' Receives the  original HTTP payload and fuzzes it. '''

        # convert the byte array into a string
        payload = "".join(chr(x) for x in current_payload)

        # Call out mutator to fuzz the POST
        payload = self.mutate_payload(payload)

        self.num_iterations += 1

        return payload
    
    def reset(self):
        ''' This method will be invoked when an attack uses the same payload generator for more
        than one payload position, for example in a snipper attack'''
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        # Pick a simple mutator or even call an external script
        picker = random.randint(1,3)

        # select a random offser in the payload to mutate
        offset = random.randint(0, len(original_payload)-1)
        
        front, back = original_payload[:offset], original_payload[offset:]

        # random offset insert a SQLi attemot
        if picker == 1:
            front += "'"
        
        elif picker == 2:
            fron += "<script>alert('xss');</script>"
        
        # repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length =  random.randint(0, len(back)-1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
        
        return front + back 

