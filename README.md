Tornado-AWS
===========

AWS Python library that plays well with Tornado IO loop
-------------------------------------------------------

Why yet another Python AWS library, if there is Boto?
- Because Boto is blocking, and asynchronous IO rocks.

Why should library rely on Tornado?
- Because Tornado is the most mature async web-framework for Python; by using it we can request AWS HTTP API asynchronously and benefit from non-blocking IO with cool features.

For example?
- We can define callbacks for SQS messages, and forget about polling in while-True loop

Then why can't I just use AWS HTTP API directly from my XY-framework?
- Becuase it's damn complicated. You can, but you don't want to. So I'll do it for you.

What is implemented so far
--------------------------

Currently only SQS handler can be used. It is under active development, so feel free to report bugs and suggestions.

Documentation
-------------

`SQSRequest` should be used to simplify AWS/SQS HTTP API requests, as it contains all necessary AWS-specific headers with checksums, signatures etc. Just write the request body, and headers will be auto-generated.
