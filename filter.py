#!/usr/bin/python -tt
# GPS coordinate (lat, lon)
# San Francisco bounding box: bottomLeft(37.645585, -122.585449)
# and topRight(37.804266, -122.372589)

import sys
import os
import re

def inside(point, bottomLeft, topRight):
 if (point[0] >= bottomLeft[0] and point[0] <= topRight[0]
   and point[1] >= bottomLeft[1] and point[1] <= topRight[1]):
   return True
 return False

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
  if len(sys.argv) != 7:
    print 'usage: ./filter.py filename date(yyyymmdd) \
    lat_bottom_left lon_bottom_left lat_top_right lon_top_right'
    sys.exit(1)
  filename = sys.argv[1]
  # Bounding box for San Francisco area
  bottomLeft = (float(sys.argv[3]), float(sys.argv[4]))
  topRight = (float(sys.argv[5]), float(sys.argv[6]))
  # Parsing file for checkin in San Francisco
  f = open(filename, 'rU')
  f2 = open(os.path.dirname(f.name) +'/san_francisco_' + sys.argv[2] + '_' + \
   os.path.basename(f.name), 'w')
  f2.write('[user]\t[check-in time]\t[latitude]\t[longitude]\t[location id]\n')
  count = 0
  countS = 0
  for line in f:
    # visual update
    count += 1
    if count % 100000 == 0:
      print count
    # process each line
    fields = line.split()
    # extract date and time
    match = re.search(r'([\w-]+)T([\w:]+)Z', fields[1])
    date = sys.argv[2]
    if (match.group(1) == date):
      location = (float(fields[2]), float(fields[3]))
      if inside(location, bottomLeft, topRight):
        outstr = fields[0] + '\t' + match.group(2) + '\t' + fields[2] + '\t' + \
        fields[3] + '\t' + fields[4] + '\n'
        f2.write(outstr)
        countS += 1
  print 'There are ', countS, 'check-ins on ', date, ' in ' + \
   str(bottomLeft[0]) + ' ' + str(bottomLeft[1]) + ' ' + str(topRight[0])  + \
   ' ' +  str(topRight[1])
  f.close()
  f2.close()
  sys.exit(1)

if __name__ == '__main__':
  main()
