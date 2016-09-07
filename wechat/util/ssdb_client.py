# -*- coding: utf-8 -*-
from SSDB import SSDB
import time
import unittest

class SSDBClient(SSDB):
  def __init__(self, host, port):
    super(SSDBClient, self).__init__(host, port)

  def __del__(self):
    # 结束后断开连接
    self.close()

  def hset(self, table_name, key, value):
    res = self.request('hset', [table_name, key, value])
    return res.ok()

  def hget(self, table_name, key):
    res = self.request('hget', [table_name, key])
    return res.ok(), res.data

  def hdel(self, table_name, key):
    res = self.request('hdel', [table_name, key])
    return res.ok()

  def multi_hget(self, table_name, key_list):
    cmd_list = []
    cmd_list.append(table_name)
    cmd_list += key_list
    res = self.request('multi_hget', cmd_list)
    return res.ok(), res.data

  def multi_hdel(self, table_name, key_list):
    cmd_list = []
    cmd_list.append(table_name)
    cmd_list += key_list
    res = self.request('multi_hdel', cmd_list)
    return res.ok()

  def multi_hset(self, table_name, kv_dict):
    cmd_list = []
    cmd_list.append(table_name)
    for k in kv_dict:
      cmd_list.append(k)
      cmd_list.append(kv_dict[k])
    res = self.request('multi_hset', cmd_list)
    return res.ok()

  def set(self, key, value):
    res = self.request('set', [key, value])
    return res.ok()

  def setx(self, key, value, ttl):
    res = self.request('setx', [key, value, ttl])
    return res.ok()

  def setnx(self, key, value):
    res = self.request('setnx', [key, value])
    return res.ok(), res.data

  def expire(self, key, ttl):
    res = self.request('expire', [key, ttl])
    return res.ok(), res.data

  def get(self, key):
    res = self.request('get', [key])
    return res.ok(), res.data

  def getset(self, key, value):
    res = self.request('getset', [key, value])
    return res.ok(), res.data

  def incr(self, key, num):
    res = self.request('incr', [key, num])
    return res.ok(), res.data

  def exists(self, key):
    res = self.request('exists', [key])
    return res.ok()

  def getbit(self, key, offset):
    res = self.request('getbit', [key, offset])
    return res.ok(), res.data

  def setbit(self, key, offset, value):
    res = self.request('setbit', [key, offset, value])
    return res.ok(), res.data

  def bitcount(self, key, start, end):
    res = ssdb.request('bitcount', [key, start, end])
    return res.ok(), res.data

  def countbit(self, key, start, size):
    res = ssdb.request('countbit', [key, start, size])
    return res.ok(), res.data

  # (key_start, key_end] ("", ""]表示整个区间
  def keys(self, key_start, key_end, limit):
    res = ssdb.request('keys', [key_start, key_end, limit])
    return res.ok(), res.data

  # 获取key-value数组
  def scan(self, key_start, key_end, limit):
    res = ssdb.request('scan', [key_start, key_end, limit])
    return res.ok(), res.data

  def rscan(self, key_start, key_end, limit):
    res = ssdb.request('rscan', [key_start, key_end, limit])
    return res.ok(), res.data

  def multi_set(self, kv_dict):
    cmd_list = []
    cmd_list.append("multi_set")
    for key in kv_dict:
      cmd_list.append(key)
      cmd_list.append(kv_dict[key])
    res = ssdb.request("multi_set", cmd_list)
    return res.ok()

  def multi_get(self, key_list):
    cmd_list = []
    cmd_list.append("multi_get")
    cmd_list += key_list
    res = ssdb.request("multi_get", cmd_list)
    return res.ok(), res.data

  # TMD和python的del冲突了 只能大写
  def Del(self, key):
    res = self.request('del', [key])
    return res.ok()

  def ttl(self, key):
    res = self.request('ttl', [key])
    return res.ok(), res.data

  def zset(self, name, key, value):
    res = self.request('zset', [name, key, value])
    return res.ok()

  def zget(self, name, key):
    res = self.request('zget', [name, key])
    return res.ok(), res.data

  def zdel(self, name, key):
    res = self.request('zdel', [name, key])
    return res.ok()

  # 某个key增加num
  def zincr(self, name, key, num):
    res = self.request('zincr', [name, key, num])
    return res.ok()

class TestSSDBClient(unittest.TestCase):
  def setUp(self):
    self.ssdb_client = SSDBClient("127.0.0.1", 8888)

  def test_hset(self):
    ssdb_client = self.ssdb_client
    # hset
    self.assertTrue(ssdb_client.hset("test", "key", "value"))
    # hget
    status, data = ssdb_client.hget("test", "key")
    self.assertTrue(status, True)
    self.assertEqual(data, "value")
    # hdel
    self.assertTrue(ssdb_client.hdel("test", "key"))
    status, data = ssdb_client.hget("test", "key")
    self.assertFalse(status)
    self.assertEqual(data, None)
    # hget 不存在的key
    status, data = ssdb_client.hget("t", "key")
    self.assertFalse(status, False)
    self.assertEqual(data, None)

  def test_set(self):
    ssdb_client = self.ssdb_client
    # set
    self.assertTrue(ssdb_client.set("key", "value"))
    # get
    status, data = ssdb_client.get("key")
    self.assertTrue(status)
    self.assertEqual(data, "value")
    # del
    status = ssdb_client.Del("key")
    self.assertTrue(status)
    status, data = ssdb_client.get("key")
    self.assertFalse(status)
    self.assertEqual(data, None)

  def test_setx(self):
    ssdb_client = self.ssdb_client
    # setx
    self.assertTrue(ssdb_client.setx("key_ttl", "value", 1))
    status, data = ssdb_client.get("key_ttl")
    self.assertEqual((True, "value"), (status, data))
    # ttl
    status, data = ssdb_client.ttl("key_ttl")
    self.assertEqual((True, 1), (status, data))
    time.sleep(2)
    # 超过5s就找不到了
    status, data = ssdb_client.get("key_ttl")
    self.assertEqual((False, None), (status, data))

  def test_zset(self):
    ssdb_client = self.ssdb_client
    # zset
    self.assertTrue(ssdb_client.zset("key", "pv", 1))
    # zget
    status, data = ssdb_client.zget("key", "pv")
    self.assertEqual((True, 1), (status, data))
    # zincr
    self.assertTrue(ssdb_client.zincr("key", "pv", 1))
    status, data = ssdb_client.zget("key", "pv")
    self.assertEqual((True, 2), (status, data))
    # zdel
    self.assertTrue(ssdb_client.zdel("key", "pv"))
    status, data = ssdb_client.zget("key", "pv")
    self.assertEqual((False, None), (status, data))

if __name__ == '__main__':
  unittest.main()
