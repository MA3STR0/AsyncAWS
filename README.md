AsyncAWS
========

Asynchronous AWS library for Python
-----------------------------------

Why yet another Python AWS library, if there is Boto?
- Because Boto is blocking, and asynchronous IO rocks.

What's the difference?
- For example, we can set asynchronous callbacks for incoming SQS messages, and forget about polling in a while-True loop.

But this lib is so small, basically it's just SQS-related stuff!
- Right, currently AsyncAWS implements only SQS and SNS, because those are most critical parts that HAVE to be async. Running a message queue
in a blocking loop is nonsense, so it was changed as priority N1. For the rest, there is Boto. They live together perfectly fine.

- Any plans to implement other AWS APIs?
Sure, I add new methods when I need them, but it's very simple so you can do it yourself. Difficult part was to create a base request class
that implements all crazy signature rules required by AWS. It's done. Now to cover some new AWS API endpoint you just need to add a function that accepts
required params and adds them to AWSRequest with correct URL. All hashes and signatures will be added automatically.

Why should a library rely on Tornado?
- Because Tornado has the most mature async tools and ioloop for Python 2 and 3. But asyncio support is also planned.

Why can't we just use AWS HTTP API directly using my XY-framework?
- Because overhead of building, hashing and signing AWS-canonical HTTP requests is huge.
Even GET params should be sorted alphabetically. And this lib will do it all for you.
