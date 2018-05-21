###############################################Python script to find the throughput of a CSS#################################
import time
import os
import subprocess


port_before = dict()
port_after  = dict()

class Port:

    def __init__(self, rx_pkts, rx_bytes, rx_drop, tx_pkts, tx_bytes, tx_drop):
        self.rx_pkts = rx_pkts
        self.rx_bytes = rx_bytes
        self.rx_drop = rx_drop

        self.tx_pkts = tx_pkts
        self.tx_bytes = tx_bytes
        self.tx_drop = tx_drop



def  createObject(port_before):

  output = subprocess.check_output("ovs-ofctl dump-ports-desc br-int",
shell=True)
  result = {}

  for row in output.split('\n'):
      if 'OFPST_PORT' in row:
          flag = 0;

      elif ': ' in row:
          key, value = row.split(': ')
          result[key]  = value.split(',');
          flag = 1;
      elif (flag == 1) :
          result[key].append(row);
          flag = 0;

  for key,row in result.iteritems():
      key_val  =  key.split(' ')[3];
      if key_val  is '':
          key_val = key.split(' ')[4];
      rx_packets = int(row[0].split('=')[1]);
      rx_bytes = int(row[1].split('=')[1]);
      rx_drop = int(row[2].split('=')[1]);
      rx_err = int(row[3].split('=')[1]);
      rx_frame = int(row[4].split('=')[1]);
      rx_over = int(row[5].split('=')[1]);
      rx_crc = int(row[6].split('=')[1]);
      tx_packets = int(row[7].split(',')[0].split('=')[1]);
      tx_bytes = int(row[7].split(',')[1].split('=')[1]);
      tx_drop = int(row[7].split(',')[2].split('=')[1]);

      print("key: %s rx_packets: %d  rx_bytes: %d rx_drop: %d
tx_packets: %d tx_bytes: %d tx_drop:
%d"%(key_val,rx_packets,rx_bytes,rx_drop,tx_packets,tx_bytes,tx_drop));
      port_before[key_val] = Port(rx_packets, rx_bytes, rx_drop,
tx_packets, tx_bytes, tx_drop);



def  findThroughput(port_before,port_after):

  diff_rx_pkts = 0;
  diff_rx_bytes = 0;
  diff_rx_drop = 0;
  diff_tx_pkts = 0;
  diff_tx_bytes = 0;
  diff_tx_drop = 0;

  output = subprocess.check_output("ovs-ofctl dump-ports-desc br-int",
shell=True)
  result = {}

  for row in output.split('\n'):
      if 'OFPST_PORT' in row:
          flag = 0;
      elif ': ' in row:
          key, value = row.split(': ')
          result[key]  = value.split(',');
          flag = 1;
      elif (flag == 1) :
          result[key].append(row);
          flag = 0;

  for key,row in result.iteritems():
      key_val  =  key.split(' ')[3];
      if key_val  is '':
          key_val = key.split(' ')[4];



      diff_rx_pkts  = diff_rx_pkts + (port_after[key_val].rx_pkts -
port_before[key_val].rx_pkts);
      diff_rx_bytes = diff_rx_bytes + (port_after[key_val].rx_bytes -
port_before[key_val].rx_bytes);
      diff_rx_drop = diff_rx_drop + (port_after[key_val].rx_drop -
port_before[key_val].rx_drop);
      diff_tx_pkts  = diff_tx_pkts + (port_after[key_val].tx_pkts -
port_before[key_val].tx_pkts);
      diff_tx_bytes = diff_tx_bytes + (port_after[key_val].tx_bytes -
port_before[key_val].tx_bytes);
      diff_tx_drop = diff_tx_drop + (port_after[key_val].tx_drop -
port_before[key_val].tx_drop);



  print ("In 10 sec rx_pkts:%d were sent" %diff_rx_pkts);
  print("In 10 sec rx_bytes:%d were sent" %(diff_rx_pkts));
  print("In 10 sec rx_dropped:%d" %(diff_rx_pkts));
  print("In 10 sec tx_pkts:%d were recieved" %(diff_tx_pkts));
  print("In 10 sec tx_bytes:%d were recieved"%(diff_tx_pkts));
  print("In 10 sec tx_dropped:%d" %(diff_tx_drop));






print ("############################Before sleep packet count
##########################################")
createObject(port_before);
print ("######################################################################")
print ("\n\n\nsleeping for 10 sec....")
time.sleep(10)
print ("\n\n\n############################After sleep packet count
########################################")
createObject(port_after);
print ("\n\n\n###############################Result#########################################")
findThroughput(port_before,port_before)

print ("#################################End#########################################")
