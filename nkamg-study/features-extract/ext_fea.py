import numpy as np
import pandas as pd
import sys, getopt, time
from numpy import *

MIN_FLOWS = 10 # Each subtrace must has more than MIN_FLOWS flows

def entropy(count): 
    sum=0
    for data in count:
        sum+=data
    for data in count:
        data=data/float(sum) # coerce to float and normalize
        #print data
    res = []
    for d in count:
        if(d != 0.0):
            res.append(d)
    entr=0
    for data in res:
        entr+=data*np.log2(data)
    entr=-entr
    #entr=-sum(res*np.log2(res))
    return entr

def __ext_feat(ifile):

    df = pd.DataFrame(pd.read_csv(ifile, low_memory=False))
    print list(df.columns.values)
    print "Number of netflows: {}".format(len(df))
    
    #['StartTime', 'Dur', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr', 'Dport', 'State', 'sTos', 'dTos', 'TotPkts', 'TotBytes', 'SrcBytes', 'Label'
    
    #test entropy
    '''
    SrcAddrCount=[]
    grouped=df.groupby('SrcAddr')
    for k,v in grouped:
        SrcAddrCount.append(len(v.index))
    en_SrcAddr=entropy(SrcAddrCount)
    print "en_SrcAddr:",en_SrcAddr,"\n"

    #Number of netflows: 17012
    #en_SrcAddr: -113003.984374 
    #maybe there exists some questions?
    '''

    ###MINDS
    '''
    1. MINDS
        - the number of NetFlows from the same source IP address as the evaluated NetFlow
        - the number of NetFlows toward the same destination host
        - the number of NetFlows toward the same destination host from the same source port
        - the number of NetFlows toward the same destination port from the same source host  
   
    grouped1=df.groupby('SrcAddr')
    for k,v in grouped1:
        print "SrcAddr:", k, "number:",len(v.index) 

    grouped2=df.groupby('DstAddr')
    for k,v in grouped2:
        print "DstAddr:", k, "number:",len(v.index) 

    grouped3=df.groupby(['Sport','DstAddr'])
    for k,v in grouped3:
        print "Sport:", k[0], "DstAddr:", k[1], "number:",len(v.index) 

    grouped4=df.groupby(['SrcAddr','Dport'])
    for k,v in grouped4:
        print "SrcAddr:", k[0], "Dport:", k[1], "number:",len(v.index) 
    '''


    ### Xu
    '''
    2. Xu
    the context of each NetFlow to be evaluated is created with all the NetFlows coming from the same source IP address.
        - the normalized entropy of the source port
        - the normalized entropy of the destination ports
        - the normalized entropy of the destination IP addresses
    The distance between the contexts of two NetFlows is computed as the difference between the three normalized entropies, combined as the sum of their squares. 
    

    grouped=df.groupby('SrcAddr')
    for k,v in grouped:
        print "------------------------------------------------"
        print "SrcAddr:", k, "number:",len(v.index) 

        grouped1=v.groupby(v['Sport'])
        sPortCount=[]
        for k,v in grouped1:
            sPortCount.append(len(v.index))  
        en_sPort=entropy(sPortCount)
        print "en_sPort:",en_sPort

        grouped2=v.groupby(v['Dport'])
        dPortCount=[]
        for k,v in grouped2:
            dPortCount.append(len(v.index))  
        en_dPort=entropy(dPortCount)
        print "en_dPort",en_dPort

        grouped3=v.groupby(v['DstAddr'])
        DstAddrCount=[]
        for k,v in grouped3:
            DstAddrCount.append(len(v.index))
        en_DstAddr=entropy(DstAddrCount)
        print "en_DstAddr",en_DstAddr
    '''

    ### Lakhina Volume
    '''
    3. Lakhina Volume
        for each source IP address:
        - the number of NetFlows
        - number of bytes
        - number of packets from the source IP address
    
    grouped=df.groupby('SrcAddr')
    for k,v in grouped:
        numNetFlows=len(v.index)
        print "SrcAddr:",k,"Number of netflows: {}".format(numNetFlows)
    TotBytes=grouped['TotBytes']
    print "number of total bytes:",TotBytes.sum()
    TotPkts=grouped['TotPkts']
    print "number of total packets:",TotPkts.sum()
    SrcBytes=grouped['SrcBytes']
    print "number of SrcBytes:",SrcBytes.sum()
    '''

    ### Lakhina Entropy
    '''  
    4. Lakhina Entropy
        for each source IP address:
        - the entropies of destination IP addresses
        - the entropies of destination ports
        - the entropies of source ports
    see 2.Xu
    '''

    ### TAPS
    '''
    5. TAPS
    The algorithm only considers the traffic sources that created at least one single-packet NetFlow during a particular observation period.
    - number of destination IP addresses
    - number of destination ports 
    - the entropy of the NetFlow size measured in number of packets.
    '''
    grouped1=df.groupby('DstAddr')
    print len(grouped1) 
    grouped2=df.groupby('Dport')
    print len(grouped2)
    grouped3=df.groupby(df['TotPkts'])
    TotPktsCount=[]
    for k,v in grouped3:
        TotPktsCount.append(len(v.index))
    en_TotPkts=entropy(TotPktsCount)
    print "en_TotPkts",en_TotPkts


    ### KGB
    '''
    It uses the same features as Lakhina Entropy detector described above. see 4.Lakhina Entropy
    '''

    ### Flags
    '''
    uses the same detection method as the KGB detector. The only difference is in the input feature vector. 
    The feature vector of the Flags detector is determined by the histogram of the TCP Flags of all the NetFlows with the same IP address. 
    This detector is looking for a sequence or a combination of anomalous TCP flags.
    '''

#这里没有输出到文件中，所以不会生成outfile
def main(argv):
   ifile = ''
   ofile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'ext_bf_feat.py -i <input_binetflow_file> -o <output_csv_file>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'ext_bf_faet.py -i <input_binetflow_file> -o <output_csv_file>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         ifile = arg
      elif opt in ("-o", "--ofile"):
         ofile = arg
   print 'Input file is "', ifile, '"'
   print 'Output file is "', ofile, '"'
   __ext_feat(ifile, ofile)

if __name__ == "__main__":
   if len(sys.argv) < 5:
      print 'ext_bf_feat.py -i <input_binetflow_file> -o <output_csv_file>'
      sys.exit()

   main(sys.argv[1:])




