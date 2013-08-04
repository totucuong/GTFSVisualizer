#!/usr/bin/python -tt
#==============================================================================
# This scripts reads trips.txt stops.txt checkins data to generate update stream
# data for simulation stored in updatestream_checkins_filename.txt
# In ordre to create a stop graph (a normal transit network graph like we see on
# any website for users. We need to parse three files: stops.txt, routes.txt and
# stop_times.txt.
# Usage: create_stop_graph gtfs_dir
# Author: To Tu Cuong
# Email: to.cuong@fu-berlin.de
#==============================================================================
import sys
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import array

def main():
  if len(sys.argv) != 2:
    print 'usage: ./create_stop_graph gtfs_dir'
    sys.exit(1)
  # parsing stops.txt
  stopsF = open(sys.argv[1] + '/stops.txt', 'rU')
  stops = []
  stopsLat = {}
  stopsLon = {}
  headers = stopsF.readline().split(',')
  # index column name in stops.txt
  headerIndex = {}
  for i in range(0, len(headers)):
    headerIndex[headers[i]] = i
  for stop in stopsF:
    fields = stop.split(',')
    stops.append(fields[0])
    stopsLat[fields[0]] = fields[headerIndex['stop_lat']]
    stopsLon[fields[0]] = fields[headerIndex['stop_lon']]
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
  # create a stop graph
  mdg = nx.MultiDiGraph()
  stopIdToIndex = {}
  # add stops to the graph
  for stop in stops:
    mdg.add_node(stop)
    mdg.node[stop]['lat'] = stopsLat[stop]
    mdg.node[stop]['lon'] = stopsLon[stop]

  # add connection between stops
  for k, v in tripIdToStopSq.items():
    for i in range(0, len(v) -1):
      if not mdg.has_edge(v[i], v[i+1]):
        mdg.add_edge(v[i], v[i+1])
  print 'number of nodes: ', mdg.number_of_nodes()
  print 'number of edges: ', mdg.number_of_edges()
  #for degree in nx.degree_histogram(mdg):
  # print degree, ' ',
  # draw stop graph
  print 'drawing..'
  # node size is propotional to its degree
  nodesize = [mdg.degree(v)*10 for v in mdg.nodes()]
  # layout according to (lat,lon) position of stops
  #pos=nx.spring_layout(mdg, iterations=20)
  pos = {}
  for node in mdg.nodes():
    a = array.array('f')
    a.append(float(mdg.node[node]['lat']))
    a.append(float(mdg.node[node]['lon']))
    pos[node] = a
    #pos[node][0] = mdg.node[node]['lat']
    #pos[node][1] = mdg.node[node]['lon']

  #print pos
  plt.figure(figsize=(8,8))
  nx.draw_networkx_nodes(mdg,pos,node_size=nodesize, node_color='r', alpha=0.4)
  nx.draw_networkx_edges(mdg,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
  #nx.draw_networkx_labels(mdg,pos,fontsize=9)
  plt.show()
  #plt.savefig("stopgraph.png");


if __name__ == '__main__':
  main()


  #for stop in stops:
  #  print stop
  #print 'there are ', len(stops)

  #for trip in trips:
  #  print trip
  #print 'there are ', len(trips), ' trips'

    #print 'drawing..'
  #nx.draw_spring(mdg)
  #print 'saving....'
  #plt.show()
  #plt.savefig("stopgraph.png");
  # display on google map
  #for component in nx.strongly_connected_components(mdg):
 #   if len(component) > 400:
 #     for v in component:
 #       print v, ' ',
  # generate all simple paths between all origin and terminus bus
 #for path in nx.all_simple_paths(mdg, '4213', '6793' , cutoff=None):
 #   print path, 'and length: ', len(path)

 # degree analysis