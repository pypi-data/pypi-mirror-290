from hashlib import sha256
from secrets import compare_digest
from datetime import datetime

import random
import math

import json


class _Block:
    """
        Block class for representing Block in BlockChain
    """
    def __init__(self , data, prev_hash , user_name, hash , is_fake:bool):
        if is_fake:
            self.data = data
            self.user_name = user_name
            self.hash = hash
            self.prev_hash = prev_hash
        else:
            self.data = data
            self.user_name = user_name
            self.hash = self.__make_hash(f'{data}{prev_hash}{datetime.now()}')
            self.prev_hash = prev_hash

        

    def __make_hash(self, data_to_hash):
        return sha256(data_to_hash.encode('utf-8')).hexdigest()

    def alter_data(self, data):
        self.data = data
        self.hash = self.__make_hash(data)

    def __str__(self):
        return f'Data : {self.data}\nHash : {self.hash}\nPrev Hash : {self.prev_hash}'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class BlockChain:

    def __init__(self):
        self.blocks = []


    def add_block(self,data,user_name):
        """Data : Data to insert into the block"""
        if len(self.blocks) > 0:
            prev_block = self.blocks[len(self.blocks) - 1]
            b = _Block(data=data , prev_hash=prev_block.hash ,user_name=user_name , hash="" ,is_fake=False)
            self.blocks.append(b)
        else:
            eb = _Block(data=data , prev_hash="",user_name=user_name , hash="" , is_fake=False)
            self.blocks.append(eb)



    def attack(self):
        """Simulates a attack on blockchain"""
        if len(self.blocks) <= 1:
            print("There are few blocks in the blockchain to attack")
            return

        c_index = math.floor(random.random() * len(self.blocks))
        current = self.blocks[c_index]
        current.alter_data("hacked!!!!")
        self.blocks[c_index] = current
        

        
    def check_integrity(self):
        """
        This method checks for any security issues in blockchain
        returns True if the check is passed returns False if the check failed
        """
        result = {}

        for i in range(1 , len(self.blocks)):
            current = self.blocks[i]
            prev = self.blocks[i - 1]
            result[compare_digest(current.prev_hash , prev.hash)] = i

        return False if False in result.keys() else True


    def print(self):
        for i in self.blocks:
            print('\n---------\n'+ i)
        

