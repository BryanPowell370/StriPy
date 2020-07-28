#!/usr/bin/python
import optparse, urllib3, os, threading, time, sys
from termcolor import colored
## Custom Import Scripts


item = []    


def main():

    global outPut, safety, threadCountG
    safety = 50
    print (colored( str(open("Menu.txt", "r").read()), "red")   )
######
    start = time.perf_counter()
    parse = optparse.OptionParser("Usage: StriPy -i <input> -o <output>\nUsage: cat text.txt | StriPy -o <output>\nUsage: Any Output | StriPy -o <output>")
    parse.add_option('-i',     dest='inp', type='string',       help='Target URL')
    parse.add_option('-o',     dest='out', type='string',       help='Target Output')
    parse.add_option('-t',     dest='threadCount', type='int',       help='Change Thread Count')   
    (options, args) = parse.parse_args()
    inp = options.inp
    out = options.out
    threadCount = options.threadCount
    threadCountG = threadCount
    outPut = str(out) + "/" + "Results.txt"
#####


    if(inp != None ):
        makeList(inp)
 
    elif(out != None and inp == None ):
         makeListPipe()
  
    elif (inp == None or out == None):
        os.system("python3 StriPy.py -h ")
    
    
    finished = time.perf_counter()
    print(f"Finished in {round(finished-start, 2 ) } seconds")


## Builds the list of domains.
def makeListPipe():   
    for line in  sys.stdin:
        item.append(line.strip('\n')  )  
    
    print(f"There are [{ str(len(item)) }] addresses.")   
    threads(0)

def makeList(inp):   
    for line in  open(inp, 'r').readlines():
        item.append(line.strip('\n')  )  
    
    print(f"There are [{ str(len(item)) }] addresses.")  
    threads(0)

## Makes the thread count so that it doesn't make to many.
def saftyCheck():
    if (threadCountG != None):
        safety = threadCountG 
        return  threadCountG
    else:
        safety = len(item)
        if  (500 < safety):
            safety = 500
            return safety 
        return safety
    

## Creates threads that will do the processing.
def threads(count):
    saftyCheck()
    while count != len(item):
        thred = []
        i = 0    
        for _ in  range(saftyCheck()) :
            t = threading.Thread(target= hostResolve,args=[count])  
            count += 1
            i += 1
            #print(str(t))
            t.start()
            thred.append(t)
        
        for thre in thred:
            thre.join()
         
 
 
## Resolves all of the hosts.
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

