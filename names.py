from __future__ import print_function

import os
import yaml
import string

__all__ = ['allowed', 'valid']

blacklist = None

def names():
    '''
    Lazy-load the tree of names, and return them in an object.
    Of course, asterisks etc. cannot be resolved, you should use allowed() to
    check for a valid name.
    '''
    global blacklist
    if blacklist is None:
        # not yet loaded
        path = os.path.join(os.path.dirname(__file__), 'names.yaml')
        f = open(path, 'r')
        blacklist = yaml.safe_load(f)
        f.close()
    return blacklist

def valid(name, maxlength=None):
    '''
    Return the lowercase name if this name adheres to requirements, None
    otherwise.
    The requirements are:
      * only alphanumeric characters or dashes
      * no number at the start
      * no double dashes or dashes at the start or end of the name
      * no empty string
      * no string bigger than maxlength
    '''

    if not name:
        return None
    if maxlength is not None and len(name) > maxlength:
        return None
    name = name.lower()
    if name.endswith('-') or name.startswith('-') or '--' in name:
        return None
    if name[0] in string.digits:
        return None
    for c in name:
        if c not in string.digits+string.ascii_lowercase+'-':
            return None

    return name

def allowed(name, collection='all'):
    '''
    Return true if this name is allowed (e.g. not in the forbidden list,
    indicated by 'collection'), false otherwise.
    '''

    if not valid(name):
        return False

    blacklist = names()
    for forbidden in blacklist[collection]:
        if name.lower() == forbidden.lower():
            return False
        if forbidden.endswith('*'):
            # very primitive glob matching
            if name.lower().startswith(forbidden[:-1].lower()):
                return False
        if forbidden.startswith('/'):
            # reference to another collection
            if not allowed(name, collection=forbidden[1:]):
                return False

    # No match.
    return True

def test_valid():
    data = [
        ('jake', 32,   True),
        ('jake', None, True),
        ('jake', 3,    False),
        ('0a',   None, False),
        ('a0',   None, True),
        ('a',    None, True),
        ('a-',   None, False),
        ('-a',   None, False),
        ('a--a', None, False),
        ('a-a',  None, True),
        ('a.b',  None, False),
        ('a a',  None, False),
    ]

    success = True
    booleans = {
        True:  'allowed',
        False: 'disallowed',
    }
    for name, maxlength, expected in data:
        result = valid(name, maxlength) is not None
        if result != expected:
            success = False
            print('expected %-4s with maxlength %-4s to be %s, was %s' % (name, maxlength, booleans[expected], booleans[result]))

    return success

def test_allowed():
    data = [
        ('jake',        'all',  True), # random username
        ('Jake',        'all',  True),
        ('Jake.',       'all',  False),
        ('masdf',       'all',  True), # 'm', followed by 'asdf'
        ('user',        'all',  False),
        ('webmaster',   'all',  False),
        ('admin',       'all',  False),
        ('AdmiN',       'all',  False),
        ('test123',     'all',  False),
        ('tesT0',       'all',  False),
        ('systemd-abc', 'all',  False),
        ('postmaster',  'all',  False),
        ('postmaster',  'mail', False),
        ('postmaster',  'null', True),
        ('null',        'all',  False),
        ('',            'all',  False),
    ]
    success = True
    booleans = {
        True:  'allowed',
        False: 'disallowed',
    }
    for name, collection, expected in data:
        result = allowed(name, collection)
        if result != expected:
            success = False
            print('expected %-11s with collection %-4s to be %s, was %s' % (name, collection, booleans[expected], booleans[result]))

    return success

def selftest():
    test1 = test_valid()
    test2 = test_allowed()
    if test1 and test2:
        print('OK')
    else:
        print('FAIL')
        exit(1)

if __name__ == '__main__':
    selftest()
