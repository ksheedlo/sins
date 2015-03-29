"""Errors for invalid sequence indices"""
# pylint: disable=too-few-public-methods, no-self-use

__revision__ = 0

TESTLIST = [1, 2, 3]
TESTTUPLE = (1, 2, 3)
TESTSTR = '123'

# getitem tests with bad indices
def function1():
    """list index is a function"""
    return TESTLIST[id]

def function2():
    """list index is None"""
    return TESTLIST[None]

def function3():
    """list index is a float expression"""
    return TESTLIST[float(0)]

def function4():
    """list index is a str constant"""
    return TESTLIST['0']

def function5():
    """list index does not implement __index__"""
    class NonIndexType(object):
        """Class without __index__ method"""
        pass

    return TESTLIST[NonIndexType()]

def function6():
    """Tuple index is None"""
    return TESTTUPLE[None]

def function7():
    """String index is None"""
    return TESTSTR[None]

def function8():
    """Index of subclass of tuple is None"""
    class TupleTest(tuple):
        """Subclass of tuple"""
        pass
    return TupleTest()[None]

# getitem tests with good indices
def function9():
    """list index is an int constant"""
    return TESTLIST[0]  # no error

def function10():
    """list index is a integer expression"""
    return TESTLIST[int(0.0)] # no error

def function11():
    """list index is a slice"""
    return TESTLIST[slice(1, 2, 3)] # no error

def function12():
    """list index implements __index__"""
    class IndexType(object):
        """Class with __index__ method"""
        def __index__(self):
            """Allow objects of this class to be used as slice indices"""
            return 0

    return TESTLIST[IndexType()] # no error

def function13():
    """list index implements __index__ in a superclass"""
    class IndexType(object):
        """Class with __index__ method"""
        def __index__(self):
            """Allow objects of this class to be used as slice indices"""
            return 0

    class IndexSubType(IndexType):
        """Class with __index__ in parent"""
        pass

    return TESTLIST[IndexSubType()] # no error

def function14():
    """Tuple index is an int constant"""
    return TESTTUPLE[0]

def function15():
    """String index is an int constant"""
    return TESTSTR[0]

def function16():
    """Index of subclass of tuple is an int constant"""
    class TupleTest(tuple):
        """Subclass of tuple"""
        pass
    return TupleTest()[0] # no error

def function17():
    """Index of subclass of tuple with custom __getitem__ is None"""
    class TupleTest(tuple):
        """Subclass of tuple with custom __getitem__"""
        def __getitem__(self, index):
            """Allow non-integer indices"""
            return 0
    return TupleTest()[None] # no error

def function18():
    """Index of subclass of tuple with __getitem__ in superclass is None"""
    class TupleTest(tuple):
        """Subclass of tuple with custom __getitem__"""
        def __getitem__(self, index):
            """Allow non-integer indices"""
            return 0

    class SubTupleTest(TupleTest):
        """Subclass of a subclass of tuple"""
        pass

    return SubTupleTest()[None] # no error

# Test with set and delete statements
def function19():
    """Set with None and integer indices"""
    TESTLIST[None] = 0
    TESTLIST[0] = 0 # no error

def function20():
    """Delete with None and integer indicies"""
    del TESTLIST[None]
    del TESTLIST[0] # no error

def function21():
    """Set and delete on a subclass of list"""
    class ListTest(list):
        """Inherit all list get/set/del handlers"""
        pass
    test = ListTest()

    # Set and delete with invalid indices
    test[None] = 0
    del test[None]

    # Set and delete with valid indices
    test[0] = 0 # no error
    del test[0] # no error

def function22():
    """Get, set, and delete on a subclass of list that overrides __setitem__"""
    class ListTest(list):
        """Override setitem but not get or del"""
        def __setitem__(self, key, value):
            pass
    test = ListTest()

    test[None][0] = 0 # failure on the getitem with None
    del test[None]

    test[0][0] = 0 # getitem with int and setitem with int, no error
    test[None] = 0 # setitem overridden, no error
    test[0] = 0 # setitem with int, no error
    del test[0] # delitem with int, no error

def function23():
    """Get, set, and delete on a subclass of list that overrides __delitem__"""
    class ListTest(list):
        """Override delitem but not get or set"""
        def __delitem__(self, key):
            pass
    test = ListTest()

    test[None][0] = 0 # failure on the getitem with None
    test[None] = 0    # setitem with invalid index

    test[0][0] = 0 # getitem with int and setitem with int, no error
    test[0] = 0 # setitem with int, no error
    del test[None] # delitem overriden, no error
    del test[0] # delitem with int, no error

def function24():
    """Get, set, and delete on a subclass of list that overrides __getitem__"""
    class ListTest(list):
        """Override gelitem but not del or set"""
        def __getitem__(self, key):
            pass
    test = ListTest()

    test[None] = 0 # setitem with invalid index
    del test[None] # delitem with invalid index

    test[None][0] = 0 # getitem overriden, no error
    test[0][0] = 0 # getitem with int and setitem with int, no error
    test[0] = 0 # setitem with int, no error
    del test[0] # delitem with int, no error

# Teest ExtSlice usage
def function25():
    """Extended slice used with a list"""
    return TESTLIST[..., 0]

def function26():
    """Extended slice used with an object that implements __getitem__"""
    class ExtSliceTest(object):
        """Permit extslice syntax by implementing __getitem__"""
        def __getitem__(self, index):
            return 0
    return ExtSliceTest[..., 0] # no error
