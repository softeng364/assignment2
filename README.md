# Assignment 2

## Getting started

Please clone the git repository from Assignment 2 and work directly from it so that you can easily pull changes from GitHub should any be necessary.

```powershell
> git clone https://github.com/softeng364/assignment2.git
> cd assignment2
```

## Submission & Assessment

- A **marking rubric** is available on [Canvas](https://canvas.auckland.ac.nz/courses/31482/assignments/92738).

- Please **upload** your code to [Canvas](https://canvas.auckland.ac.nz/courses/31482/assignments/92738).

- The rubric includes a **Best Practice** component. Fur full credit, please ensure that your code adheres to the usual guidelines of consistency and readability, and use `pycodestyle` to check conformance with PEP 8, as demonstrated in lab worksheet.

---

## Part 1. Link-state routing

### Task 1.1. Predecessor lists

Modify `dijkstra_5_14()` so as to return  predecessors (in addition to distances).

Using your new function, **visualize** the least-cost path tree for node `u` on the network from Slide `5-15`, as we did in Lab 1.

- The new interface should matches that of NetworkX's `dijkstra_predecessor_and_distance()` i.e. having the same order- and types of output arguments.

- We need to initialize the predecessor map appropriately and update it each time the distance map is update. Only a few lines of code are required.

### Task 1.2. Forwarding tables

Write a function `forwarding` that produces the forwarding table associated with a predecessor map.

- Verify that the output is consistent with the example on Slide `5-17`.

- Nodes may be visited more than once. If you have time and would like to experiment with a more efficient algorithm, please see Assignment 2 Challenges, below.

### Task 1.3. Widest path routing

Make the necessary modifications to `dijkstra_5_14` (from Lab 1) to solve instances of the [widest path problem](https://en.wikipedia.org/wiki/Widest_path_problem).

Add suitable [keyword arguments](https://docs.python.org/2/tutorial/controlflow.html#keyword-arguments) `plus`, `less`, `infinity`, and `min_` to the parameter list so that the same code can solve shortest- or widest (or some other similarly structured) path problems based on the operator functions passed into it.

**Visualize** the widest path tree for node `u` on the network from Slide `5-15`, as we did in Lab 1, interpreting the link `'cost'` as bandwidth.

- In Lab 1, we saw that `min` used a keyword argument used to extend the applicability of Python's built-in function `min(..., key=...)`.

- If none of these arguments are specified, the defaults should correspond to the least-cost path problem.

- Operators like `+` and `<` can be represented as functions using [`lambda`](https://docs.python.org/3/tutorial/controlflow.html?highlight=lambda#lambda-expressions) expressions (e.g. `lambda a, b: a + b`) or the definitions provided in module [`operator`](https://docs.python.org/3/library/operator.html) (e.g. `operator.add`).

#### Additional remarks (17/05) on Task 1.3

- You may like to introduce an additional keyword parameter `sourcedist=0` in `dijkstra_generalized`, as discussed on this [Piazza post](https://piazza.com/class/jf4jq6n8ha05zg?cid=15). This is not essential for Assignment 2, but please do ensure that you understand the role that this parameter should play.

- To visualize the least-cost path and widest path trees on **separate** plots, the following code should be used:

```python
import matplotlib.pyplot as plt

fig1 = plt.figure(1)
fig1.suptitle('Shortest paths')
# Least-cost path visualization here
# ...
fig1.show()

fig2 = plt.figure(2)
fig2.suptitle('Widest paths')
# Widest path visualization here
# ...
fig2.show()
```

---

## Part 2. Error detection

### Task 2.1. One's complement in Python

Write a function `hextet_complement(x)` to compute the one's complement of a Python `int` regarded as a fixed-width hextet (16 bits, two bytes/octets, four nibbles).

- Use the the **invert** operator `~` and a suitable mask, as discussed in the lab.

- Don't worry about handling the case where the argument itself occupies more than one hextet.

### Task 2.2. The Internet Checksum

Implement the [Internet Checksum](https://en.wikipedia.org/wiki/IPv4_header_checksum) in Python.

- Use `hextet_complement()` to compute the one's complement.

- Your function should work for any Python sequence whose elements are bytes.

- Ensure that you can reproduce the calculation given in Section 3 of [IETF 1071](https://tools.ietf.org/html/rfc1071).

> We'll use this function to check IP packets in Part 3.

#### Additional remarks (17/05) on Task 2.2

- Please remember (from the lab worksheet) that an implementation in C of the Internet Checksum is provided in RFC 1071, Section 4.

```c
/*
The following "C" code algorithm computes the checksum with an inner loop that sums 16-bits at a time in a 32-bit accumulator.
*/
{
    /*
    Compute Internet Checksum for "count" bytes beginning at location "addr".
    */
    register long sum = 0;

    while( count > 1 )  {
    /*  This is the inner loop */
        sum += * (unsigned short) addr++;
        count -= 2;
    }

    /*  Add left-over byte, if any */
    if( count > 0 )
        sum += * (unsigned char *) addr;

    /*  Fold 32-bit sum to 16 bits */
    while (sum>>16)
        sum = (sum & 0xffff) + (sum >> 16);

    checksum = ~sum;
}
```

- With respect to the C code above:
  - A literal translation into Python of the C code `sum += * (unsigned short) addr++;` is not possible. Rather, we will need to treat the two adjacent bytes separately and shift the bits in the "larger" one.
  - Warning: Recall from the worksheet that Python's operator `~` does **not** work in the same was as C's version.

- If you like, it is possible to index every second element of a sequence `data` as follows:

```python
>>> data = b'abcdefg'
>>> data[0::2]
b'aceg'
>>> data[1::2]
b'bdf'
>>>
```

- If you like, Python does have a built-in sum function (cf. [this Piazza post](https://piazza.com/class/jf4jq6n8ha05zg?cid=14)).

### Task 2.3. Cyclic Redundancy Checks

Implement a function to perform CRC checks with a given generator on an arbitrary sequence of bytes.

- Verify that your function reproduces the calculation of slide `6-15`.

- There is no need to store the quotient.

#### Additional remarks (17/05) on Task 2.3

- Please use the temlate file `crc.py`, which contains several test cases. If you have already done this task, please rename your existing file `crc.py` and ensure that your function `crc.crc()` has the same interface as the one in the template provided; Thank You.

- The sample code provided in the lab worksheet performs one step of the long division; please ensure that you are happy with this. Hence, we need iterate through a sequence of such steps: Very little new code is required because the polynomial coefficients are either `0` or `1`.

---

## Part 3. ICMP and socket programming

Use your modules `icmp` and `checksum` to reimplement `ping` in Python.

- To send ICMP messages, we'll need to use a so-called [raw socket](https://en.wikipedia.org/wiki/Network_socket#Raw_socket), as returned by the following snippet:

```python
import socket
socket.socket(family=socket.AF_INET,
              type=socket.SOCK_RAW,
              proto=socket.getprotobyname("icmp"))
```

Your system might require Administrator permissions to open raw sockets: In particular, you may not be able to complete this task on the Faculty's lab PCs.

- Use Python's [`argparse`](https://docs.python.org/3/library/argparse.html) module to process the following command-line options:

| Name | Abbreviation | Type | Default | Help |
|---|---|---|---|---|
| `--timeout` | `-w` | `int` | 1000 | Timeout to wait for each reply (milliseconds) |
| `--count` | `-c` | `int` | 4 | Number of echo requests to send |
| `hosts` | | `str` | | URL or IPv4 address of target host(s) |

A demonstration of the required line interface is shown in the examples below.

- Use Python's [`struct`](https://docs.python.org/3/library/struct.html) and [`collections.namedtuple`](https://docs.python.org/3/library/collections.html?highlight=namedtuple#collections.namedtuple) libraries to to de/serialize ICMP messages to/from byte sequences.

- Use Python's [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) to guarantee that your socket is closed gracefully. `socket` module's documentation provides several [examples](https://docs.python.org/3/library/socket.html#example).

- Use a suitable function from the [`time`](docs.python.org/3/library/time.html) module to estimate round-trip time (elapsed time).

- Each ICMP echo request should carry the time instant at which it was created/sent. In reality, this would not be necessary, but it relates to one of the challenge problems.

- Use exceptions to signal checksum errors and timeouts. All exceptions should be handled in `verbose_ping()`.

- Use [built-in functions](https://docs.python.org/3/library/functions.html) to calculate the minimum, maximum, and mean of the calculated round-trip times, as demonstrated in the example below.

- Complete details about the ICMP messages used for `ping` implementations are detailed on [wikipedia.org](https://en.wikipedia.org/wiki/Ping_(networking_utility)).

#### Additional remarks (17/05) on Part 3

- A more detailed template is now (17/05) available to help with Part 3. Please study the new template and replace each "TODO" with suitable code.

- The type specifiers passed to `struct.pack` and `struct.unpack` must be consistent with the ICMP protocol's [packet format](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Datagram_structure):

| Field | Integer Type | Size in bytes |
|---|---|---|
| `type` | `unsigned char`| 1 |
| `code` | `unsigned char` | 1 |
| `checksum` | `unsigned short` | 2 |
| `identifier` | `unsigned short` | 2 |
| `sequence_number` | ~~`unsigned char`~~ `unsigned short` | ~~1~~ 2 |

- The type of our payload will be  `float`:

```python
>>> import time
>>> type(time.process_time())
<class 'float'>
>>> type(time.perf_counter())
<class 'float'>
>>> type(time.clock())
<class 'float'>
```

- You can execute `ping.py` from the IPython console inside Anaconda using `%run` e.g.

```python
%run ping --help
%run ping --count 5 www.google.com
```

##### Example: Command line interface

```powershell
> python ping.py --help
usage: ping.py [-h] [-w milliseconds] [-c num] host [host ...]

Test a host.

positional arguments:
  host                  URL or IPv4 address of target host(s).

optional arguments:
  -h, --help            show this help message and exit
  -w milliseconds, --timeout milliseconds
                        Timeout to wait for each reply (milliseconds).
  -c num, --count num   Number of echo requests to send.
```

##### Example: Successful invocation

```powershell
>python ping.py www.python.org --count 3
Contacting www.python.org with 36 bytes of data
Reply from 151.101.0.223 in 5ms: ICMPMessage(type=0, code=0, checksum=48791, identifier=33540, sequence_number=0)
Reply from 151.101.0.223 in 12ms: ICMPMessage(type=0, code=0, checksum=35850, identifier=33540, sequence_number=1)
Reply from 151.101.0.223 in 6ms: ICMPMessage(type=0, code=0, checksum=61385, identifier=33540, sequence_number=2)
Ping statistics for 151.101.0.223:
    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss)
Approximate round trip times in milli-seconds:
    Minimum = 5ms, Maximum = 12ms, Average = 7ms

```

#### Example: Timeout

Auckland University's web-server doesn't respond to ICMP echo requests:

```powershell
> python ping.py www.auckland.ac.nz --count 3 --timeout 1500
Contacting www.auckland.ac.nz with 36 bytes of data
Request timed out after 1500ms
Request timed out after 1500ms
Request timed out after 1500ms
Ping statistics for 130.216.159.127:
    Packets: Sent = 3, Received = 0, Lost = 3 (100.0% loss)
```

- Please be aware of the marking scheme [on Canvas](https://canvas.auckland.ac.nz/courses/31482/assignments/92738) - especially the link to `view longer description` for each task.

---

## Network programming challenges

> These are not assessed: Please don't look at these unless you have spare time.

### Optimized routing functions

Using only the Python standard library, optimize (for speed) your functions.

- Incorporate a [priority queue](https://en.wikipedia.org/wiki/Priority_queue) to improve the efficiency of Dijkstra's algorithm. An implementation is available in the Standard Library's [`heapq`](docs.python.org/3.6/library/heapq.html) and [`queue`](https://docs.python.org/3.6/library/queue.html) modules.

- Re-implement `forwarding` using a [graph traversal](https://en.wikipedia.org/wiki/Tree_traversal) algorithm that visits each node only once. The [Boost Graph Library](https://www.boost.org/doc/libs/1_67_0/libs/graph/doc/) is a good place to look for inspiration e.g. [`depth_first_search`](https://www.boost.org/doc/libs/1_67_0/libs/graph/doc/depth_first_search.html)

- Use one of NetworkX's [graph generators](https://networkx.github.io/documentation/stable/reference/generators.html) to generate a large test network.

- Use IPython's [`%time`](http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time) or [`%timeit`](http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit) magic functions to compare execution times.

### Asynchronous `ping`

Our current implementation waits to receive the current echo response before sending the next echo request. Employ [`gevent`](http://www.gevent.org) to write an asynchronous version of your `ping` code, which doesn't block on echo receives.
