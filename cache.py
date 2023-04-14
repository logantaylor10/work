# Cache
# Implementation of a simplified cache with three levels, implemented as a hash table using seperate chaining for collision resolution


class Node:
    def __init__(self, content):
        self.value = content
        self.next = None
        self.previous = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            #check that all attributes are equal
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        #let hash value be equal to sum of every ASCII value in the header, modulo 3
        value = 0
        for ch in self.header:
            #for each character in header, add ASCII number to value      
            chord = ord(ch)
            value += chord
        finalvalue = value%3
        #value modulo 3 for final value to return        
        return finalvalue



class CacheList:
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        #since numItems is already an attribute, return it for length
        return self.numItems
    
    def put(self, content, evictionPolicy):
        if content.size > self.maxSize:
            #insertion not to be allowed if size of content is greater than maximum size
            return f'Insertion not allowed'
        elif content.cid in self:
            #insertion not allowed, but use of in/__contains__ method moves content to beginning of list
            return f'Content {content.cid} already in cache, insertion not allowed'
        while self.remainingSpace < content.size:
            #remove content to make space as needed, using given eviction polcy
            if evictionPolicy == 'mru':
                self.mruEvict()
            elif evictionPolicy == 'lru':
                self.lruEvict()
        self.remainingSpace -= content.size
        self.numItems += 1
        if self.head is None:
            #if there are no nodes/no head               
            self.head = Node(content)
            self.tail = self.head
        elif self.tail == self.head:
            #if there is one/tail and head are the same        
            self.head = Node(content)
            self.head.next = self.tail
            self.tail.previous = self.head
        else:
            temp = self.head
            self.head = Node(content)
            self.head.next = temp
            if self.head.next is not None:
                self.head.next.previous = self.head
        return f'INSERTED: {content}'

    

    def __contains__(self, cid):
        if len(self) != 0:
            #if length of CacheList is 0, do not complete
            current = self.head
            prev = None
            while current.value.cid != cid and current.next is not None:
                #if current value is not desired value, and there is a next value, set current to next, changing previous as well
                prev = current
                current = current.next
            if current.value.cid == cid:
                if current == self.head:
                    #if current is already head, only need to return True            
                    return True
                elif current == self.tail:
                    #if current is tail
                    tailprev = self.tail.previous
                    temp = self.head
                    self.tail = tailprev
                    if self.tail is not None:
                        self.tail.next = None
                    self.head = current
                    self.head.next = temp
                    if self.head.next is not None:
                        self.head.next.previous = self.head
                else:
                    #if current is not head or tail
                    prev.next = current.next
                    current.next.previous = prev
                    temp = self.head
                    self.head = current
                    self.head.next = temp
                    self.head.next.previous = self.head
                return True
            else:
                current = current.next
        return False


    def update(self, cid, content):
        if cid in self and (content.size <= self.head.value.size + self.remainingSpace):
            #if content in CacheList and content size less than head and remaining space combined        
            self.remainingSpace -= content.size - self.head.value.size
            temp = self.head.next
            self.head = Node(content)
            self.head.next = temp
            if temp is not None:
                self.head.next.previous = self.head
            return f'UPDATED: {content}'
        else:
            return f'Cache miss!'



    def mruEvict(self):
        if len(self) !=0:
            #if length of CacheList is 0, do not complete
            if self.head.next is not None:
                temp = self.head
                self.head = self.head.next
                self.head.previous = None
            else:
                temp = self.head
                self.head = self.head.next
                self.tail = None
            self.remainingSpace += temp.value.size
            self.numItems -= 1


    
    def lruEvict(self):
        if self.tail is None:
            #if tail is None/only head remains, use mruEvict       
            self.mruEvict()
        elif len(self) != 0:
            #if length of CacheList is 0, do not complete
            if self.tail.previous is None:
                temp = self.tail
                self.tail = self.tail.previous
                self.head = None
            else:
                temp = self.tail
                self.tail = self.tail.previous
                self.tail.next = None
            self.remainingSpace += temp.value.size
            self.numItems -= 1


    def clear(self):
        #while content remains in List, remove it
        while len(self) != 0:
            self.mruEvict()
        #set remainingSpace back to the maximum size
        self.remainingSpace = self.maxSize
        return 'Cleared cache!'

class Cache:
    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    
    def insert(self, content, evictionPolicy):
        #put content in cache level decided by hash
        return self.hierarchy[hash(content)].put(content,evictionPolicy)    


    def __getitem__(self, content):
        if content.cid in self.hierarchy[hash(content)]:
            #if cid in cache at proper level then return it    
            return self.hierarchy[hash(content)].head
        else:
            return 'Cache miss!'                                   


    def updateContent(self, content):
        #update method for content in cache
        return self.hierarchy[hash(content)].update(content.cid,content)

