#!/usr/bin/env python

import mmap, os

# there seems to be a problem with this (and devmem2) where if a address
# is too close to a multiple of the page size (say 4095) than a portion of the
# data is blank in this case, and random for devmem2

MAP_MASK = mmap.PAGESIZE - 1

def value_to_hex(value):
  return '0x%08x' % value

def read_addr(mem, addr, length):
  global MAP_MASK
  mem.seek(addr & MAP_MASK)
  print mem.size()
  s = mem.read(length)
  val = 0x0
  for i in range(len(s)):
    val |= ord(s[i]) << (i * 8)
  return val

def write_addr(mem, addr, value, length):
  global MAP_MASK
  mem.seek(addr & MAP_MASK)
  valueString = ""
  for i in range(length):
    valueString += chr((value >> (i*8)) & 0xff)
  mem.write(valueString)

def read(addr, length=4):
  f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
  mem = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE,offset=addr & ~MAP_MASK)
  print mem, hex(addr)
  val = read_addr(mem, addr, length)
  mem.close()
  os.close(f)
  return val

def write(addr, value, mask=0xffffffff, length=4, ):
  f = os.open("/dev/mem", os.O_RDWR)
  #f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
  print "/dev/mem opened"
  mem = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=addr & ~MAP_MASK)
  print "mmap made"
  # read old value
  readValue = read_addr(mem, addr, length)
  print "value:",value_to_hex(readValue),"read"
  # apply mask
  maskedValue = (value & mask) | (readValue & ~mask)
  # write new value
  write_addr(mem, addr, maskedValue, length)
  print "value:",value_to_hex(maskedValue),"written"
  #print "flush mem:",mem.flush(addr & MAP_MASK, length)
  #print "flush mem:",mem.flush()
  # read new value
  newValue = read_addr(mem, addr, length)
  print "value:",value_to_hex(newValue),"read"
  mem.close()
  os.close(f)
  return newValue

#def write_value(addr, value, length=4, mask=0xffffffff):
#  f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
#  m = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=addr & ~MAP_MASK)
#  # read current value
#  m.seek(addr & MAP_MASK)
#  r = 0x0
#  for i in range(length):
#    r |= ord(m.read_byte()) << (i * 8)
#  # write value to register
#  m.seek(addr & MAP_MASK)
#  w = value | (r & ~mask)
#  sw = ""
#  for i in range(length):
#    sw += chr((w >> (i*8)) & 0xff)
#  m.write(sw)
#  # read new value
#  m.seek(addr & MAP_MASK)
#  r = 0x0
#  for i in range(length):
#    r |= ord(m.read_byte()) << (i * 8)
#  # cleanup
#  m.close()
#  os.close(f)
#  return r

#def read_addr(addr,length=4):
#  f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
#  m = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE,offset=addr & ~MAP_MASK)
#  #r = m[addr]
#  m.seek(addr & MAP_MASK)
#  #r = m.read_byte()
#  r = 0x0
#  for i in range(length):
#    r |= ord(m.read_byte()) << (i * 8)
#  #r = m.read(length)
#  m.close()
#  os.close(f)
#  return r

#def convert_value(value):
#  newValue = 0
#  for i in range(len(value)):
#    newValue |= ord(value[i]) << (i * 8)
#  return newValue

if __name__ == "__main__":
  #print read_addr(0x1fffffff).encode("hex")
  #print_value(read_addr(0x48004a40))
  print value_to_hex(read(0x48002178))
  print value_to_hex(read(0x4808802c))
