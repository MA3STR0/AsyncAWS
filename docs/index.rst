AsyncAWS - Asynchronous AWS library in Python
=============================================

.. toctree::
   :maxdepth: 2

   SQS Reference <sqs>
   SNS Reference <sns>

About
+++++

AsyncAWS is a collection of convenient classes that provide abstract access
to AWS API in Python. It's killer-feature is efficient asynchronous behaviour
achieved with simple, sequential code. No callback spaghetti thanks to Python
"yield" and coroutines. Just look:

::

        queue_url = yield sqs.create_queue("test-queue")
        message_id = yield sqs.send_message(queue_url, "Hello, World!")

Used within a coroutine, this code will 'pause' on each yield keyword, letting
IOLoop to run other stuff meanwhile. As soon as AWS will return some response,
IOLoop will switch back to the "yield" point, and just continue as if "yield" was never there.
This way can keep the usual sequential coding style, but run the code asynchronously.

Installation
++++++++++++

I'm preparing a stable package for PyPI, meanwhile you can install it
with pip directly from github:
::

    pip install git+git://github.com/MA3STR0/AsyncAWS.git


Still not convinced? Wondering what is the benefit?
+++++++++++++++++++++++++++++++++++++++++++++++++++

First of all, it's performance. Most of the time our code is waiting for IO, especially
if it has to deal with remote connections: database, web-APIs, etc. Calling such resources
asynchronously allows main Python thread to do other stuff in the meanwhile.

Finally, running things like a message queue in a blocking while-True loop is not only
embarrassing, but also expensive. You pay for every SQS API request, which means
every time your code asks for new messages in a loop. Instead, AsyncAWS would
make a long-polling request and wait. It will only re-connect when a message comes,
or when SQS drops the connection to force you to pay at least something :)


Minimal working example
+++++++++++++++++++++++

You need to define main function as a coroutine and schedule it in IOLoop.
Here is code that creates an SQS queue and sends a message to it:

.. literalinclude:: /../examples/minimal.py

FAQ
---

Why yet another Python AWS library, if there is Boto?
    Because Boto is blocking, and asynchronous IO rocks.

What's the difference?
    For example, you can set asynchronous callbacks for incoming SQS messages, and forget about polling in a while-True loop.

But this lib is so small, mostly SQS-related stuff...
    Currently AsyncAWS implements only SQS and SNS, because those are most critical parts that HAVE to be async.
    For the rest, there still is Boto. They live together perfectly well.

Any plans to implement other AWS APIs?
    I do my best to add new methods regularly, but it's quite fast and simple so you can contribute as well.
    The most unpleasant part was to create a base `AWSRequest` class
    that implements all crazy hashing & signing stuff required by AWS, and it's done.
    Implementing new APIs is mostly copy-and-paste of parameters.

Why does this library rely on Tornado?
    Because Tornado has most mature async tools and ioloop for Python 2 and 3. Asyncio support is also planned.

Can't we just use AWS HTTP API directly using requests/urllib/etc?
    We can, but the overhead of building, hashing and signing canonical HTTP requests will be huge.
    Even GET params should be sorted alphabetically. And this lib will do it all for you.

Development and contributions
+++++++++++++++++++++++++++++

AsyncAWS is developed on Github:  https://github.com/MA3STR0/AsyncAWS

Code is maximally PEP8-compliant, well-documented and easy to read, welcoming
everyone to contribute and send pull requests.

AsyncAWS is extremely easy to extend, there are just 2 points I would kindly ask to follow:
  * Project currently scores 8.5 with Pylint, the goal is to keep it above 8.
  * Most of this documentation is auto-generated, so every public method should have a nice docstring.


The End.
++++++++

* :ref:`genindex`

