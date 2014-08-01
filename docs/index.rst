AsyncAWS - Asynchronous AWS library in Python
=============================================

.. toctree::
   :maxdepth: 2

   SQS Reference <sqs>
   SNS Reference <sns>


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


The End.
++++++++

* :ref:`genindex`

