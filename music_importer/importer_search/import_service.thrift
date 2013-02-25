/**
 *
 *  bool        Boolean, one byte
 *  byte        Signed byte
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 */

namespace java com.baina.importer.search.service.thrift

enum ResultCode {
    SUCCESS = 0,
    FAIL = 1,
}

struct Meta {
    1:i32 song_id,
    2:string name,
    3:string album_name,
    4:string artist_name,
}

service SearchService {

    list<Meta> search(1:string query);
    
    ResultCode addDoc(1:Meta meta);
}