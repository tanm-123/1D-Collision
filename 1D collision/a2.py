class PriorityQueue:
    def __init__(self):
        self.list=[]
    def is_empty(self):
        if len(self.list)==0:
            return True
        else:
            return False
    def heap_up(self,n): #to traverse from nth node to the root 
        while self.list[(n-1)//2][0]>=self.list[n][0]:# if we are at nth node then its parent node is (n-1)//2 so if parent time is more than node then we will exchange
            if self.list[(n-1)//2][0]==self.list[n][0]:# if both times are same then we will compare the i value of tuple..if i of parent is more then we will exchange
                if self.list[(n-1)//2][1]<self.list[n][1]:
                    return
            c1=self.list[(n-1)//2]
            c2=self.list[n]
            self.list[n]=c1
            self.list[(n-1)//2]=c2
            n=(n-1)//2
            if n==0:# means we are at root so no parent
                return
    def heap_down(self,n):# to traverse from node to the end of list 
        l=len(self.list)
        if n>(l-2)//2:# means we are in the leaf so no more child branches
            return
        if 2*n+2<=l-1:# if we are at nth node then 2n+1 is left child and 2n+2 is right branch
            while (self.list[2*n+1][0]<=self.list[n][0] or self.list[2*n+2][0]<=self.list[n][0]): #compare between child and node if child's time is less then exchange
                if  self.list[2*n+1][0]<self.list[2*n+2][0]:
                    v=self.list[2*n+1]
                else:                       #assign v with the branch having lesser time
                    v=self.list[2*n+2]
                if v[0]==self.list[n][0]:   #if time of child and node is same then compare the i value of tuple->if i of child is less then exchange
                    if v[1]>self.list[n][1]:
                        break
                c1=self.list[n]
                c2=v
                self.list[n]=c2
                if self.list[2*n+1][0]<self.list[2*n+2][0]:
                    self.list[2*n+1]=c1
                    n=2*n+1
                else:
                    self.list[2*n+2]=c1
                    n=2*n+2
                if n>(l-2)//2:
                    break
                if 2*n+2>l-1:
                    break
        if 2*n+1<=l-1:
            if (self.list[2*n+1][0]<=self.list[n][0]):
                v=self.list[2*n+1]
                if v[0]==self.list[n][0]:
                    if v[1]>self.list[n][1]:
                        return
                c1=self.list[n]
                c2=v
                self.list[2*n+1]=c1
                self.list[n]=c2
    def insert(self,data): 
        self.list.append(data)
        if len(self.list)>1:
            self.heap_up(len(self.list)-1)
    def extractmin(self):
        l=[]
        n=len(l)
        if len(self.list)>1:
            c=self.list[0]
            d=self.list.pop()
            self.list[0]=d
            if len(self.list)>1:
                self.heap_down(n)
        else:
            c=self.list[0]
            self.list.pop()
        return c
    def buildheap(self,l): #this will build the heap in O(n)
        self.list=l
        for i in range ((len(l)-1)//2,-1,-1):
            self.heap_down(i) 
pq=PriorityQueue()
def listCollisions(M,x,v,m,T):
    cnt=[] #a list which contains the no. of collisions of each particle
    l=[]
    t=[] # a list which contains the time frame of each particle 
    n=len(M)
    for i in range (0,n):
        t.append(0)
        cnt.append(0)
    tr=0 # the real time at present 
    for i in range (0,n-1):
        if v[i]>v[i+1]: #iterate and create tuples and build heap from the values
            j=(x[i+1]-x[i])/(v[i]-v[i+1])
            if T>j:
                X=x[i]+(v[i]*j)
                col=(j,i,X,cnt[i],cnt[i+1])
                l.append(col)
    if len(l)!=0:
        pq.buildheap(l)
    ans=[]
    while (m!=0 and pq.is_empty()==False):# after building initial heap extract the root and check whether collision happens or not
        tup=pq.extractmin()
        d=tup[1]
        if cnt[d]==tup[3] and cnt[d+1]==tup[4]:# we stored a count at the time of making tuple..so if that count is same as the present count of particle and the next particle-> means there path have not changed so means that collision will happen
            cnt[d]+=1                           # if count stored and the real count comes to be different->means the particles involved have collided with other particles before-> so this tuple becomes invalid
            cnt[d+1]+=1
            tupp=(round(tup[0],4),tup[1],round(tup[2],4))
            ans.append(tupp)
            m=m-1
            x[d]=x[d+1]=tup[2]   #update the positions after collision
            tr=tup[0]
            t[d]=t[d+1]=tr # update the time frames as well
            l=v[d]
            b=v[d+1]
            v[d]=((l*(M[d]-M[d+1]))/(M[d]+M[d+1])) + (b*2*M[d+1]/(M[d]+M[d+1])) # update the velocities 
            v[d+1]=(l*2*M[d]/(M[d]+M[d+1])) - ((b*(M[d]-M[d+1]))/(M[d]+M[d+1]))
            if d!=n-2: # if last 2 balls have not collided
                if d!=0: # if first 2 balls have not collided
                    if v[d+1]>v[d+2]: #when i and i+1 have collided-> check possible collision of i+1 with i+2 and i-1 with i and store them in the priority queue        
                        j=(x[d+2]+(v[d+2]*(tr-t[d+2]))-x[d+1])/(v[d+1]-v[d+2])
                        if T>tr+j:
                            X=x[d+1]+(v[d+1]*j)
                            col=(tr+j,d+1,X,cnt[d+1],cnt[d+2])
                            pq.insert(col)
                    if v[d-1]>v[d]:
                        j=(x[d]-(x[d-1]+(v[d-1]*(tr-t[d-1]))))/(v[d-1]-v[d])
                        if T>tr+j:
                            X=x[d]+(v[d]*j)
                            col=(tr+j,d-1,X,cnt[d-1],cnt[d])
                            pq.insert(col)
                else:
                    if v[d+1]>v[d+2]:
                        j=(x[d+2]+(v[d+2]*(tr-t[d+2]))-x[d+1])/(v[d+1]-v[d+2])
                        if T>tr+j:
                            X=x[d+1]+(v[d+1]*j)
                            col=(tr+j,d+1,X,cnt[d+1],cnt[d+2])
                            pq.insert(col)
            else:
                if v[d-1]>v[d]:
                        j=(x[d]-(x[d-1]+(v[d-1]*(tr-t[d-1]))))/(v[d-1]-v[d])
                        if T>tr+j:
                            X=x[d]+(v[d]*j)
                            col=(tr+j,d-1,X,cnt[d-1],cnt[d])
                            pq.insert(col)
    return ans
# the order is n+mlogn as while loop will operate at most m times and we are inserting and extracting which is around 2mlogn and rest we are doing O(1) so net time inside while loop is O(mlogn)
# and outside while loop we are just iterating n times using for loops so O(n)
# initially i was using distance to check validity of tuple but due to calculations there was some problem in the precision-> so therefore then i used count function to detect collision