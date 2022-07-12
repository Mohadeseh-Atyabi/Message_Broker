# Message_Broker
A message broker is a server that distributes messages received from clients. Of course, these brokers do more things that are beyond our discussion. There are two important operations in the server, one is to subscribe and the other is to publish. In the subscribe operation, the client requests to listen to a specific topic. In publish, the client publishes a rar message of a specific topic. Finally, the broker delivers the messages to all those listening on that thread. In this section, all communication between the client and the server is implemented in TCP format.

## Client to server commands:
- Publish: This command sends a message from the client side to the server under a specific title. Messages are ASCII strings of arbitrary length.
- Subscribe: This command informs the server that this client is requesting to receive messages with the given title.
- Ping: This command is sent from the client side to ensure connection.
- Pong: This command is sent from the client side in response to the Ping message.

## Server to client commands:
- Message: This command sends a message from the server side to the client when the applicant is a subject (note that this command includes the message and title). Messages are ASCII strings of arbitrary length.
- SubAck: This command is sent from the server side to confirm the client's subscribe message when the subscribe operation is successful.
- PubAck: This command is sent from the server to confirm the client's publish message when the publish operation is successful.
- Ping: This command is sent from the server side to ensure connection.
- Pong: This command is sent from the server side in response to the Ping message.

## Server implementation:
The server has a server socket that listens on a specific port (here we assume the desired port is 1370). Since the server is going to handle several simultaneous connections, you will need to create a Thread for each connection so that the accept function is called immediately. The server does not close any connection and keeps all connections open. For the server, each connection represents a client, so it must have a list of sockets and their desired titles. Be careful that the server should also consider the status of connections and avoid sending data on closed connections.

## Client implementation:
The client receives the following arguments at runtime. For more information about arguments in Python, you can use here. The client has two main commands:

The Publish command sends the message given in the message argument to the server under the title of the topic argument. This command waits for 10 seconds until the PubAck message arrives from the server and informs the user if it is received successfully. Otherwise, an appropriate error will be displayed.

> python3 client.py <host> <port> publish <topic> <message>
> your message published successfully # in case of success
> your message publishing failed # in case of failure

The Subscribe command informs the server that we are requesting to receive the messages of the topics given under the topic arguments.
 Please note that this command can be called with one or more topics and you need to use Thread to have multiple connections with the server at the same time. (For more information, you can refer here). For each title, you need to send a Subscribe message and receive a SubAck message within a limited period of 10 seconds. If the Subscribe message is not received within this limited period, your program should end with the appropriate message. Finally, the program should listen on all created sockets to display the received messages to the user in the form of a Message command.
 
 > python3 client.py <host> <port> subscribe <topic-1> <topic-2> ... <topic-n>
> # in case of success
> subscribing on <topic-1> <topic-2> ... <topic-n>
> <topic-1>: message
> <topic-2>: message
> <topic-1>: message
> # in case of failure
> subscribing failed
