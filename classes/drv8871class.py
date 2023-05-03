from machine import Pin, PWM
import time

class drv8871:
    def __init__(self, motorPin1= 0, motorPin2= 1, pwmRate=10000, scaler = False, minScaler = 0 , maxScaler = 100):
        
        #	need to add scaling function for active range
        
        self.motorPWM1 = PWM(Pin(motorPin1))
        self.motorPWM1.freq(pwmRate)

        self.motorPWM2 = PWM(Pin(motorPin2))
        self.motorPWM2.freq(pwmRate)

        self.motorPWM1.duty_u16(0)
        self.motorPWM2.duty_u16(0)
        
        self.motScale = scaler
        self.minScale = minScaler
        self.maxScale = maxScaler
        
    def speed(self, rate):

        #	rate = -1 to +1
              
        self.lastRate = rate
        
        #	lets scale it to motors operational range
       
        if self.motScale:
            self.theRate = drv8871.scaling(self,rate)
        else:
            self.theRate = self.lastRate

        #	ok we have scaled it so lets convert to PWM duty cycle

        self.duty = min(max(int(2**16 * abs(self.theRate)), 0), 65535)
        
        if self.lastRate < 0:
            self.duty1 = self.duty
            self.duty2 = 0
        else:
            self.duty1 = 0
            self.duty2 = self.duty
            
        self.motorPWM1.duty_u16(self.duty1)
        self.motorPWM2.duty_u16(self.duty2)

    def stop(self):
       
        self.lastRate = 0
        self.duty1 	  = 0
        self.duty2 	  = 0
        
        self.motorPWM1.duty_u16(self.duty1)
        self.motorPWM2.duty_u16(self.duty2)

    def currentSpeed(self):

        return self.lastRate
        
    def scaler(self, scaler = True):

        self.motScale = scaler

        return self.motScale
    
    def scaling(self, rate):

        workRate = abs(rate)
            
        scaleOffset = self.minScale
        scaleFactor = (self.maxScale - self.minScale)
        
        tOffset   = scaleOffset      
        tFactored = workRate * scaleFactor

        newRate     = tOffset +  tFactored
        
        if rate < 0:
                newRate = newRate * -1
    
        return newRate
                      
