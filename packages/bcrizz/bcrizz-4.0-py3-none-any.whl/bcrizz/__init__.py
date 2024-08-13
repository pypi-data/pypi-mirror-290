def pip():
    print(""" 
!pip install pycryptodome
"""
    )

def index():
    print("""          
          
Practical 1: (!!! USE Jupyter Notebook !!! )
1a) A simple client class that generates the private and public keys by using built-in Python RSA algorithm and test it.
1b) A transaction class to send & receive money and test it.
1c) Create multiple transactions and display them.
1d) Create a blockchain, a genesis block and execute it.
1e) Create a mining function and test it. 
    Add blocks to the miner and dump the blockchain.
                                     

Practical 2:
2a) Variable and Operators
2b) Loops
2c) Decision Making 
2d) Arrays 
2e) Enums
2f) Structs 
2g) Mappings
2h) Conversions, Ether Units, Special Variables.
2i) Strings

          
Practical 3:
3a) Functions
3b) Fallback Function
3c) Mathematical functions
3d) Cryptographic functions 
3e) Function Modifiers
3f) View and Pure Functions
3g) Function Overloading


Practical 4:
4a) Withdrawal Pattern
4b) Restricted Access
             
          
Practical 5: 
5a) Contracts and Inheritance
5b) Constructors
5c) Abstract Contracts
5d) Interfaces
         
          
Practical 6:
6a) Libraries
6b) Assembly
6c) Error handling 
6d) Events
          

Practical 7:
    Install hyperledger fabric
          
Practical 9: (IDLE recommended)         
    Demonstrate the use of Bitcoin API.

      
             
""")
    

