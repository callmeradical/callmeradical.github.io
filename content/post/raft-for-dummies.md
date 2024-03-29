+++
draft = false
date = "2016-09-11T19:28:49-05:00"
title = "Raft for Dummies and those like me."
description = ""
subtitle = ""
header_img = ""
toc = true
tags = ["Miscellaneous", "DevOps", "Cloud Engineering"]
categories = ["Technology", "Programming", "Algorithm", "Distributed System", "Networking"]
series = []
comment = true
image = "https://dl.dropboxusercontent.com/s/6ayy2yfyl2j2qtc/raft.png"
+++

This is going to be my very feeble attempt to explain the Raft consensus algorithm.  The very least I will accomplish is sharing the material I have read about Raft and how I have come to understand it. Raft is used in popular pieces of software such as RethinkDB, etcd, and a number of Hashicorp products.([^1])

### What is Raft?

Raft was developed in the hopes of creating an easy to understand consensus algorithm. As far as that goes, I think they succeeded, especially when compared with similiar algorithms, such as [Paxos](https://en.wikipedia.org/wiki/Paxos_(computer_science))(I am still working this one out). Consensus algorithms allow a collection of machines to work as a coherent group that can survive the failures of some of its members.([^2])

To really understand this, lets take a step back and talk about what makes up a distributed system. Wikipedia has a really great definition on the [Distributed Computing page](https://en.wikipedia.org/wiki/Distributed_computing):

> A distributed system is a model in which components located on networked computers communicate and coordinate their actions by passing messages.

The consensus algorithm is how these computers coordinate their actions. Implementing a consensus algorithm is typically necessary in the context of *replicated state machines*. 

A common implementation of a replicated state machine, uses a replicated log. In otherwords, the following is true:

- Multiple logs containing a series of commands or transactions.
- Each log must contain the same instructions in the same order.
- Each machine processes the same sequence of commands.

 A commonplace example of this, at least in most enterprise shops, is Zookeeper. Zookeeper is an example of a replicated state machine.![cloudcraft - RSM (1)](https://dl.dropboxusercontent.com/s/eahsi12m5jov22u/statemachine.png)

This is the basic design of state machine architecture. Client sends a message to the consensus module, the consensus module replicates the transaction to multiple logs, the state machine reads from the logs and returns the value or transaction back to the client.

The log is very important. The consensus algorithm is the manner in which we keep the replicated log consistent. The consensus module on a node receives instructions from clients, adds them to its log, and it communicates to other servers to ensure that every log eventually contains all requests in the in which they were received, even if some servers fail. After the commands are properly replicated, each server's state machine processes them in log order, and output is returned to the client nodes. The outcome, is a system that appears to be a single, highly reliable, state machine. This is true with the exception of Byzantine conditions([^3]) (network delays, partitions, packet loss, duplication, and reordering).



In Raft a node can be in 1 of 3 states:

- The Follower state
- The Candidate state
- The Leader state



All nodes start in the follower state. If Followers don't hear from a leader then they can become a candidate. The candidate then requests votes from other nodes. Nodes reply with their vote. The candidate becomes the leader if it gets votes from a majority of nodes. This is the process called *Leader Election*. All changes now flow through the leader. Each change is added as an entry in the node's log. The log entry is uncommitted and as such will not update the node's value, instead, the node first replicates it to the follower nodes, then the leader waits until a majority of nodes have written the entry, and is then committed to the leader node. The leader then notifies the followers that the entry is committed. The cluster has then come to a consensus. This is log replication.



Leader Election

In Raft there are two timeout settings which control elections, *Election Timeout*, and *Heartbeat Timeout*.

Election timeout is the amount of time a follower waits until becoming a candidate. Election timeout is randomized to be between 150 ms and 300 ms. After the election timeout the follower becomes a candidate and starts a new election term, votes for itself, and sends out Request Vote messages to other nodes. If the receiving node hasn't voted yet in this term then it votes for the candidate, and the node resets its election timeout. Once a candidate has a majority of votes it becomes leader. 

The leader begins sending out Append Entries messages to its followers. These messages are sent in intervals specified by the heartbeat timeout. Followers then respond to each Append Entries message. This election term will continue until a follower stops receiving heartbeats and becomes a candidate. Requiring a majority of votes guarantees that only one leader can be elected per term. If two nodes become candidates at the same time then a split vote can occur. In the event of a split vote, say we had four nodes, two nodes both start an election for the same term, and each reaches a single follower node before the other. Now each candidate has 2 votes and can receive no more for this term. The nodes will wait for a new election and try again. This will continue until majority is reached.([^4])



Raft was created to be easier to understand than Paxos. There is a conference specifically for systems design called the NSDI (Networked Systems Design and Implementation) and someone there even voiced concern about people understanding all components of Paxos. Claiming that there only 5 people are the conference that understood it completely. Whether or not that is true. I can say for sure, Raft is definitely easier to understand and has succeeded in that mission.

### References

[^1]: [Raft Implementations](https://raft.github.io/#implementations) |
[^2]: [In Search of an Understandable Consesus Algorithm ](https://raft.github.io/raft.pdf) | 
[^3]: [Byzantine fault tolerance](https://en.wikipedia.org/wiki/Byzantine_fault_tolerance) |
[^4]: [The Secret Lift of Data - Raft](http://thesecretlivesofdata.com/raft/#home) | 



