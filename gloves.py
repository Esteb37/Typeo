#-----------------------------------Type-O--------------------------------------

#                           -------Project by------
#                           Montserrat Ulloa Barrón
#                           Sofía Carrión Cervantes
#                           Esteban Padilla Cerdio
#


#---------------------Controller class for the Type-O Gloves--------------------

#Communication to the Gloves will be through a serial port
import serial, time
import serial.tools.list_ports

#Main class
class Gloves:

    #Begin serial connection
    def start(self):
        self.port = self.findPort()
        if(self.port):
            self.arduino = serial.Serial(self.port, 9600)

    #Find where the gloves are connected
    def findPort(self):
        print("Looking for port...")
        comPorts = list(serial.tools.list_ports.comports())
        for port in comPorts:
            if("Arduino" in port.description):
                print("{0} found in {1}".format(port.description,port.device))
                self.vibrate("all")
                return str(port.device)
        print("No device found")
        return False

    #Activate the vibration in the specified finger
    def vibrate(self,finger):
        try:
            if(self.port):
                self.arduino.write(bytes(finger,"utf-8"))
        except:
            pass

if __name__ =="__main__":
    gloves = Gloves()
    gloves.start()
    gloves.vibrate(str(0))
