import sys
import base64
import time
import json
import uuid
import random
from ecdsa import SigningKey, NIST384p

import torndb

db = torndb.Connection("127.0.0.1", "csz", user="root", password="leile13506625118")

def main():
    i = random.randint(1,10)
    # sk_filename = sys.argv[1]
    sk_filename = "p" + str(i) + ".pem"
    sk = SigningKey.from_pem(open(sk_filename).read())
    i = random.randint(1, 10)

    receiver_filename = "p" + str(i) + ".pem"
    rec = SigningKey.from_pem(open(receiver_filename).read())
    amount = random.randint(1,20)

    vk = sk.get_verifying_key()
    sender = base64.b64encode(vk.to_string())
    receiver_key = rec.get_verifying_key()
    receiver = base64.b64encode(receiver_key.to_string())
    txid = uuid.uuid4().hex
    timestamp = time.time()

    transaction = {
        "txid": txid,
        "sender": str(sender, encoding="utf-8"),
        "receiver":str(receiver, encoding="utf-8"),
        "timestamp": timestamp,
        "amount": amount
    }
    print(transaction)
    signature = sk.sign(json.dumps(transaction).encode('utf-8'))
    data = {
        "transaction": transaction,
        "signature": str(base64.b64encode(signature), encoding="utf-8")
    }

    # try:
    assert vk.verify(signature, json.dumps(transaction).encode('utf-8'))
    db.execute("INSERT INTO transactions (data, txid, timestamp) VALUES (%s, %s, %s)", json.dumps(data), txid, int(timestamp))
    time.sleep(10)
    # except:
    #     pass


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(5)
