REDIS

SET key value (EX secondsToLive)
GET key
EXISTS key
DEL key


// Counters (only for integer values)

INCR key                // increase by 1
INCRBY key 10           // increase by 10
DECR key                // decrease by 1
DECRBY key 10           // decrease by 10


// Expiry

EXPIRE key 120          // set key to expire in 120 seconds
PEXPIRE key 120         // set key to expire in 120 milliseconds
SET key value EX 120    // create key that will expire in 120 seconds
TTL key                 // time to live in seconds (-1 means key never expires, -2 means it has already expired)
PTTL key                // time to live in milliseconds
PERSIST key             // remove expiry; key becomes permanent


// Arrays

RPUSH key val1 (val2..) // push value(s) onto end (right side) of array (returns array length)
LPUSH key val1 (val2..) // push value(s) onto start (left side) of array (return array length)
RPOP key                // pop and return end value
LPOP key                // pop and return start value
LLEN key                // length of array
LRANGE key start Stop   // get array items within range [start, stop], to get entire array, use `LRANGE key 0 -1`


// Sets (no order, no duplicates, faster membership test - compared to lists)

SADD key val1 (val2..)  // add value(s) to set (returns 1 if value added, 0 if value already existed)
SREM key value          // remove value from set (returns 1 if value exists, 0 if did not exist)
SISMEMBER key value     // check if value is a member of the set
SMEMBERS key            // returns list of all members in the set
SUNION key1 key2 (...)  // combines 2+ sets and returns list of all elements
SPOP key num            // pop and return num # of elements from the set (random, since set is not ordered)
SRANDMEMBER key num     // return (but not pop) posNum # of elements from set (if num is negative, duplicates are allowed)


// Sorted sets (each member has an associated score)

ZADD hackers score value // add value to sorted set, with given score (int)
ZRANGE hackers start end // get array of items (sorted on score) within range [start, stop]


// Hashes (maps b/w string fields and string/numeric values)

HSET hashname key value  // store key-value info for hash specified by hashname
HMSET hashname key1 val2 key2 val2 ...  // set multiple values at once
HEXISTS hashname key     // check if key exists in hash
HGET hashname key        // get value specified by key for hash hashname
HGETALL hashname         // get list of all members of set, of format [key1, val1, key2, val2, ...]
HDEL hashname key        // delete key from hash
HINCRBY hashname key num // increase key's value (must be numeric) by num








ALL COMMANDS:
Please type HELP for one of these commands: DECR, DECRBY, DEL, EXISTS, EXPIRE, GET, GETSET, HDEL, HEXISTS, HGET, HGETALL, HINCRBY, HKEYS, HLEN, HMGET, HMSET, HSET, HVALS, INCR, INCRBY, KEYS, LINDEX, LLEN, LPOP, LPUSH, LRANGE, LREM, LSET, LTRIM, MGET, MSET, MSETNX, MULTI, PEXPIRE, RENAME, RENAMENX, RPOP, RPOPLPUSH, RPUSH, SADD, SCARD, SDIFF, SDIFFSTORE, SET, SETEX, SETNX, SINTER, SINTERSTORE, SISMEMBER, SMEMBERS, SMOVE, SORT, SPOP, SRANDMEMBER, SREM, SUNION, SUNIONSTORE, TTL, TYPE, ZADD, ZCARD, ZCOUNT, ZINCRBY, ZRANGE, ZRANGEBYSCORE, ZRANK, ZREM, ZREMRANGEBYSCORE, ZREVRANGE, ZSCORE
