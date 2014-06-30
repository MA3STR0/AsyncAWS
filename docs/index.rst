.. include:: aws_links.txt

AsyncAWS - Asynchronous AWS library in Python
=============================================

.. toctree::
   :maxdepth: 2

   sqs
   sns

Why yet another Python AWS library, if there is Boto?
    Because Boto is blocking, and asynchronous IO rocks.

What's the difference?
    For example, you can set asynchronous callbacks for incoming SQS messages, and forget about polling in a while-True loop.

But this lib is so small, mostly SQS-related stuff...
    Currently AsyncAWS implements only SQS and SNS, because those are most critical parts that HAVE to be async. Running a message queue
    in a blocking loop is nonsense, so it was fixed as priority N1. For the rest, there still is Boto. They live together perfectly well.

Any plans to implement other AWS APIs?
    I try to add new methods regularly, but it's quite simple so you can do it yourself. The most unpleasant part was to create a base `AWSRequest` class
    that implements all crazy signature rules required by AWS, and it's done.

    To cover any new AWS API endpoint you only need to make a function that accepts
    some params and passes them to AWSRequest together with API base URL. All hashes and signatures will be added automatically.

Why does this library rely on Tornado?
    Because Tornado has most mature async tools and ioloop for Python 2 and 3. Asyncio support is also planned.

Can't we just use AWS HTTP API directly using requests/urllib/etc?
    We can, but the overhead of building, hashing and signing canonical HTTP requests will be huge.
    Even GET params should be sorted alphabetically. And this lib will do it all for you.


Still no luck? Try:
+++++++++++++++++++

* :ref:`genindex`
* :ref:`search`

