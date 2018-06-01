
Take away
=========

1. The `fixbv` will be in a separate repository.
2. Reverting to a simplified `fixbv` and `Fixed` objects, where
   the `fixbv` is simplified and `Fixed` is the fully functional
   fixed-point object.
3. A new conversion proposals instead of the direct conversion
   of the `fixbv` type via the myhdl converter / compiler.

[History](), [Moving forward](), [Fixed-point objects and types]()
[Fixed-point conversion]()

History
=======
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
will be automatically converted but rather *interfaces*, *blocks*, and
*functions* to support fixed-point operations.

At this point the `fixbv` will remain as it is, it will be a bit-vector
type that checks for alignment but doesn't automatically perform alignment
etc.  This allows the `fixbv` to be converted like the `intbv`, to support
automatic alignment, rounding, overflow a new concept is proposed (see
next section).


Fixed-point objects and types
=============================
The `fixbv` type will remain as originally proposed, limited
functionality that enforces `fixbv` aligment and overflow but does
not perform it.  This allows the `fixbv` type to be converted but
requires the use of additional functions etc. to perform rounding,
overflow etc.

The `fixbv` type
----------------

The following two examples show how the `fixbv` errors on alignment
issues.
<!-- EXAMPLE THAT FAILS: add/sub alignment error -->
```python
```

<!-- EXAMPLE THAT FAILS: assignment format error -->
```python
```

<!-- EXAMPLE THAT WORKS -->
```python
```


### Changes
There are a bunch of changes (for now) to simplify how the `fixbv`
is used and incorporate feedback and other things learned over the
many years this was first proposed.

#### Initial value and resolution
In attempts to break the hardware only thinking when working with
fixed-point (i.e. thinking in number of bits), originally there
was the desire to initialize and represent the fixed-type with
floating-point values (Pythons float, double prec).  This is nice
in some ways but as @???? point out there can be a loss of precision,
in other words some of the functions relied on the conversion to
doubles.  To avoid loss of precision, no conversion to `float`
will be implemented, when a real number representation is desired
a string will be created to prevent loss of precision, this is the
same with the initial value.  When creating a `fixbv` the initial
value can be an `int` or `str` (in the future maybe `decimal`,
the `str` will represent the real number to be encoded in the

#### Bit width definition
Removed the `tuple` definition, did this to remove mixed uses in
the get item.  To set the bit-width and format will require an
additional function call.

```python
# Same as intbv, creating a new type, like the following,
# defines the total number of bits, it will default to
# fixed-point format of (37, 0, 36)
x = fixbv(0)[37:]

# Next, need to define the integer word length or the fractional
# word length - if the default is not desired.
# fixbv.set_format(iwl, fwl, wl)
# wl = len(x); fwl = wl - iwl - 1
x.set_format(7)

# Third, the initial value might need to be set, if the default
# format is not the desired format, the initial instantiation
# can not be used.
x.set_value("2.71828")
```

Other wise this can be set by setting the `min`, `max`, and `res`
arguments:

```python
x = fixbv("2.71828", min=-8, max=8, res=100000)
```

Note, on setting the resolution, the fractional portion of the

The `Fixed` object
------------------


Fixed-point conversion
======================
As mentioned the `fixbv` is convertible, same as the `intbv` but
has limited utility - many fixed-point operations have to manually
be handled.  Eventually, as the myhdl transition solidifies
`fixbv` conversion will be added to the myhdl converter and more
functionality will be added to the `fixbv`.

In the short-term the `FixedPoint` object does all the stuff one
would like, and we can support some interesting conversion as
well.  To achieve conversion, without having to add conversion
we can create

To support full functionality modeling and conversion (more on the
conversion part later) a `Fixed` object exists that performs
the rounding and overflow.

<!-- EXAMPLE -->
```python
```

In general this is not converitble, you can not use a `Fixed`
object in an `always*` and convert it.


```python
with clock_domain(clock, reset) as cd:
    u = Fixed(0, min=-16, max=16, res=1/17
    w = Fixed(0, min=-8, max=8, res=1/16))
    v = Fixed(0, min=-8, max=8, res=1/16))

    # This will be converted
    y = (u + w) * v

print(y)
```

<!-- COMPLETE EXAMPLE -->
```python
import myhdl as hdl
from myhdl import Signal, intbv, always_comb

@hdl.block
def example_fixed_point(glbl, smpi, smpo):
    nbits = len(smpi.data)
    xi = Signal(fixbv(0)[nbits, 0, nbits-1])
    nbits = len(smpi.data)
    yo = Signal(fixbv(0)]

    # Fixed-point
    u = FixedPoint(0, min=-16, max=16, res=1/17
    w = FixedPoint(0, min=-8, max=8, res=1/16))
    v = FixedPoint(0, min=-8, max=8, res=1/16))
    y = FixedPoint(yo, min=-8, max=8, res=1/32))
    fx_insts = None


    # Assign the `intbv` to `fixbv` types and vise-versa
    @always_comb
    def beh_assign():
        xi.next = smpi.data
        smpo.data.next = yo


    with clock_domain(glbl.clock, glbl.reset) as cd begin
        y = (u + w) * v




```

<!-- What about Variables ??? -->


