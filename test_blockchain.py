import unittest
from blockchain import Transaction, Block, Ledger, Blockchain
from hashmap import Hashmap


# Add
class TestBlockchain(unittest.TestCase):
    def test_transaction(self):
        tx = Transaction("Messi", "Ronaldo", 100)
        self.assertEqual(tx.__str__(), "Messi -> Ronaldo: 100")

    def test_ledger(self):
        ledger = Ledger()
        trans0 = Transaction("bank", "Messi", 500)
        ledger.add_transaction(trans0)
        self.assertTrue(ledger.has_funds("Messi", 500))
        self.assertFalse(ledger.has_funds("Messi", 3000))
        self.assertFalse(ledger.has_funds("Ronaldo", 10))

    def test_block_constructor(self):
        tx1 = Transaction("Messi", "Ronaldo", 100)
        tx2 = Transaction("Ronaldo", "Messi", 50)
        block = Block(transactions=[tx1, tx2])
        self.assertEqual(len(block.transactions), 2)

    def test_blockchain(self):
        Block = Block()
        self.assertEqual(len(Block.chain), 1)
        self.assertEqual(Block.last_block.hash, Block.chain[0].hash)

    def test_add_block(self):
        blockchain = Blockchain()
        trans1 = Transaction('Messi', 'Ronaldo', 100)
        block1 = Block([trans1])
        block1 = Block([trans1])
        blockchain.add_block(block1)
        self.assertEqual(len(Block.chain), 2)

    def test_add(self):
        hashmap = Hashmap()
        hashmap.add("Messi", 100)
        hashmap.add("Ronaldo", 50)
        self.assertEqual(hashmap.get("Messi"), [["Messi", 100]])
        # self.assertEqual(hashmap.map[hash("Ronaldo")], [["Ronaldo", 50]])


if __name__ == '__main__':
    unittest.main()