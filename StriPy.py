#!/usr/bin/python
import optparse
import urllib3
import os
import threading
import time
from termcolor import colored


item = []    


def main():
    global outPut 
    print (colored( str(open("Menu.txt", "r").read()), "red")   )
######
    start = time.perf_counter()
    parse = optparse.OptionParser("Usage: StriPy -i <input>")
    parse.add_option('-i',     dest='inp', type='string',       help='Target URL')
    parse.add_option('-o',     dest='out', type='string',       help='Target URL')
    (options, args) = parse.parse_args()
    inp = options.inp
    out = options.out
    outPut = str(out) + "/" + "Results.txt"
#####
    if(inp != None ):
        
        makeList(inp)
    
    else:
        os.system("python3 sublisterHttpAdder.py -h ")
    
    
    finished = time.perf_counter()
    print(f"Finished in {round(finished-start, 2 ) } seconds")



def makeList(inp):   
    for line in  open(inp, 'r').readlines():
        item.append(line.strip('\n')  )  
       
    threads(0)


def threads(count):
    while count != len(item):
        
        thred = []
        safty = len(item)
        i = 0
        if  (500 < safty):
            safty = 500
                
        for _ in  range(safty) :
            t = threading.Thread(target= hostResolve,args=[count])  
            count += 1
            
            i += 1
            #print(str(t))
            t.start()
            thred.append(t)
        
        for thre in thred:
            thre.join()
         
 
def hostResolve(count2):
        http =  urllib3.PoolManager()
        
        try:
            r = http.request('GET', "https://" + item[count2], timeout=3).status   
            s = http.request('GET', "http://" + item[count2], timeout=3).status   
            if(r == 200):
              print(colored(f"[*] https://{item[count2]} [{r}]", "green")  )   
              open(outPut, 'a').write(f"https://{item[count2]}  [{r}]\n")
              
            if(s == 200):
                print(colored(f"[*] http://{item[count2]} [{r}]", "green")  )
                open(outPut, 'a').write(f"http://{item[count2]}  [{r}]\n")
            
            else:
                print(colored(f"[!!]Removed Page Bad [{r}]", "red")  )
                r.close()
           
            print(f"Inprogress ",end="\r") 
        except:
           pass
        

    


if __name__ == "__main__":
    main()
