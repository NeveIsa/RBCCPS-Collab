import requests
import time


lastVal = -1
while 1:
    try:
      r=requests.get("https://dweet.io/get/latest/dweet/for/sampy")
      val=r.json()['with'][0]['content']['brightness']
      val=int(val)
      if lastVal==val:
          print("Stale value: %s" % val)
          continue
      print (time.time(), val)
      lastVal = val
      import os
      os.system("python3 rabbit_pub.py %s" % val)
    except Exception as e:
      print("Exception: %s" % e)


