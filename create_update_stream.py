#!/usr/bin/python -tt
#==============================================================================
# This scripts reads trips.txt stops.txt checkins data to generate update stream
# data for simulation stored in updatestream_checkins_filename.txt
# Usage: create_update_stream gtfs_dir checkins_filename
# Author: To Tu Cuong
# Email: to.cuong@fu-berlin.de
#==============================================================================
import sys
import os
import random
import networkx as nx
import matplotlib.pyplot as plt


def main():
  if len(sys.argv) != 3:
    print 'usage: ./create_update_stream gtfs_dir checkins_filename'
    sys.exit(1)
  # parsing stops.txt
  stopsF = open(sys.argv[1] + '/stops.txt', 'rU')
  stops = []
  stopsF.readline() # skip the first line
  for stop in stopsF:
    fields = stop.split(',')
    stops.append(fields[0])
  print 'there are ', len(stops), 'stops'
  # parsing trips.txt
  tripsF = open(sys.argv[1] + '/trips.txt', 'rU')
  trips = []
  tripsF.readline() # skip the first line
  for trip in tripsF:
    fields = trip.split(',')
    trips.append(fields[2])
  print 'there are ', len(trips), ' trips'
  # parsing stop_times.txt
  stop_timesF = open(sys.argv[1] + 'stop_times.txt', 'rU')
  tripIdToStopSq = {}
  stopSq = []
  tripId = ''
  for segment in stop_timesF:
    fields = segment.split(',')
    if tripId == fields[0]:
      stopSq.append(fields[3])
    elif tripId != '': # new trip encountered, save the old trip
      #print 'add a new trip ', tripId
      tripIdToStopSq[tripId] = stopSq
      stopSq = []
      tripId = fields[0]
      stopSq.append(fields[3])
    else:
      tripId = fields[0]
      stopSq.append(fields[3])
  print 'there are ', len(tripIdToStopSq.keys()), 'trips'
  stop_timesF.close()
  #parsing checkins data
  checkinsF = open(sys.argv[2], 'rU')
  #f2 = open(os.path.dirname(f.name) +'/san_francisco_' + sys.argv[2] + '_' + \
  updateF = open('update.txt', 'w')
  updateF.write('[stopId]\t[tripId]\t' + checkinsF.readline())
  for checkin in checkinsF:
    # randomly pick a trip to update
    tripId = trips[random.randint(0, len(trips)-1)]
    # randomly pick a stop in the above trip to update
    stopId = tripIdToStopSq[tripId][random.randint(0, len(tripIdToStopSq[tripId])-1)]
    updateF.write(stopId + '\t' + tripId + '\t' + checkin)
  stopsF.close()
  tripsF.close()
  updateF.close()
if __name__ == '__main__':
  main()
