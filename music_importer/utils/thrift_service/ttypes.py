#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class ResultCode:
  SUCCESS = 0
  FAIL = 1

  _VALUES_TO_NAMES = {
    0: "SUCCESS",
    1: "FAIL",
  }

  _NAMES_TO_VALUES = {
    "SUCCESS": 0,
    "FAIL": 1,
  }


class MetaBean:
  """
  Attributes:
   - song_id
   - name
   - album_name
   - artist_name
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'song_id', None, None, ), # 1
    (2, TType.STRING, 'name', None, None, ), # 2
    (3, TType.STRING, 'album_name', None, None, ), # 3
    (4, TType.STRING, 'artist_name', None, None, ), # 4
  )

  def __init__(self, song_id=None, name=None, album_name=None, artist_name=None,):
    self.song_id = song_id
    self.name = name
    self.album_name = album_name
    self.artist_name = artist_name

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.song_id = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.album_name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.artist_name = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('MetaBean')
    if self.song_id is not None:
      oprot.writeFieldBegin('song_id', TType.I32, 1)
      oprot.writeI32(self.song_id)
      oprot.writeFieldEnd()
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 2)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.album_name is not None:
      oprot.writeFieldBegin('album_name', TType.STRING, 3)
      oprot.writeString(self.album_name)
      oprot.writeFieldEnd()
    if self.artist_name is not None:
      oprot.writeFieldBegin('artist_name', TType.STRING, 4)
      oprot.writeString(self.artist_name)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)