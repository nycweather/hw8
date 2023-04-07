from hashmap import Hashmap
import hashlib
" In this section, I will be implementing an approach that allows the user to do the money transcation "
# Contains transcation that you are sending to the user.


class Transaction:
    def __init__(self, from_user, to_user, amount):
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount


    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.amount}"


"A block of transcations that are stored in the blockchain"

# In this section, I will basically try and implement a transcation for the user to implement.

class Block:
    def __init__(self, transactions, previous_hash=''):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

# Here I will be calculating the hashvalues. 
    def calculate_hash(self):
        return hashlib.sha256(str(self.timestamp).encode() + str(self.transactions).encode() + str(self.previous_hash).encode() + str(self.nonce).encode()).hexdigest()

    def generate_hash(self):
        block_contents = str(self.transactions) + \
            str(self.previous_hash) + str(self.nonce)
        block_hash = hashlib.sha256(block_contents.encode())
        return block_hash.hexdigest()
        
# Here we add the transcation we want for the user respectively. 
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.hash = self.generate_hash()


# def add_transaction(self, tx):
    # if hasattr(tx, 'sender') and tx.sender in self._ledger:
  #  self._ledger[tx.sender] -= tx.amount
    # s  # elf._ledger[tx.to_user] += tx.amount
    # self._transactions.append(tx)
    # else:
   # raise ValueError("Invalid transaction.")


class Ledger:
    def __init__(self):
        self._ledger = {"bank":10000}

    def add_transaction(self, transaction):
        sender = transaction.from_user
        receiver = transaction.to_user
        amount = transaction.amount

        if self.has_funds(sender, amount):
            self._ledger[sender] -= amount
            self._ledger[receiver] = self._ledger.get(receiver, 0) + amount
            return True

        return False

    def has_funds(self, user, amount):
        return self._ledger.get(user, 0) >= amount

    def get_balance(self, user):
        return self._ledger.get(user, 0)

    # def has_funds(self, user, amount):
    #     if user not in self._hashmap:
    #         return False
    #     balance = self._hashmap.get(user)
    #     return balance >= amount

# need to transfer the amount

class Blockchain():
    '''Contains the chain of blocks.'''
    #########################
    # Do not use these three values in any code that you write.
    _ROOT_BC_USER = "ROOT"            # Name of root user account.
    # Amoung of HuskyCoin given as a reward for mining a block
    _BLOCK_REWARD = 1000
    # Total balance of HuskyCoin that the ROOT user receives in block0
    _TOTAL_AVAILABLE_TOKENS = 999999
    #########################

    def __init__(self):
        self._blockchain = list()     # Use the Python List for the chain of blocks
        self._bc_ledger = Ledger()    # The ledger of HuskyCoin balances
        # Create the initial block0 of the blockchain, also called the "genesis block"
        self._create_genesis_block()

    # This method is complete. No additional code needed.
    def _create_genesis_block(self):
        '''Creates the initial block in the chain.
        This is NOT how a blockchain usually works, but it is a simple way to give the
        Root user HuskyCoin that can be subsequently given to other users'''
        trans0 = Transaction(self._ROOT_BC_USER,
                             self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)
        block0 = Block([trans0])
        self._blockchain.append(block0)
        self._bc_ledger.deposit(
            self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)

    # This method is complete. No additional code needed.
    def distribute_mining_reward(self, user):
        '''
        You need to give HuskyCoin to some of your users before you can transfer HuskyCoing
        between users. Use this method to give your users an initial balance of HuskyCoin.
        (In the Bitcoin network, users compete to solve a meaningless mathmatical puzzle.
        Solving the puzzle takes a tremendious amount of copmputing power and consuming a lot
        of energy. The first node to solve the puzzle is given a certain amount of Bitcoin.)
        In this assigment, you do not need to understand "mining." Just use this method to
        provide initial balances to one or more users.'''
        trans = Transaction(self._ROOT_BC_USER, user, self._BLOCK_REWARD)
        block = Block([trans])
        self.add_block(block)

    # TODO - add the rest of the code for the class here

    def add_block(self, block):
        prev_block = self._blockchain[-1]
        trans = block.transactions[-1]
        if self._bc_ledger.balance(trans.from_user) >= trans.amount:
            self._bc_ledger.transfer(
                trans.from_user, trans.to_user, trans.amount)
            block.previous_hash = prev_block.block_hash
            block.block_hash = block.hash()
            self._blockchain.append(block)
            return True
        return False

    def validate_chain(self):
        tampered_blocks = []
        for i in range(len(self._blockchain)):
            block = self._blockchain[i]
            if i == 0:
                continue
            previous_block = self._blockchain[i-1]
            expected_hash = self._calculate_block_hash(previous_block)
            if previous_block.hash != expected_hash:
                tampered_blocks.append(previous_block)
        return tampered_blocks