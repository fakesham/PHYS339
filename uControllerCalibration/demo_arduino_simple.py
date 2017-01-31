import arduino
import time

print "Opening Arduino ... this might take a moment"
a = arduino.arduino(debug=0)
print "I will read a number from you,\nsend it to PCM output pin 10,\nand report value read from ADC A0"
print "I will exit on negative input\n"
while 1 > 0 :
  str = raw_input("enter a number between 0 and 255: ")
  if 0 == len(str) :
    print "That is not a number!"
    continue
  out_value = int(str)
  if 0 > out_value :
    print "Exiting due to negative input"
    break
  if 255 < out_value :
    print "Number must be in range 0...255"
    break
  a.analogWrite(10,out_value)
  print "Sent %d to pin 10" % out_value
  print "pausing to allow signal to settle"
  time.sleep(1)
  in_value = a.analogRead(0)
  print "Read %d from ADC A0" % in_value
