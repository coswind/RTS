'''
Created on Oct 12, 2011

@author: chzhong
'''
import hashlib
import hmac
import datetime
import time
import random
import bisect
import binascii

EPOCH = datetime.datetime(1970, 1, 1)
ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)
ONE_SECOND = datetime.timedelta(seconds=1)
ONE_DAY = datetime.timedelta(days=1)

class freeobject(object):
    '''An object that allows free attribute access without exception.
    '''

    def __init__(self, **kwargs):
        '''Initialize an object with free attributes like a JavaScript object.
        '''
        for key in kwargs:
            object.__setattr__(self, key, kwargs[key])


    def __getattr__(self, name):
        '''x.__getattribute__('name') <==> x.name, but returns None if name is not an attribute of this object.

        ``AttributeError`` will also be raise while accessing special methods/attributes (methdos/attributes that starts with ``__`` and ends with ``__``.
        '''
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name.startswith('__') and name.endswith('__'):
                raise

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

_boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                       '0': False, 'no': False, 'false': False, 'off': False}

def boolean(x):
    '''
    If x is None, returns False.
    If x is a basestring, and its content is one of (1, yes, true, on) in any case, returns True.
    If x is a basestring, and its content is one of (0, no, false, off) in any case, returns False.
    If x is not a basestring, returns bool(x).
    '''
    if not x:
        return False
    if isinstance(x, basestring):
        if x.lower() not in _boolean_states:
            raise ValueError, 'Not a boolean: %s' % x
        return _boolean_states[x.lower()]
    else:
        return bool(x)

def safe_float(s, default):
    '''Convert a string or number to an integer, if possible; otherwise ``default`` will be returned.
    '''
    if not isinstance(default, int):
        raise TypeError('the default value should be int')
    if not s:
        return default
    try:
        v = float(s)
    except:
        v = default
    return v

def safe_int(s, default):
    '''Convert a string or number to an integer, if possible; otherwise ``default`` will be returned.
    '''
    if not isinstance(default, int):
        raise TypeError('the default value should be int')
    if not s:
        return default
    try:
        v = int(s)
    except:
        v = default
    return v

def safe_long(s, default):
    '''Convert a string or number to an long integer, if possible; otherwise ``default`` will be returned.
    '''
    if not isinstance(default, (long, int)):
        raise TypeError('the default value should be long or int.')
    if not s:
        return default
    try:
        v = long(s)
    except:
        v = default
    return v

def string_encode(s, encoding='UTF-8'):
    if isinstance(s, unicode):
        s = s.encode(encoding)
    else:
        s = str(s)
    return s

def str_clip(s, max_len=48):
    cap = max_len / 2 - 4
    if len(s) > max_len:
        r = "%s...%s(length %d)" % (s[:cap], s[-cap:], len(s))
    else:
        r = s
    return r

def bytes_clip(s):
    s = binascii.hexlify(s)
    return str_clip(s, max_len=40)

def _checkoverflow(val, max_v):
    if abs(val) >= max_v:
        raise Exception('Value %d overflowed.' % val)

def dictize(obj):
    if isinstance(obj, dict):
        return obj
    attrs = dir(obj)
    d = {}
    for attr in attrs:
        if attr.startswith('__') and attr.endswith('__'):
            continue
        val = getattr(obj, attr)
        if callable(val):
            continue
        d[attr] = val
    return d

def model2dct(model):
    dct = {}
    for field in model._meta.get_all_field_names():
        value = getattr(model, field)
        if isinstance(value, int) or isinstance(value, long) or isinstance(value, float) or isinstance(value, unicode) or isinstance(value, str) or isinstance(value, bool):
            dct[field] = value
        if isinstance(value, datetime.datetime):
            dct[field] = value
            # dct[field] = int(time.mktime(value.timetuple()))
    return dct

def dict_encode(d, encoding):
    result = {}
    for k in d:
        v = d[k]
        # Encode the key
        if isinstance(k, unicode):
            k = k.encode(encoding)
        # Encode value
        if isinstance(v, unicode):
            v = v.encode(encoding)
        elif isinstance(v, dict):
            v = dict_encode(v, encoding)
        result[k] = v
    return result

def partial_update(dest, src, keys):
    for key in keys:
        if key in src:
            dest[key] = src[key]

def utf8(s):
    if not isinstance(s, basestring):
        try:
            s = str(s)
        except:
            s = repr(s)
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return s

def safe_typed(v, conv, default):
    try:
        return conv(v)
    except:
        return default

def utctoday():
    '''Returns current date time in UTC time zone.'''
    return utcnow().date()

def utcnow():
    '''Returns current date time in UTC time zone.'''
    return datetime.datetime.utcnow()

def today():
    '''Returns current date time in UTC time zone.'''
    return now().date()

def now():
    '''Returns current date time in local time zone.'''
    return datetime.datetime.now()

def unixnow():
    '''
    Returns current UNIX timestamp in milliseconds.
    '''
    return long(time.time() * 1000)

def datetime2timestamp(dt):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if isinstance(dt, datetime.datetime):
        timestamp = total_seconds(dt - EPOCH)
        return long(timestamp * 1000)
    return dt

def timestamp2datetime(timestamp):
    '''
    Converts UNIX timestamp in milliseconds to a datetime object.
    '''
    if isinstance(timestamp, (int, long, float)):
        return datetime.datetime.fromtimestamp(timestamp / 1000.0, utc)
    return timestamp

def total_seconds(delta):
    """Return total seconds of a time delta."""
    if not isinstance(delta, datetime.timedelta):
        raise TypeError('delta must be a datetime.timedelta.')
    return delta.days * 86400 + delta.seconds + delta.microseconds / 1000000.0

