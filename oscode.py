import pyvisa
from matplotlib import pyplot as plt
import time

# start of Untitled
#points = 1000
#payload = ":WAVeform:POINts " + str(points)
rm = pyvisa.ResourceManager()
DSO5014A = rm.open_resource('USB0::0x0957::0x1765::MY48510618::0::INSTR')
number = 0
var = ''
nvar = ''
xorg = 0
xinc = 0

# Test--------------------
#DSO5014A.write(":ACQuire:POINts?")
#response = DSO5014A.read()
#print("Response = ", response)
# Test ends here ----------------------
DSO5014A.write(":CHANnel1:SCALe 5V")
DSO5014A.write(":TIMebase:RANGe .05")
DSO5014A.write(":TIMebase:SCALe?")
resp = DSO5014A.read()
time.sleep(5)
print("Per unit div is :", resp)
#DSO5014A.write(":ACQuire:TYPE HRESolution")
#print("Acquire Type set to HIgh Resolution")
#Execute the acquisition process.
DSO5014A.write("':DIGitize %s' % ('CHANNEL1')")                 #Starts and ends(?) the acquisition process.
#DSO5014A.write(":STOP")
print("Digitized Channel 1")
#DSO5014A.write(":WAVeform:POINts:MODE RAW")
DSO5014A.write(":WAVeform:POINts:MODE NORMal")
print("Waveform Points set to RAW")
#Formats the data read sent to the controller.
DSO5014A.write(":WAVeform:FORMat ASCii")                        #Converts data into integer values in floating point notation seperated by commas.
print("Waveform format set to ASCII")
#DSO5014A.write(":WAVeform:SOURce 2")                           #Selects channel 1. Command may not be needed.

DSO5014A.write(":WAVeform:POINts 1000")
DSO5014A.write(":WAVeform:POINts?")
time.sleep(5)
print("First sleep completed.")
resp = DSO5014A.read()
print("Number of data points: ", resp)

DSO5014A.write(":WAVeform:DATA?")
#print("Capturing data")
time.sleep(5)
print("First sleep completed")
hstr = DSO5014A.read()
#time.sleep(5)
print("Data read")
nhstr = hstr[11:]                                               #Filters out the header
print("Head removed from data")
nstring = nhstr.split(',')                                      #Seperates the variable into a matrix of floating point y-values.
print("Data converted into a matrix")
print("Writing data into file")
data = open('Data.txt', 'w')                                    #Record data into a file
data.write(hstr)
data.close()
print("Data recorded")

length = len(nstring)                                           #Number of the data values.
ymat = ['none']*length                                          #Set the length of the new matrix for the y-axis.
for i in range(0,length):                                       #Convert y-axis values from floating point to binary and enters into a new matrix.
    var = nstring[i]
    nvar = var.split('e')
    number = float(nvar[0])*(10**(float(nvar[1])))
    ymat[i] = number
print("Y matrix created")

print("Amplitude Array = ")
print(ymat)
print("Length of the Amplitude Array = ", len(ymat))

DSO5014A.write(":WAVeform:XORigin?")
print("X origin found")
time.sleep(5)
print("Second sleep done")
xorg = DSO5014A.read()
DSO5014A.write(":WAVeform:XINCrement?")
print("X increment found")
time.sleep(5)
print("Last sleep done")
xinc = DSO5014A.read()

nvar2 = xorg.split('E')
number2 = float(nvar2[0]) * (10 ** (float(nvar2[1])))          # Convert x-axis increment and origin from floating point to binary.
nvar3 = xinc.split('E')
number3 = float(nvar3[0]) * (10 ** (float(nvar3[1])))
print("X data converted to integers")

matx = ['none']*length
for i in range(0,length):
    matx[i] = number2 + (number3*i)
print("X matrix created")
print("time Array = ")
print(matx)
print("Length of the time Array = ", len(matx))

print("Plotting data")
plt.plot(matx,ymat)                                             #Plots time versus voltage.

plt.tight_layout()
plt.xlabel('Time')
plt.ylabel('Voltage')

plt.show()

DSO5014A.write("*RST")
DSO5014A.close()
rm.close()
