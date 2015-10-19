from urllib2 import Request, URLError, urlopen 
import re
import Queue
import threading

url = []
for i in xrange(100):
    url.append("http://www.ebay.com/itm/2-2015-John-Kennedy-Coin-And-Chronicles-Sets-IN-HAND-MINT-SEALED-UNOPENED-/161853021161?hash=item25af311be9:g:ae8AAOSwo6lWF8HW")

for i in xrange(20):
    url.append("http://www.ebay.com/itm/2015-Coin-and-Chronicles-Kennedy-Reverse-Proof-AX3-2-sets-MINT-SEALED-/201429224810?hash=item2ee61e0d6a:g:YB0AAOSwsB9V93Je")

def worker():
    while True:
        url = q.get()
        req = Request(url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            q.task_done()
            q.put(url)
            break
        except URLError as e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            q.task_done()
            q.put(url)
            break
        else:
            # everything is fine
            try:
                html = response.read()
            except:
                print 'The read is imcomplete'
                q.task_done()
                q.put(url)
                break
            else:    
                match1 = re.search(r'content="(US \$[\d.]+)', html)
                match2 = re.search(r'>\s*(US \$[\d.]+)\s*<', html)
                if match1 and match2 and match1.group and match2.group:
                    price_accepted = match1.group(1)
                    price_asked = match2.group(1)
                    print "The item had a Buy It Now price of %s and was sold at %s" % (price_asked, price_accepted)
                    q.task_done()
                else:
                    q.task_done()
                    q.put(url)
                    break

q = Queue.Queue()

for i in xrange(50):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


for j in url:
    q.put(j)

q.join()