def prog(num):
    if num =="1a":
        print(""" --- Pract 1a ---

!pip install pycryptodome

import Crypto
import binascii
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self):
        #Creating a random number for key
        random = Crypto.Random.new().read
        #Creating a new public key and private key
        self._private_key = RSA.generate(1024,random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


Demo = Client()
print(Demo.identity)                                          


        """)

    elif num =="1b":
        print(""" --- Pract 1b  ---
         
!pip install pycryptodome

import collections
import datetime
import binascii
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
    
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')



class Transaction: 
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
        
    def to_dict(self): 
        if self.sender == "Genesis": 
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return collections.OrderedDict({ 
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time})

    def sign_transaction(self): 
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')



def display_transaction(transaction):
    dict = transaction.to_dict()
    print ("Sender: \\n" + dict['sender'])
    print ('------------------------------------------------------------------')
    print ("Recipient: \\n" + dict['recipient'])
    print ('------------------------------------------------------------------')
    print ("Value: " + str(dict['value']))
    print ('------------------------------------------------------------------')
    print ("Time: " + str(dict['time']))
    print ('------------------------------------------------------------------')
    print ("Signature: \\n" + signature)
    print ('------------------------------------------------------------------')

    



Shlok = Client()
Jivesh = Client()

signature = Transaction(Shlok, Jivesh.identity, 5.0).sign_transaction()

display_transaction(Transaction(Shlok, Jivesh.identity, 5.0))
              
        """)
    
    elif num =="1c":
        print(""" --- Pract 1c  ---
         
!pip install pycryptodome

import collections
import datetime
import binascii
import Crypto
import hashlib
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA 
from Crypto.Signature import PKCS1_v1_5



class Client:
    def __init__(self): 
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random) #create private key
        self._public_key = self._private_key.publickey() #create public key
        self._signer = PKCS1_v1_5.new(self._private_key) #create digital signature
        
    @property 
    def identity(self): 
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    


 
class Transaction: #creating transaction
    def __init__(self, sender, recipient, value): # in python client used to create constructor
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
    def to_dict(self): #record identity
        if self.sender == "Genesis": #base block in blockchain
            identity = "Genesis"
        else:
            identity = self.sender.identity
            return collections.OrderedDict({ # inserting in oredered manner \ storing | nothing but an ordered dictionary
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time})

    def sign_transaction(self): # verify sender and converting into hash value
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')




def display_transaction(transaction):
    dict = transaction.to_dict()
    print ("Sender: \\n" + dict['sender'])
    print ('------------------------------------------------------------------')
    print ("Recipient: \\n" + dict['recipient'])
    print ('------------------------------------------------------------------')
    print ("Value: " + str(dict['value']))
    print ('------------------------------------------------------------------')
    print ("Time: " + str(dict['time']))
    print ('------------------------------------------------------------------')
    


transactions = []
Shlok = Client()
Jivesh = Client()
Shreyas = Client()
Himanshu = Client()
    


t1 = Transaction(Shlok, Jivesh.identity, 15.0)
t1.sign_transaction()
transactions.append(t1)

t2 = Transaction(Shreyas, Himanshu.identity,6.0)
t2.sign_transaction()
transactions.append(t2)
    
t3 = Transaction(Jivesh, Shlok.identity,2.0)
t3.sign_transaction()
transactions.append(t3)


for txn in transactions:
    display_transaction (txn)              
        """)
    
    elif num =="1d":
        print(""" --- Pract 1d  ---
         
!pip install pycryptodome

import collections
import datetime
import binascii
import Crypto
import hashlib
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA 
from Crypto.Signature import PKCS1_v1_5


class Client:
    def __init__(self): 
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random) 
        self._public_key = self._private_key.publickey() 
        self._signer = PKCS1_v1_5.new(self._private_key)         
    @property 
    def identity(self): 
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    


 
class Transaction: 
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
        
    def to_dict(self): 
        if self.sender == "Genesis": 
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return collections.OrderedDict({ 
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time})

    def sign_transaction(self): 
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
 

class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        #self.Nonce = ""        
    last_block_hash = ""


def blockchain (self):
        print ("Number of blocks in the chain: " + str(len (self)))
        for x in range (len(SampleCoins)):
            block_temp = SampleCoins[x]
            print ("block # " + str(x))
        for transaction in block_temp.verified_transactions:
            display_transaction (transaction)

def display_transaction(transaction):
    dict = transaction.to_dict()
    print ("Sender: " + dict['sender'])
    print ('------------------------------------------------------------------')
    print ("Recipient: \\n" + dict['recipient'])
    print ('------------------------------------------------------------------')
    print ("Value: " + str(dict['value']))
    print ('------------------------------------------------------------------')
    print ("Time: " + str(dict['time']))
    print ('------------------------------------------------------------------')

            



SampleCoins = []
Shlok = Client()
Jivesh = Client()



txn0=Transaction("Genesis",Shlok.identity,10)

block0=Block()
block0.previous_block_hash = None
#Nonce = None
block0.verified_transactions.append(txn0)

last_block_hash = hash(block0)




SampleCoins.append(block0)
blockchain(SampleCoins)
              
        """)
    
    elif num =="1e":
        print(""" --- Pract 1e  ---

!pip install pycryptodome


import collections
import datetime
import binascii
!pip install pycryptodome
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


class Client:
    def __init__(self):
        random=Crypto.Random.new().read
        self._private_key=RSA.generate(1024,random)
        self._public_key=self._private_key.publickey()
        self._signer=PKCS1_v1_5.new(self._private_key)
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')



class Transaction:
    def __init__(self,sender,recipient,value):
        self.sender=sender
        self.recipient=recipient
        self.value=value
        self.time=datetime.datetime.now()

    def to_dict(self):
        if self.sender=="Genesis":
            identity="Genesis"
        else:
            identity=self.sender.identity

        return collections.OrderedDict({
            'sender':identity,
            'recipient':self.recipient,
            'value':self.value,
            'time':self.time})
    def sign_transaction(self):
        private_key=self.sender._private_key
        signer=PKCS1_v1_5.new(private_key)
        h=SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')




import hashlib
def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()
def mine(message,difficulty=1):
    assert difficulty>=1
    prefix='1'*difficulty
    for i in range(1000):
        digest=sha256(str(hash(message))+str(i))
        if digest.startswith(prefix):
            print("after"+str(i)+"iterationsfoundnonce:"+digest)
            return digest


class Block:
    def __init__(self):
        self.verified_transactions=[]
        self.previous_block_hash=""
        self.Nonce=""
        



def display_transaction(transaction):

    dict=transaction.to_dict()
    print("sender : "+dict['sender'])
    print('-----')
    print("recipient : "+dict['recipient'])
    print('-----')
    print("value : "+str(dict['value']))
    print('-----')
    print("time : "+str(dict['time']))
    print('-----')



def dump_blockchain(self):
    print("Number of blocks in the chain :"+str(len(self)))
    for x in range(len(TPCoins)):
        block_temp=TPCoins[x]
        print("Block # "+str(x))
        for transaction in block_temp.verified_transactions:
            display_transaction(transaction)
            print('--------------')
            print('=====================================')




last_block_hash=""
TPCoins=[]
last_transaction_index=0
transactions=[]


Raja=Client()
Rani=Client()
Seema=Client()
Reema=Client()




t1=Transaction(Raja,Rani.identity,15.0)
t1.sign_transaction()
transactions.append(t1)

t2=Transaction(Raja,Seema.identity,6.0)
t2.sign_transaction()
transactions.append(t2)

t3=Transaction(Rani,Reema.identity,2.0)
t3.sign_transaction()
transactions.append(t3)

t4=Transaction(Seema,Rani.identity,4.0)
t4.sign_transaction()
transactions.append(t4)

t5=Transaction(Reema,Seema.identity,7.0)
t5.sign_transaction()
transactions.append(t5)

t6=Transaction(Rani,Seema.identity,3.0)
t6.sign_transaction()
transactions.append(t6)

t7=Transaction(Seema,Raja.identity,8.0)
t7.sign_transaction()
transactions.append(t7)

t8=Transaction(Seema,Rani.identity,1.0)
t8.sign_transaction()
transactions.append(t8)

t9=Transaction(Reema,Raja.identity,5.0)
t9.sign_transaction()
transactions.append(t9)

t10=Transaction(Reema,Rani.identity,3.0)
t10.sign_transaction()
transactions.append(t10)



#Miner1addsablock

block=Block()
for i in range(3):
    temp_transaction=transactions[last_transaction_index]
    #validatetransaction
    #if valid
    block.verified_transactions.append(temp_transaction)
    last_transaction_index+=1

block.previous_block_hash=last_block_hash
block.Nonce=mine(block,2)
digest=hash(block)
TPCoins.append(block)
last_block_hash=digest


#Miner2 adds a block

block=Block()
for i in range(3):
    temp_transaction=transactions[last_transaction_index]
    #validate transaction
    #if valid
    block.verified_transactions.append(temp_transaction)
    last_transaction_index+=1

block.previous_block_hash=last_block_hash
block.Nonce=mine(block,2)
digest=hash(block)
TPCoins.append(block)
last_block_hash=digest




#Miner3 adds a block

block=Block()
for i in range(3):
    temp_transaction=transactions[last_transaction_index]
    #validate transaction
    #if valid
    block.verified_transactions.append(temp_transaction)
    last_transaction_index+=1

block.previous_block_hash=last_block_hash
block.Nonce=mine(block,2)
digest=hash(block)
TPCoins.append(block)
last_block_hash=digest




dump_blockchain(TPCoins)


        """)

    elif num =="2a":
        print(""" --- Pract 2a  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract PrimitiveDataTypes {

    //state variables (global variable)
    uint8   a = 20; 
    uint256 b = 35;
    int     c = 10;
    int8    d = 3;

    bool    flag = true;
    address addr = 0xCA35b7d915458EF540aDe6068dFe2F44E8fa733c;
    
    // Operations in solidity

    uint public addition    = a + b;
    int  public subtraction = c - d;
    int  public multiply    = d * c;
    int  public division    = c / d;
    int  public moduloDiv   = c % d;
    int  public increment   = ++c;
    int  public decrement   = --d;

}
              
        """)
        
    elif num =="2b":
        print(""" --- Pract 2b  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Loop {

    function summation(uint n) public pure returns (uint) {
        uint sum = 0;
        for (uint i = 1; i <= n; i++) {
            sum += i;
        }
        return sum;
    }

    function sumWhile(uint n) public pure returns (uint) {
        uint sum = 0;
        uint i = 1;
        while (i <= n) {
            sum += i;
            i++;
        }
        return sum;
    }

    function sumDoWhile(uint n) public pure returns (uint) {
        uint sum = 0;
        uint i = 1;
        do {
            sum += i;
            i++;
        } while (i <= n);
        return sum;
    }


    
}              
        """)

    elif num =="2c":
        print(""" --- Pract 2c  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract decision{

    function even(uint n) public pure returns(bool){
        if(n%2==0){
            return true;
        }
        else{
            return false;
        }
    }
}
                            
        """)

    elif num =="2d":
        print(""" --- Pract 2d  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Arrays {

    // Declaring an array
    uint[] public array1 = [1, 2, 3, 4];
    
    function fetch(uint index) public view returns (uint) {
        require(index < array1.length, "Index out of bounds");
        return array1[index];
    }
}
              
        """)
    
    elif num =="2e":
        print(""" --- Pract 2e  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Enums{

    //Define enum
    enum week_days {Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday}
    week_days choice;

    function set_value() public {
      choice = week_days.Friday;
    }
 
    // Defining a function to
    // return value of choice
    function get_choice(
    ) public view returns (week_days) {
      return choice;
    }
}              
        """)
    
    elif num =="2f":
        print(""" --- Pract 2f  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Structs{

    //declaring a struct
    struct Book {
        string name;
        string writer;
        uint price;
        bool available;
    }

    Book book1;

    //set book details like this
    Book book2 = Book ("Harry Potter","J.K.Rowling",300,true);

    //set book details like this
    function set_book_detail() public {
    book1 = Book("Introducing Ethereum and Solidity","Chris Dannen",250, true);
    }

    function book1_info() public view returns (string memory, string memory, uint, bool) { 
        return(book2.name, book2.writer,book2.price, book2.available); 
    }

      function book2_info() public view returns (string memory, string memory, uint, bool) {
      return (book1.name, book1.writer, book1.price, book1.available);
   }

}              
        """)
    
    elif num =="2g":
        print(""" --- Pract 2g  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract maps{

    mapping (uint=>string) public roll_no;

    function set(uint keys, string memory value) public {
        roll_no[keys]=value;
    }
    
}              
        """)
    
    elif num =="2h":
        print(""" --- Pract 2h  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Conversion {

    uint   a = 5;
    uint8  b = 10;
    uint16 c = 15;

    function convert() public view returns (uint) {
        uint result = a + uint(b) + uint(c);
        return result;
    }

    // Demonstrating Ether Units
    function etherUnits() public pure returns (uint, uint, uint) {
        uint oneWei = 1 wei;
        uint oneEther = 1 ether;
        uint oneGwei = 1 gwei;
        return (oneWei, oneEther, oneGwei);
    }

    // Demonstrating Special Variables
    function specialVariables() public view returns (address, uint, uint) {
        address sender = msg.sender; // Sender of the message (current call)
        uint timestamp = block.timestamp; // Current block timestamp
        uint blockNumber = block.number; // Current block number
        return (sender, timestamp, blockNumber);
    }
}
              
        """)

    elif num =="2i":
        print(""" --- Pract 2i  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract StringExample {
    // State variable to store a string
    string public greeting = "Hello, ";

    // Function to concatenate strings
    function concatenate(string memory _name) public view returns (string memory) {
        return string(abi.encodePacked(greeting, " ",_name));
    }

    // Function to compare two strings
    function compareStrings(string memory _a, string memory _b) public pure returns (bool) {
        return keccak256(abi.encodePacked(_a)) == keccak256(abi.encodePacked(_b));
    }

    // Function to update the greeting
    function updateGreeting(string memory _newGreeting) public {
        greeting = _newGreeting;
    }
}
              
        """)
    
    elif num =="3a":
        print(""" --- Pract 3a  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Addition {

    int public input1;
    int public input2;
    
    function setInputs(int _input1, int _input2) public {
        input1 = _input1;
        input2 = _input2;
    }

    function additions() public view returns(int) {
        return input1 + input2;
    }

    function subtract() public view returns(int) {
        return input1 - input2;
    }
}
              
        """)

    elif num =="3b":
        print(""" --- Pract 3b  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract fallbackfn
{
    event Log(string func,address sender, uint value, bytes data);

    fallback() external payable{
        emit Log("fallback",msg.sender,msg.value,msg.data);
    }

    receive() external payable{
        emit Log("receive..",msg.sender,msg.value,"");
        //msg.data is empty hence no need to specify it and mark it as empty string
    }
}

              
        """)

    elif num =="3c":
        print(""" --- Pract 3c  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract MathOperations {
    // addMod computes (x + y) % k
    // mulMod computes (x * y) % k

    function computeMod() public pure returns (uint addModResult, uint mulModResult) {
        uint x = 3;
        uint y = 2;
        uint k = 6;
        addModResult = addmod(x, y, k);
        mulModResult = mulmod(x, y, k);
    }
}
              
        """)

    elif num =="3d":
        print(""" --- Pract 3d  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Crypto {
    function hash(string memory _text,uint _num,address _addr) public pure returns (bytes32) {
            return keccak256(abi.encodePacked(_text, _num, _addr));
            }

    function collision(string memory _text, string memory _anotherText)public pure returns (bytes32){
                return keccak256(abi.encodePacked(_text, _anotherText));
            }
}
        
 //hash is same for collision
 //0x5f38993891425af42a69bd3cbabdc916f093d4f444455134d4371f4ddd17bd08 - shlok shivkar
 //0x5f38993891425af42a69bd3cbabdc916f093d4f444455134d4371f4ddd17bd08 - shl okshivkar

//abc, defgh
//0x48624fa43c68d5c552855a4e2919e74645f683f5384f72b5b051b71ea41d4f2d

//ab, cdefgh
//0x48624fa43c68d5c552855a4e2919e74645f683f5384f72b5b051b71ea41d4f2d
                            
contract GuessTheWord {
    bytes32 public answer = 0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8;
    
    function guess(string memory _word) public view returns (bool) {
     return keccak256(abi.encodePacked(_word)) == answer;
    }
}


              
        """)

    elif num =="3e":
        print(""" --- Pract 3e  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract FunctionModifier{ 
    
    address public owner;
    uint public x = 100;
    bool public locked;

    constructor() {
        // Set the transaction sender as the owner of the contract.
        owner = msg.sender;
        }

        modifier onlyOwner() {
            require(msg.sender == owner, "Not owner");
            _;
            }

        modifier validAddress(address _addr) {
            require(_addr != address(0), "Not valid address");
            _;
            }

    function changeOwner(address _newOwner) public onlyOwner validAddress(_newOwner) {
        owner = _newOwner;
        }

        modifier noReentrancy() {
            require(!locked, "No reentrancy");
            locked = true;
            _;
            locked = false;
        }

    function decrement(uint i) public noReentrancy {
        x -= i;
        if (i > 1) {
            decrement(i - 1);
        }
    }
}              
        """)

    elif num =="3f":
        print(""" --- Pract 3f  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract ViewAndPure {
    uint public x = 1;

    // Promise not to modify the state.
    function addToX(uint y) public view returns (uint) {
        return x + y;
    }

    // Promise not to modify or read from the state.
    function add(uint i, uint j) public pure returns (uint) {
        return i + j;
    }
}              
        """)

    elif num =="3g":
        print(""" --- Pract 3g  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FunctionOverloading {
    // Function with one parameter
    function sum(uint a) public pure returns (uint) { return a + 10; }

    // Overloaded function with two parameters
    function sum(uint a, uint b) public pure returns (uint) { return a + b; }

    // Overloaded function with three parameters
    function sum(uint a, uint b, uint c) public pure returns (uint) { return a + b + c; }

    // Examples of calling overloaded functions
    function exampleUsage() public pure returns (uint, uint, uint) {
        uint result1 = sum(5);            // Calls the first sum function
        uint result2 = sum(5, 10);        // Calls the second sum function
        uint result3 = sum(5, 10, 15);    // Calls the third sum function

        return (result1, result2, result3);
    }
}
              
        """)

    elif num =="4a":
        print(""" --- Pract 4a  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract withdrawalPattern{
    address public richest;
    uint public mostSent;

    mapping (address=>uint) pendingWithdrawals;
    error NotEnoughEther();

    constructor() payable{
        richest = msg.sender;
        mostSent = msg.value;
    }

    function becomeRichest() public payable{
        if (msg.value <= mostSent) revert NotEnoughEther();
        pendingWithdrawals[richest] += msg.value;
        richest = msg.sender;
        mostSent = msg.value;
    }

    function withdraw() public {
        uint amount = pendingWithdrawals[msg.sender];
        pendingWithdrawals[msg.sender] = 0;
        payable (msg.sender).transfer(amount);
    }

}              
        """)

    elif num =="4b":
        print(""" --- Pract 4b  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;
contract AccessRestriction {

    address public owner = msg.sender;
    uint public creationTime = block.timestamp;
    
    error Unauthorized();
    error TooEarly();
    error NotEnoughEther();
    
    modifier onlyBy(address account){
        if (msg.sender != account)
        revert Unauthorized();
        _;
    }

    modifier costs(uint amount) {
        if (msg.value < amount)
            revert NotEnoughEther();
            _;
        if (msg.value > amount)
            payable(msg.sender).transfer(msg.value - amount);
    }

    modifier onlyAfter(uint time) {
        if (block.timestamp < time)
            revert TooEarly();
            _;
    }

    function changeOwner(address newOwner)public onlyBy(owner){
        owner = newOwner;
    }

    function disown()public onlyBy(owner) onlyAfter(creationTime + 6 weeks){
        delete owner;
    }

    function forceOwnerChange(address newOwner)public payable costs(20 ether){
        owner = newOwner;
        // just some example condition
        if (uint160(owner) & 0 == 1)
            return;
    }
}
              
        """)

    elif num =="5a":
        print(""" --- Pract 5a  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract C{

    uint private data;
    uint public info;


    constructor()  {
        info = 10;
        }

        function increment(uint a) private pure returns(uint){ 
            return a + 1; 
        }
        
        function updateData(uint a) public {
            data = a;
        }

        function getData() public view returns(uint) {
            return data;
        }
        function compute(uint a, uint b) internal pure returns (uint) {
            return a + b;
        }
}
        

        
contract D {

    function readData() public returns(uint) {
        C c = new C();
        c.updateData(7);
        return c.getData();
    }
}
                

contract E is C {

    uint private result;
    C private c;
    
    constructor()  {
        c = new C();
    }

    function getComputedResult() public {
        result = compute(3, 6);
    }

    function getResult() public view returns(uint) {
        return result; 
    }
}


              
        """)

    elif num =="5b":
        print(""" --- Pract 5b  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract constructors{

    string str;
    uint amount;

    constructor(){
        str  = "Shlok is learning Solidity";
        amount = 10;
    }

    function const()public view returns(string memory,uint){
        return (str,amount);
 
    }

}              
        """)

    elif num =="5c":
        print(""" --- Pract 5c  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

abstract contract Main {
    // Define an abstract function that can be overridden
    function add(uint a, uint b) public virtual pure returns (uint);
}

contract Adder is Main {
    // Override the add function from the Main contract
    function add(uint a, uint b) public override pure returns (uint) {
        return a + b;
    }
}
              
        """)

    elif num =="5d":
        print(""" --- Pract 5d  ---
         
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

interface adder{
    function add(uint a, uint b)external pure returns(uint);
}

contract adderContract is adder{
    function add(uint a, uint b)external pure returns(uint){
        return a+b;
    }
}
              
        """)

    elif num =="5d":
        print(""" --- Pract 5d  ---
              
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

interface adder{
    function add(uint a, uint b)external pure returns(uint);
}

contract adderContract is adder{
    function add(uint a, uint b)external pure returns(uint){
        return a+b;
    }
}

        """)

    elif num =="6a":
        print(""" --- Pract 6a  ---
              
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

library Search {
   function indexOf(uint[] storage self, uint value) internal view returns (uint) {
      for (uint i = 0; i < self.length; i++) {
         if (self[i] == value) {
            return i;
         }
      }
      return type(uint).max;

   }
}

contract Test {
   uint[] data;

   constructor() {
      data.push(1);
      data.push(2);
      data.push(3);
      data.push(4);
      data.push(5);
   }

   function isValuePresent() external view returns (uint) {
      uint value = 4;
      
      // Search if value is present in the array using Library function
      uint index = Search.indexOf(data, value);
      return index;
   }
}

library MathLibrary {
   function square(uint num) internal pure returns (uint) {
      return num * num;
   }
}

contract SquareContract {
   using MathLibrary for uint;

   function calculateSquare(uint num) external pure returns (uint) {
      return num.square();
   }
}
              
        """)
    
    elif num =="6b":
        print(""" --- Pract 6b  ---
              
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

library Sum {
   function sumUsingInlineAssembly(uint[] memory _data) public pure returns (uint sum) {
      for (uint i = 0; i < _data.length; ++i) {
         assembly {
            // Load the value from memory at the current index
            let value := mload(add(add(_data, 0x20), mul(i, 0x20)))
            // Add the value to the sum
            sum := add(sum, value)
         }
      }
      // Return the calculated sum
      return sum;
   }
}

contract Test {
   uint[] data;

   constructor() {
      data.push(1);
      data.push(2);
      data.push(3);
      data.push(4);
      data.push(5);
   }

   function sum() external view returns (uint) {
      return Sum.sumUsingInlineAssembly(data);
   }
}

        """)

    elif num =="6c":
        print(""" --- Pract 6c  ---
              
pragma solidity ^0.8.17;

contract ErrorHandlingExample {
    constructor() payable {
        // Allow the contract to receive Ether during deployment
    }

    function divide(uint256 numerator, uint256 denominator) external pure returns (uint256) {
        require(denominator != 0, "Division by zero is not allowed");
        return numerator / denominator;
    }

    function withdraw(uint256 amount) external {
        require(amount <= address(this).balance, "Insufficient balance");

        payable(msg.sender).transfer(amount);
    }

    
}

        """)
    
    elif num =="6d":
        print(""" --- Pract 6d  ---
              
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract EventExample {

    // Define an event
    event Deposit(address indexed from, uint256 amount);
    event Withdraw(address indexed to, uint256 amount);

    // Mapping to keep track of user balances
    mapping(address => uint256) public balances;

    // Function to deposit ether into the contract
    function deposit() public payable {
        require(msg.value > 0, "Must deposit more than 0 ether");

        // Update the balance
        balances[msg.sender] += msg.value;

        // Emit the Deposit event
        emit Deposit(msg.sender, msg.value);
    }

    // Function to withdraw ether from the contract
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // Update the balance
        balances[msg.sender] -= amount;

        // Transfer the ether
        payable(msg.sender).transfer(amount);

        // Emit the Withdraw event
        emit Withdraw(msg.sender, amount);
    }
}

        """)
    
    elif num =="7":
        print(""" --- Pract 7  ---
              

Step 1:
	git --version
	curl --version
	docker --version
	jq --version

Step 2: Create a new folder named fabric
	mkdir fabric
	cd fabric

Step 3: Download fabric samples
	curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && chmod +x install-fabric.sh

	./install-fabric.sh

Step 4: Navigate to test network directory
	ls
	cd fabric-samples
	ls
	cd test-network
	ls


Step 5: Remove any containers or artifacts and Up the network
	./network.sh down
	./network.sh up
	
	
Step 6:Create a channel
	./network.sh createChannel


Step 7: Deploy chaincode on peers and channel
	./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-javascript -ccl javascript


Step 8: Set the path for peer binary and config for core.yaml
	export PATH=${PWD}/../bin:$PATH
	export FABRIC_CFG_PATH=$PWD/../config/


Step 9: Set the environment variables to operate Peer as Org1
	export CORE_PEER_TLS_ENABLED=true
	export CORE_PEER_LOCALMSPID="Org1MSP"
	export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
	export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
	export CORE_PEER_ADDRESS=localhost:7051


Step 10: Command to initialize the ledger with assets
	peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"InitLedger","Args":[]}'


Step 11: Query the ledger
	peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'



Step 12: Transfer the asset
	peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"TransferAsset","Args":["asset6","Christopher"]}'





Step 13: Set the environment variables to operate Peer as Org2
	export CORE_PEER_TLS_ENABLED=true
	export CORE_PEER_LOCALMSPID="Org2MSP"
	export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
	export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
	export CORE_PEER_ADDRESS=localhost:9051



Step 14: Query the ledger
	peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset6"]}'


Step 15: Bring the network down
	./network.sh down



        """)

    elif num =="9":
        print(""" --- Pract 9  ---
              
import requests

# Task 1: Get information regarding the current block
def get_current_block_info():
    response = requests.get("https://blockchain.info/latestblock")
    block_info = response.json()
    print("Current block information:")
    print("Block height:", block_info['height'])
    print("Block hash:", block_info['hash'])
    print("Block index:", block_info['block_index'])
    print("Timestamp:", block_info['time'])


# Task 3: Get balance of an address
def get_address_balance(address):
    response = requests.get(f"https://blockchain.info/q/addressbalance/{address}")
    balance = float(response.text) / 10**8
    print("Balance of address", address, ":", balance, "BTC")

# Example usage
if __name__ == "__main__":
    # Task 1: Get information regarding the current block
    get_current_block_info()
    
    # Task 3: Get balance of an address
    address = "3Dh2ft6UsqjbTNzs5zrp7uK17Gqg1Pg5u5"
    get_address_balance(address)

        """)

    
    else:
        print("Invalid input")

#prog('2a')
#index()   
        