def unsigned(v, base=64):
    '''
    Convert a signed integer to unsigned integer of a given base.
    '''
    max_v = 1 << base
    _checkoverflow(v, max_v)
    if v < 0:
        v += max_v
    return v

def hashdigest(s, algorithm=None, hexlify=True):
    '''
    Return hash digest of a given string, using specified algorithm or default hash.
    '''
    if s is None:
        return None
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    if algorithm:
        l = algorithm() if callable(algorithm) else hashlib.new(algorithm)
        l.update(s)
        digest = l.hexdigest() if hexlify else False
    else:
        h = hash(s)
        digest = '%016x' % unsigned(h) if hexlify else h
    return digest

def md5(s, hexlify=True):
    '''
    Return md5 digest of a given string.
    '''
    return hashdigest(s, algorithm=hashlib.md5, hexlify=hexlify)

def sha1(s, hexlify=True):
    '''
    Return sha1 digest of a given string.
    '''
    return hashdigest(s, algorithm=hashlib.sha1, hexlify=hexlify)

def hmac_digest(key, msg, algorithm=None, hexlify=True):
    '''
    Return hash digest of a given string, using specified algorithm or default hash.
    '''
    key = key or ''
    if msg is None:
        return None
    if isinstance(key, unicode):
        key = key.encode('utf-8')
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
    if not algorithm:
        algorithm = hashlib.md5
    if isinstance(algorithm, basestring):
        algorithm = getattr(hashlib, algorithm)
    elif not callable(algorithm):
        raise TypeError('Algorithm must be either a hash method or name of the hash algorithm.')
    l = hmac.new(key, digestmod=algorithm)
    l.update(msg)
    digest = l.hexdigest() if hexlify else l.digest()
    return digest

def hmac_md5(key, msg, hexlify=True):
    '''
    Return md5 digest of a given string.
    '''
    return hmac_digest(key, msg, algorithm=hashlib.md5, hexlify=hexlify)

def hmac_sha1(key, msg, hexlify=True):
    '''
    Return sha1 digest of a given string.
    '''
    return hmac_digest(key, msg, algorithm=hashlib.sha1, hexlify=hexlify)

def random_string(char_dict, length):
    '''
    Generate a random string.
    '''
    return ''.join([random.choice(char_dict) for _ in range(length)])

def weighted_choice(seq, weights):
    '''Return a random element with given weights from the non-empty sequence seq.
    If seq is empty, raises IndexError.
    If weights is empty, return the result of choice(seq).
    '''
    if not seq:
        raise IndexError('seq must not be empty.')
    if not weights:
        return random.choice(seq)
    elif len(weights) != len(seq):
        raise ValueError('seq and weights must have the same length.')
    # http://rosettacode.org/wiki/Probabilistic_choice#Python
    prob_accumulator = 0
    accumulator = []
    for p in weights:
        prob_accumulator += p
        accumulator.append(prob_accumulator)
    r = random.random()
    return seq[bisect.bisect(accumulator, r)]

def weighted_sample(population, weights, k):
    '''Return a k length list of unique elements chosen from the population sequence. Used for random sampling without replacement.
    If population is empty, raises IndexError.
    If weights is empty, return the result of sample(population, k).
    '''
    if not population:
        raise IndexError('population must not be empty.')
    if k < 0:
        raise ValueError('k must be >= 0.')
    elif 0 == k:
        return []
    elif k >= len(population):
        return population
    if not weights:
        return random.sample(population, k)
    elif len(weights) != len(population):
        raise ValueError('population and weights must have the same length.')
    # http://en.wikipedia.org/wiki/Sampling_(statistics)#Probability_proportional_to_size_sampling
    prob_accumulator = 0
    accumulator = []
    for p in weights:
        prob_accumulator += p
        accumulator.append(prob_accumulator)
    step = 1 / k
    r = random.random() / k
    picked = []
    for _ in range(k):
        picked.append(population[bisect.bisect(accumulator, r)])
        r += step
    return picked

def json_encode_datetime(obj):
    #from bson.objectid import ObjectId
    if hasattr(obj, 'utctimetuple'):
        return datetime2timestamp(obj)
#    elif isinstance(obj, ObjectId):
#        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")

def mutable_copy(d):
    try:
        from django.http import QueryDict
        if isinstance(d, QueryDict):
            query = d.urlencode()
            mutable = QueryDict(query, mutable=True)
            return mutable
        return d
    except ImportError:
        return d

def get_real_gid(gid):
    import grp
    return int(gid) if gid.isdigit() else grp.getgrnam(gid).gr_gid

def get_real_uid(uid):
    import pwd
    return int(uid) if uid.isdigit() else pwd.getpwnam(uid).pw_uid

def compare_version(ver1, ver2):
    vers1 = ver1.split(".")
    vers2 = ver2.split(".")
    for i in range(0, len(vers2)):
        if len(vers1) <= i:
            subver1 = 0.0
        else:
            subver1 = float("0." + vers1[i])
        subver2 = float("0." + vers2[i])
        if subver1 > subver2:
            return 1
        elif subver1 < subver2:
            return -1
    return 0


class flagDict(dict):
    def __setitem__(self, key, value):
        if not isinstance(key, (long, int)):
            raise TypeError('Only integer or long will be accepted as key.')
        dict.__setitem__(key, value)
    def __getitem__(self, key):
        if not isinstance(key, (long, int)):
            raise TypeError('Only integer or long will be accepted as key.')
        keys = reversed(sorted(self.keys()))
        for k in keys:
            if (key & k) == k:
                key = k
                break
        return dict.__getitem__(self, key)
    def __delitem__(self, key):
        if not isinstance(key, (long, int)):
            raise TypeError('Only integer or long will be accepted as key.')
        dict.__delitem__(self, key)
