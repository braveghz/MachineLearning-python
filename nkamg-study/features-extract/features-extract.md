## 数据包解析

主要是 `.pcap` 解析为 `.csv`

### 安装libpcap

源代码 [网址](http://www.tcpdump.org/) 下载 `libpcap-x.x.x.tar.gz`
```s
braveghz@braveghz:~$ cd Downloads/
braveghz@braveghz:~/Downloads$ tar -zxvf libpcap-1.8.1.tar.gz 
braveghz@braveghz:~/Downloads$ cd libpcap-1.8.1/
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ sudo apt-get install flex
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ sudo apt-get install bison
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ ./configure
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ make 
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ make install 
```

### 安装tshark
```s
braveghz@braveghz:~/Downloads/libpcap-1.8.1$ sudo apt-get install tshark
```

查看版本（检查是否安装成功喽
```s
braveghz@braveghz:~$ tshark -v
TShark 1.10.6 (v1.10.6 from master-1.10)
.......
```

运行`tshark -D`会提示`There are no interfaces on which a capture can be done`

then--解决办法：运行以下代码（其实我是瞎搞的
```s
$ sudo apt-get install wireshark
$ sudo dpkg-reconfigure wireshark-common 
$ sudo usermod -a -G wireshark $USER
$ gnome-session-quit --logout --no-prompt
```

结果ok
```s
braveghz@braveghz:~$ tshark -D
1. eth0
2. nflog
3. nfqueue
4. any
5. lo (Loopback)
```

### tshark使用

捕获500个网络数据包（`-c 500`）并保存到1.pcap（`-w 1.pcap`）：
```s
braveghz@braveghz:~/MachineLearning-python/nkamg-study$ tshark -c 500 -w 1.pcap
Capturing on 'eth0'
500 
```
用wireshark打开，长下面这样

![](https://github.com/braveghz/MachineLearning-python/blob/master/nkamg-study/features-extract/images/1.png)

可以看到信息：`no`/ `time`/ `source`/ `destination`/ `protocol`/ `length`/ `info`...实际上的pcap文件信息应该多得多

先转化为`csv`文件试一下,比如说我要提取数据包的`mac`/`ip`/`tcp/udp`等信息
```s
tshark -r 1.pcap -T fields -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -E header=y -E separator=, -E quote=d -E occurrence=f >1.csv
```
ok

![](https://github.com/braveghz/MachineLearning-python/blob/master/nkamg-study/features-extract/images/2.png)

## 参考
[Using tshark to Watch and Inspect Network Traffic](http://www.linuxjournal.com/content/using-tshark-watch-and-inspect-network-traffic)

---

## 特征提取

### NetFlows Files

- Start Time
- End Time
- Duration
- Source IP address 
- Source Port
- Direction
- Destination IP address
- Destination Port
- State
- SToS
- Total Packets
- Total Bytes

### Features

@An empirical comparison of botnet detection methods

1. MINDS

     - the number of NetFlows from the same source IP address as the evaluated NetFlow
     - the number of NetFlows toward the same destination host
     - the number of NetFlows toward the same destination host from the same source port
     - the number of NetFlows toward the same destination port from the same source host  

    ```py
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
    ```

2. Xu

the context of each NetFlow to be evaluated is created with all the NetFlows coming from the same source IP address.
    - the normalized entropy of the source port
    - the normalized entropy of the destination ports
    - the normalized entropy of the destination IP addresses

The distance between the contexts of two NetFlows is computed as the difference between the three normalized entropies, combined as the sum of their squares. 
    
    ```py
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
    ```

3. Lakhina Volume

    for each source IP address:
    - the number of NetFlows
    - number of bytes
    - number of packets from the source IP address

    ```py    
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
    ```

4. Lakhina Entropy

    for each source IP address:
    - the entropies of destination IP addresses
    - the entropies of destination ports
    - the entropies of source ports

    see 2.Xu


5. TAPS

    The algorithm only considers the traffic sources that created at least one single-packet NetFlow during a particular observation period.
    - number of destination IP addresses
    - number of destination ports 
    - the entropy of the NetFlow size measured in number of packets.

    ```py
    grouped1=df.groupby('DstAddr')
    print len(grouped1) 
    grouped2=df.groupby('Dport')
    print len(grouped2)
    grouped3=df.groupby(df['TotPkts'])
    DstAddrCount=[]
    for k,v in grouped3:
        DstAddrCount.append(len(v.index))
    en_DstAddr=entropy(DstAddrCount)
    print "en_DstAddr",en_DstAddr
    ```   

6. KGB

    It uses the same features as Lakhina Entropy detector described above. see 4.Lakhina Entropy

7. Flags

    uses the same detection method as the KGB detector. The only difference is in the input feature vector.
    
    The feature vector of the Flags detector is determined by the histogram of the TCP Flags of all the NetFlows with the same IP address. 

    This detector is looking for a sequence or a combination of anomalous TCP flags.

---

求熵值函数如下---当然我写的是那个通俗易懂的那个

```py
def entropy(counts):
    '''Compute entropy.'''
    ps = counts/float(sum(counts))  # coerce to float and normalize
    ps = ps[nonzero(ps)]            # toss out zeros
    H = -sum(ps * numpy.log2(ps))   # compute entropy
    return H

#我的count是一个list
def entropy(count): 
    sum=0
    for data in count:
        sum+=data
    for data in count:
        data=data/float(sum) 
    res = []
    for d in count:
        if(d != 0.0):
            res.append(d)
    entr=0
    for data in res:
        entr+=data*np.log2(data)
    entr=-entr
    return entr
```
---

CTU13的二进制pcap文件使用Argus工具转换为netflow文件

