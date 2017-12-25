

Introduction
============
<!-- History of the `fixbv`
  * Initial proposal
  * Initial pull-request
  * Decision to fully support
  * Google summer of code
  * Comments and feedback
-->


Moving forward
==============
The plan I proposing, is to move the `fixbv` to a separate repository,
the `fixbv` can be used for various modeling task but conversion is
currently limited.  With the `fixbv` in a separate repository we can
have greater interaction with other developers - in the future if we
ever to decide to and complete conversion in the myhdl.conversion the
code can be merged into the myhdl base.  The `fixbv` will be stuck in
the modeling mode for a bit longer - the `fixbv` as is supports conversion
but none of the automatic alignment, rounding, and overflow handling
will be automatically converted.

At this point the `fixbv` will remain as it is, it will be a bit-vector
type that checks for alignment but doesn't automatically perform alignment
etc.  This allows the `fixbv` to be converted like the `intbv`, to support
automatic alignment, rounding, overflow a new concept is proposed (see
next section).


Fixed-point domains
===================


```python
with clock_domain(clock, reset):
    a, b = FixedPoint(0, min=-8, max=8, prec=1/16))
    c = FixedPoint(0, min=-8, max=8, prec=1/32))
    c = a * b
```

<!-- What about Variables ??? -->


