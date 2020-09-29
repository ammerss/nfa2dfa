class Delta : 
    def __init__(self, _start_state, _input, _end_state) :
        self.start_state = _start_state # list of integer
        self.input = _input # singular char or int
        self.end_state = _end_state # list of integer
    
    def delta2str(self) :
        #returns a readable delta
        return "delta{{" + str(self.start_state) + "}, " + str(self.input) + "} = {" + str(self.end_state) + "}" 
        #s  = ",".join((str(n)) for n in self.start_state)
        #e = ",".join((str(n)) for n in self.end_state)
        #return "delta{{" + s + "}" + "," + self.input + "} = {" + e + "}"

    def add_start(self, s) :
        self.start_state = self.start_state.append(s)

    def add_end(self,s) :
        self.end_state = self.end_state.append(s)

class DFA:

    def __init__(self, _Q, _I, _D, _S, _F):
        self.Q = _Q #
        self.I = _I # 
        self.D = _D # 
        self.S = _S #
        self.F = _F # 

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

from queue import Queue  

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
    end = determine_the_end_state(nfa,delta)
   

    dfa = DFA(states,nfa.I,delta,nfa.S,end)
    dfa.print()

def determine_the_end_state(nfa,delta) :
    end = []
    for d in delta :
        temp = str(nfa.end_state()).replace("[", "")
        temp = temp.replace("]","")
        if( temp in str(d.end_state))  :
            end.append(d.end_state)
    return end

            
def look_all_possible_next_states(nfa,s,i) :
    new=[]
    #print(str(s))
    for n in nfa.deltas() :
        #erase brackets for string search
        temp = str(n.start_state).replace("[", "")
        temp = temp.replace("]","")
        if (temp in str([s]) and n.input == i) :
            new = new + n.end_state
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
nfa1 = DFA(Q ,I, d, S, F)"""

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




print("NFA : ")
nfa1.print()

print("")
print("->DFA : ")
nfa2dfa(nfa1)
