import hashlib
import json
from time import time

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0', student_data={})

    def create_block(self, previous_hash, student_data):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(time()),
            'student_data': student_data,
            'previous_hash': previous_hash
        }

        block['hash'] = self.hash(block)

        self.chain.append(block)

        return block

    def hash(self, block):

        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block(self):
        return self.chain[-1]

