# Distributed Sequencer Service

## Introduction

This repository contains the design and implementation of a distributed sequencer service for generating monotonically increasing and unique numerical IDs to client requests. The objective is to ensure that each client request receives a unique ID greater than the previously assigned ID. The system is designed to handle multiple sequencer processes, and clients can potentially contact any process.

## Architecture

### Fixed Sequencer Algorithm

The fixed sequencer algorithm is implemented to achieve total order multicast for the distributed sequencer. The algorithm designates a specific process as the generator/sequencer, responsible for assigning a unique sequence number (ID) to each message received from any client. The sequencer relays the message, along with its assigned sequence number, to all servers in the system.

#### Steps Involved:

1. **Initialization:** The sequencer initializes its sequence number to 1.
2. **Sending a request:** A client sends a `getid()` request to the sequencer.
3. **Sequencer receives a request:** Upon receiving a request, the sequencer assigns a unique sequence number to it and broadcasts the message along with its sequence number to all servers.
4. **Receiving a request at a server:** When a server receives a request, it stores it in a local buffer along with its assigned sequence number. The server keeps track of the next expected sequence number to deliver. When a message with the expected sequence number arrives, the server delivers it back to the sequencer, which responds to the client. The server increments its next expected sequence number.

### Design

#### 1. Sequencer/Generator:

In the fixed sequencer algorithm, the sequencer is elected at the start and remains the sequencer throughout the operation. Upon receiving a message from a client, the sequencer assigns a sequence number to the message and relays it to all servers. The implementation includes a `Generator` class that uses sockets to communicate with clients.

- **Initialization:** `seqnum = 1`
- When receiving a `request`, send `(request, seqnum)` to all servers.

#### 2. Server:

Servers are processes in the system that receive broadcasted messages from the sequencer. Each server stores the message in its local buffer with the assigned sequence number. When a server receives a message with a sequence number matching its next expected sequence number, it delivers the sequence number back to the sequencer and updates its next expected sequence number.

- **Initialization:**
  ```
  buffer ← priority queue
  seqnum ← 1
  ```
- While receiving a `request` from the generator:
  ```
  seqnum = seqnum + 1
  ```

#### 3. Client:

The client is a process that sends a message to all servers. In the fixed sequencer algorithm, the client sends its message to the sequencer, which assigns a unique sequence number and relays it to all servers.

- The client program sends a `request` on each Enter pressed by the user.

#### 4. Delivering an ID:

When a request with the expected sequence number arrives at the server:
- Add `(id, addr)` to the buffer.
- While the buffer is not empty and `q[0][0] == seqnum`:
  - Pop the top of the queue.
  - Send ID to the client.
  - `seqnum = seqnum + 1`

# How to run 

## Generator/Sequencer

`
python Generator.py
`
## Server

`
python Server.py
`

## Client

`
python Client.py
`
`
To test with different ports change the constants.py file
To see the testcases see testcases folder
