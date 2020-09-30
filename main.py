from queue import Queue  


class Delta : 
    def __init__(self, _start_state, _input, _end_state) :
        self.start_state = _start_state # list of integer
        self.input = _input # singular char or int
        self.end_state = _end_state # list of integer
    
    def delta2str(self) :
        #returns a readable delta
        return "delta{" + str(self.start_state) + ", " + str(self.input) + "} = " + str(self.end_state)  

    def add_start(self, s) :
        self.start_state = self.start_state.append(s)

    def add_end(self,s) :
        self.end_state = self.end_state.append(s)

class DFA:

    def __init__(self, _Q, _I, _D, _S, _F):
        self.Q = _Q #states
        self.I = _I #input
        self.D = _D #deltas
        self.S = _S #start_states
        self.F = _F #end_states 
        self.closure = [] #cl for each state
        self.cnt = 0

    def cl_loop(self,s,i) :
        cl = []
        for k in s :
            temp = str(k).replace("[", "")
            temp = temp.replace("]","")
            for d in self.D :
                #print("s and d",s,d.delta2str())
                if temp in str(d.start_state) and  ( str(i) in str(d.input) or (self.cnt!=0 and 'e' in str(d.input)) ) :
                    cl = cl + d.end_state
                    self.cnt = self.cnt + 1
                    cl = cl + self.cl_loop(d.end_state, 'e')
                    self.cnt = self.cnt - 1
        #print("cnt",self.cnt)
        return cl

    def cl (self,s,i) : #closure for each state
        #for s in self.Q :
        cl = []
        cl = self.cl_loop(s,i)
        #cl = cl + s
        #print('cl',cl)
        cl=list(set(cl))
        return cl


    def deltas(self) :
        return self.D

    def inputs(self) :
        return self.I

    def start_state(self) :
        return self.S
    
    def end_state(self):
        return self.F

    def print(self) :
        #print(i.delta2str() for i in self.D)
        #print(self.D)
        print("Q :", self.Q)
        print("I :", self.I)
        print("D : ")
        for i in self.D :
            print("",i.delta2str())
        print("S :",self.S)
        print("F :", self.F)
        #print ([ i.delta2str() for i in self.D ], sep = "\n")
        #print( self.Q, self.I, self.S, self.F)



def nfa2dfa (nfa) :
    delta=[] # list for deltas
    states = [] # list for states
    q=Queue() # queue for the loop

    states.append(nfa.start_state())#start state 넣고 시작 # 
    for i in states : #init the queue
        q.put(i)

    #get the num of states
    while(not q.empty()) : #iterate until no more new states are found
        s = q.queue[0] 
        #print("queue length",q.qsize())
        for i in nfa.inputs() : # iterate over all the inputs
            #print("looking for",s,i)
            o = look_all_possible_next_states(nfa, s, i)
            if o : #some states don't have next states at all
                #print("oos",o)
                new_delta = Delta(s,i,o)
                delta.append(new_delta)
                if not any(o == i for i in states ) :
                    states.append(o)
                    q.put(o)
        q.get() #remove from queue after searching once

    #print("num of states",len(states))
    #print(states)
    #for i in delta :
    #    print(i.delta2str())
    end = determine_the_end_state(nfa,states)
   

    dfa = DFA(states,nfa.I,delta,nfa.S,end)
    dfa.print()

def determine_the_end_state(nfa,states) :
    end = []
    for s in states :
        temp = str(nfa.end_state()).replace("[", "")
        temp = temp.replace("]","")
        if( temp in str(s))  :
            end.append(s)
            #end.append(nfa.cl(s)) #for epsilon
    return end

    
            
def look_all_possible_next_states(nfa,s,i) : # for each state
    new=[]
    #print(str(s))
    for n in nfa.deltas() :
        #erase brackets for string search
        temp = str(n.start_state).replace("[", "")
        temp = temp.replace("]","")
        if (temp in str([s]) and n.input == i) :
            new = new + n.end_state
    new = new + nfa.cl(s, i) #for epsilon states
    #print("before",nfa.cl(s))
    new=list(set(new))#get rid of dups     
    #print('s i ',s,i,new)   
    return new

"""
#make nfas
Q = [(0),(1),(2),(3)]
I = ['a','b']
S = [(0)]
F = [(3)]
d=[] # delta input only singular starting states
d.append(Delta([0],'a',[0]))
d.append(Delta([0],'a',[1]))
d.append(Delta([0],'b',[0]))
d.append(Delta([1],'b',[2]))
d.append(Delta([2],'b',[3]))
nfa1 = DFA(Q ,I, d, S, F)
"""


"""
q = [(0),(1),(2),(3)]
i = ['a','b']
s=[(0)]
f=[(3)]
d=[]
d.append(Delta([0],'a',[0]))
d.append(Delta([0],'b',[0]))
d.append(Delta([0],'a',[1]))
d.append(Delta([0],'b',[2]))
d.append(Delta([1],'a',[3]))
d.append(Delta([2],'b',[3]))
d.append(Delta([3],'a',[3]))
d.append(Delta([3],'b',[3]))
nfa1=DFA(q,i,d,s,f)
"""


q = [('A'),('B'),('C'),('D'),('E')]
i = [0,1]
s=[('A')]
f=[('D')]
d=[]
d.append(Delta(['A'],0,['E']))
d.append(Delta(['A'],1,['B']))
d.append(Delta(['B'],1,['C']))
d.append(Delta(['B'],'e',['D']))
d.append(Delta(['C'],1,['D']))
d.append(Delta(['E'],0,['F']))
d.append(Delta(['E'],'e',['B']))
d.append(Delta(['E'],'e',['C']))
d.append(Delta(['F'],0,['D']))
#d.append(Delta(['A'],0,['E']))
nfa1=DFA(q,i,d,s,f)

print("NFA : ")
nfa1.print()

print("")
print("->DFA : ")
nfa2dfa(nfa1)
