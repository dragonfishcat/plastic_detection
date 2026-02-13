import hashlib
import json
import time
import base64
import os


BLOCKCHAIN_FILE = "blockchain.json"


class Block:
    def __init__(self, index, timestamp, request_id, plastic_type, confidence, image_hash, verification_status, previous_hash):
        
        self.index = index
        self.timestamp = timestamp
        self.request_id = request_id
        self.plastic_type = plastic_type
        self.confidence = confidence
        self.image_hash = image_hash
        self.verification_status = verification_status
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()


    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "plastic_type": self.plastic_type,
            "confidence": self.confidence,
            "image_hash": self.image_hash,
            "verification_status": self.verification_status,
            "previous_hash": self.previous_hash
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "plastic_type": self.plastic_type,
            "confidence": self.confidence,
            "image_hash": self.image_hash,
            "verification_status": self.verification_status,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

        if not self.chain:
            self.create_genesis_block()
            self.save_chain()

    def create_genesis_block(self):
        genesis = Block(index=0, 
                        timestamp=time.time(), 
                        request_id="GENESIS", 
                        plastic_type="N/A", 
                        confidence=0.0, 
                        image_hash="0", 
                        verification_status="N/A", 
                        previous_hash="0")
        self.chain.append(genesis)

    def add_block_from_data(self, record):
        last_block = self.chain[-1]

        new_block = Block(
            index=len(self.chain),
            timestamp=record["timestamp"],
            request_id=record["request_id"],
            plastic_type=record["plastic_type"],
            confidence=record["confidence"],
            image_hash=record["image_hash"],
            verification_status=record["verification_status"],
            previous_hash=last_block.hash
        )

        self.chain.append(new_block)
        self.save_chain()

    def save_chain(self):
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=4)

    def load_chain(self):
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r") as f:
                data = json.load(f)
                self.chain = []

                for block_data in data:
                    block = Block(
                        block_data["index"],
                        block_data["timestamp"],
                        block_data["request_id"],
                        block_data["plastic_type"],
                        block_data["confidence"],
                        block_data["image_hash"],
                        block_data["verification_status"],
                        block_data["previous_hash"]
                    )
                    block.hash = block_data["hash"]
                    self.chain.append(block)
