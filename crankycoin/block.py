import hashlib
import time
import json
import pyscrypt

from config import *
from errors import *
import datetime 
import socket


class BlockHeader(object):

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


    def __init__(self, previous_hash, merkle_root, timestamp=None, nonce=0):
        self.version = config['network']['version']
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.timestamp = timestamp if timestamp is not None else time.time()
        # self.timestamp = timestamp if timestamp is None return 'Null' else time.time()
        # self.timestamp = time.time()
        #self.timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def myfunc(timestamp):
        if not timestamp: 
            return 'Null Value'
            

    def to_hashable(self):
        for v in 'version previous_hash merkle_root timestamp nonce'.split():
            if getattr(self, v) is None:
                print 'PANIC: %s is None' % v

        return "{0:0>8}".format(self.version, 'x') + \
            self.previous_hash + \
            "{0:0>8}".format(self.timestamp, 'x')  + \
            "{0:0>8}".format(self.nonce, 'x')
            

    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()},
                          sort_keys=True)

    def __repr__(self):
        return "<Block Header {}>".format(self.merkle_root)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class Block(object):

    transactions = []

    def __init__(self, index, transactions, previous_hash, timestamp=None, nonce=0):
        """
        :param index: index # of block
        :type index: int
        :param transactions: list of transactions
        :type transactions: list of transaction objects
        :param previous_hash: previous block hash
        :type previous_hash: str
        :param timestamp: timestamp of block mined
        :type timestamp: int
        """
        self._index = index
        self._transactions = transactions
        merkle_root = self._calculate_merkle_root()
        self.block_header = BlockHeader(previous_hash, merkle_root, timestamp, nonce)
        self._current_hash = self._calculate_block_hash()

        bc_header = '{}'.format(self._current_hash)

        bc_info = {}

        bc_info[bc_header] = {
            'index': index,
            'previous_hash': previous_hash,
            'transactions':{},
        }
        for num in range(0, len(transactions)):
            
            transac_info = {'{}'.format(num) : {'source': transactions[num].source, 'destination': transactions[num].destination, 'amount': transactions[num].amount}}
            bc_info[bc_header]["transactions"].update(transac_info)
            host = '137.198.12.190'
            # host =  '137.198.12.190'
            port = 5000

            ip = '10.0.2.15'
            # print(ip)
            #public_key = config['user']['public_key']
            # fullnode = FullNode(ip, public_key)
            s = socket.socket()
            s.bind((host, port))
            myaddr = '137.198.12.190'

            s.listen(1)
            c, addr = s.accept()
            # print(fullnode.add_node(host))
            # print ("Got Conecttion From: " + str(addr))
            #c.send(myaddr)
            data = c.recv(1024)
            print("\n\n\n\n")
            #print(fullnode.full_nodes)
            #fullnode.add_node(data)
            #config['network']['seed_nodes'].append(data)
            #update()
            #print(fullnode.full_nodes)
            #print("Node Added" + str(data))

        print("\n HI \n")
        bcinfo.update(bc_info)
        bcinfo.update(data)
        print("\n\n")
        print(bc_info)
        blockdata = "config/bcinfo.yaml"
        with open(blockdata, 'w') as f:
            yaml.dump(bcinfo, f)


    @property
    def index(self):
        return self._index

    @property
    def transactions(self):
        return self._transactions

    @property
    def current_hash(self):
        return self._calculate_block_hash()

    @property
    def hash_difficulty(self):
        difficulty = 0
        for c in self.current_hash:
            if c != '0':
                break
            difficulty += 1
        return difficulty

    def _calculate_block_hash(self):
        """
        :return: scrypt hash
        :rtype: str
        """
        header = self.block_header.to_hashable()
        hash_object = pyscrypt.hash(
            password=header,
            salt=header,
            N=1024,
            r=1,
            p=1,
            dkLen=32)
        return hash_object.encode('hex')

    def _calculate_merkle_root(self):
        if len(self._transactions) < 1:
            raise InvalidTransactions(self._index, "Zero transactions in block. Coinbase transaction required")
        #print("Transactions: " + str(self._transactions))
        merkle_base = [t.tx_hash for t in self._transactions]
        print("Merkle Base: " + str(merkle_base[0]))
        while len(merkle_base) > 1:
            temp_merkle_base = []
            for i in range(0, len(merkle_base), 2):
                if i == len(merkle_base) - 1:
                    temp_merkle_base.append(
                        hashlib.sha256(merkle_base[i]).hexdigest()
                    )
                else:
                    temp_merkle_base.append(
                        hashlib.sha256(merkle_base[i] + merkle_base[i+1]).hexdigest()
                    )
            merkle_base = temp_merkle_base
        return merkle_base[0]

    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()},
                          sort_keys=True)

    def __repr__(self):
        return "<Block {}>".format(self._index)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other