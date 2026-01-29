### Heap 
Tree based data structure, with parent (p) - child (c) structuring of elements. 
a) max heap : p>=c.
b) min heap : p<=c.
Common implementation of heap is binary heap, each node has at most two children. Let's assume max heap is implemented. 
Completeness of heap - only the last row may be partially filled, rest must be completely filled. 
height = number of edges from root to leaf = num of rows -1.
$2^h \leq n < 2^{h+1}. \implies h \leq log_2n < h+1 \implies h = \lfloor log_2n \rfloor$
$\therefore h = O(logn)$
Array representation
Leave 0th index unused for simplicity. Left child of $n^{th}$ element occupies $2n^{th}$ position, right child occupies $(2n+1)^{th}$ position. So, parent of nth element = $\lfloor \frac{n}{2} \rfloor$

increaseKey - key at known index is increased.
If new key>parent, exchange the key with its parent's key (float up). Keep floating up until the key reaches a position good enough.

Insertion -  we append a value to the end of the binary tree and then float it up, as long as necessary (like increaseKey)

Building a heap - repeatedly insert keys to heap, starting with an empty heap.

Worst case, every added element has to climb full height --> each takes time O(logn), so total time to build heap is O(nlogn)

maxHeapify - when we have a binary tree such that only the root isn't correct, each of the child trees are ordered properly. Then, swap root with the larger of its two children and keep floating until nexessary.

extractMax - Swap the element at the extreme end of the heap with the root.
 Remove the value at the extreme end and return it as the maximum value.
 Sink in the root to the right place with `maxHeapify`.

heapsort - constantly extract max.


### Discrete event clock vs wall-clock time

a) Wall-Clock Time : 
Actual time measured by clock, subject to hardware constraints, latency, continues regardless of whether event occurs. 

b) Discrete event clock : 
Jumps from one event timestamp to another, only when event occurs. Deterministic, better for simulation.

### Deterministic replay (important for debugging & RL)
a) Assign time stamp + sequence id to orders.
b) Use pseudo  random number generator (prng), which gives same output for same 'seed', to control the randomness. 
c) Complete input logging. 

------------------------------------------------------------------------
## Implementing LOB (Understanding PyLOB)
### OrderBook Class
lastPrice : a dict with key : value pairs where key is the ticker of a particular stock and the value is the last traded price of that stock on the market.
tickSize (should also have a default value) : minimum increment in stock prices.
rounder : since python's round(x, n) function takes n to be number of decimal places, we must convert tick size to decimal places. if tick size = $10^{-n}$, we want n decimal places. So, rounder = $log_{10}{\frac{1}{tick}}$ = $log_{10}{10^n}$ = n.

time : since we're not using wall clock time, we need to maintain event driven time.
nextQuoteID : sequential id for incoming orders.



#### methods 
clipPrice(self, price): rounds price according to ticker.
updateTime(self) : updates time+=1
processOrder(self, quote, fromData, verbose) : 
quote is a dictionary of data about the order (side, type, price, qty, name of security)
fromData is a boolean which tells us whether this is a replay or a new order
verbose is a boolean, which tells us whether we want to print details.
workflow - if fromData, then change self.time to timestamp of order.
if new, then set time of order (quote dict) to self.time, self.time+=1, assign order id, increment id.
validate the order (qty>0, type should be market or limit, side should be buy or sell)
if it's a limit order, clip the quote price based on ticker.









