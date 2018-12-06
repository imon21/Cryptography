def mult(x,y):
    binary = bin(y)[2:]
    i = 0
    sum = 0
    index = len(binary)-1
    while index >= 0:
        #print("index : "+str(index))
        if binary[index] == '1':
            sum = sum ^ (x << i)
        i = i + 1
        index = index - 1
    #print("sum = "+ str(sum))
    return sum

def mod(x,y):
    while len(bin(x)) >= len(bin(y)):
        lack = len(bin(x))-len(bin(y))
        x = x ^ (y << lack)
    return x

def modInvGF(number, divisor):
    if number == 0:
        return 0
    for i in range(0,256):
        a = mult(number , i)
        #print(str(number)+" * "+str(i)+" = "+str(a))
        b = mod(a,divisor)
        #print("b = " + str(b))
        if b == 1:
            return i

def mult2(number):
    number = int(number,16)
    number = number * 2
    if number > 255:
        number = number % 256
        number = number ^ 0x1B
    return number;

def mult3(number):
    number1 = mult2(number)
    number1 = number1 ^ int(number,16)
    return number1

def subByte(number):
    number = int(number,16)
    mi = modInvGF(number, 283)
    #print("first mi "+str(mi))
    mi = format(bin(mi)[2:],'0>8')
    #print("8 bit mi "+str(mi))
    mi = mi[::-1]
    #print("reverse of mi "+str(mi))
    b = []
    for ch in mi:
        b.append(int(ch))
    c = [1,1,0,0,0,1,1,0]
    sbox = []
    #print("b array "+str(b))
    for i in range(8):
        value = b[i]^b[(i+4)%8]^b[(i+5)%8]^b[(i+6)%8]^b[(i+7)%8]^c[i]
        sbox.append(value)
    #print("sbox = "+str(sbox))
    sc = ''
    for data in sbox:
        sc += str(data)
    sc = sc[::-1]
    sc = int(sc,2)
    return hex(sc)[2:]

def addRoundKey(plain, keytext):
    key = [[0 for i in range(4)] for j in range(4)]
    xorStore = [[0 for i in range(4)] for j in range(4)]
    index = 0
    for i in range(4):
        key[0][i] = keytext[index]
        index = index + 1
        key[1][i] = keytext[index]
        index = index + 1
        key[2][i] = keytext[index]
        index = index + 1
        key[3][i] = keytext[index]
        index = index + 1

    for i in range(4):
        xor = int(plain[i][0],16) ^ int(key[i][0],16)
        xorStore[i][0] = hex(xor)[2:]
        xor = int(plain[i][1],16) ^ int(key[i][1],16)
        xorStore[i][1] = (hex(xor)[2:])
        xor = int(plain[i][2],16) ^ int(key[i][2],16)
        xorStore[i][2] = (hex(xor)[2:])
        xor = int(plain[i][3],16) ^ int(key[i][3],16)
        xorStore[i][3] = (hex(xor)[2:])
    #for i in range(16):
     #   xor = int(plain,16) ^ int(key,16)
      #  xorStore.append(hex(xor)[2:])
        
    return xorStore

def shiftRow(array):
    newArray = [[0 for i in range(4)] for j in range(4)]
    newArray[0][0] = array[0][0]
    newArray[0][1] = array[0][1]
    newArray[0][2] = array[0][2]
    newArray[0][3] = array[0][3]
    newArray[1][0] = array[1][1]
    newArray[1][1] = array[1][2]
    newArray[1][2] = array[1][3]
    newArray[1][3] = array[1][0]
    newArray[2][0] = array[2][2]
    newArray[2][1] = array[2][3]
    newArray[2][2] = array[2][0]
    newArray[2][3] = array[2][1]
    newArray[3][0] = array[3][3]
    newArray[3][1] = array[3][0]
    newArray[3][2] = array[3][1]
    newArray[3][3] = array[3][2]

    return newArray
    
def mixColoumn(array):
    newArray = [[0 for i in range(4)] for j in range(4)]
    for j in range(0,4):
        newArray[0][j] = hex(mult2(array[0][j]) ^ mult3(array[1][j]) ^ int(array[2][j],16) ^ int(array[3][j],16))[2:]
        newArray[1][j] = hex(int(array[0][j],16) ^ mult2(array[1][j]) ^ mult3(array[2][j]) ^ int(array[3][j],16))[2:]
        newArray[2][j] = hex(int(array[0][j],16) ^ int(array[1][j],16) ^ mult2(array[2][j]) ^ mult3(array[3][j]))[2:]
        newArray[3][j] = hex(mult3(array[0][j]) ^ int(array[1][j],16) ^ int(array[2][j],16) ^ mult2(array[3][j]))[2:]
    return newArray

def funcG(A,j):
    Rcon = ['01','02','04','08','10','20','40','80','1B','36']
    
    B = []
    B.append(A[1])
    B.append(A[2])
    B.append(A[3])
    B.append(A[0])

    for i in range(4):
        B[i] = subByte(B[i])

    B[0]  = hex(int(B[0],16) ^ int(Rcon[j],16))[2:]

    return B

def keyExpansion(key):
    
    word = [None]*176
    for i in range(16):
        word[i] = key[i]
   
    for i in range(4,44):
        temp = []
        temp.append(word[4*i-4])
        temp.append(word[4*i-3])
        temp.append(word[4*i-2])
        temp.append(word[4*i-1])
        
        if i % 4 == 0:
            temp = funcG(temp, i//4-1)

        for j in range(4):
            word[4*i+j] = hex(int(word[4*(i-4)+j],16) ^ int(temp[j],16))[2:]
    #print("key = "+str(word))    
    return word

def transpose(array):
    newArray = [[0 for i in range(4)] for j in range(4)]
    for j in range(4):
        for i in range(4):
            newArray[i][j] = array[j][i]
    return newArray

def difference(array1, array2):
    #string1 = ''.join(array1)
    #string2 = ''.join(array2)
    count = 0
    for j in range(4):
        for i in range(4):
            int1 = int(array1[i][j],16)
            int2 = int(array2[i][j],16)
            bin1 = bin(int1)[2:]
            bin2 = bin(int2)[2:]
            bin1 = bin1.zfill(8)
            bin2 = bin2.zfill(8)

            for k in range(8):
                if bin1[k] != bin2[k]:
                    count = count + 1
    return count

keytext = open("key.txt","r").read()
keytext2 = open("key2.txt","r").read()
plaintext = open("plaintext.txt","r").read()
plaintext2 = open("plaintext3.txt","r").read()
key = []
key2 = []
pp2 = []
pp = []
for i in range(16):
    index = i * 2
    data = plaintext[index]+plaintext[index+1]
    pp.append(data)

for i in range(16):
    index = i * 2
    data = plaintext2[index]+plaintext2[index+1]
    pp2.append(data)
    
plain = [[0 for i in range(4)] for j in range(4)]
plain2 = [[0 for i in range(4)] for j in range(4)]

index = 0
for i in range(4):
        plain[0][i] = pp[index]
        plain2[0][i] = pp2[index]
        index = index + 1
        plain[1][i] = pp[index]
        plain2[1][i] = pp2[index]
        index = index + 1
        plain[2][i] = pp[index]
        plain2[2][i] = pp2[index]
        index = index + 1
        plain[3][i] = pp[index]
        plain2[3][i] = pp2[index]
        index = index + 1

print(plain)
print(plain2)
print("Difference = "+str(difference(plain,plain2)))
for i in range(16):
    index = i * 2
    data = keytext[index]+keytext[index+1]
    data2 = keytext2[index]+keytext2[index+1]
    key.append(data)
    key2.append(data2)
    

#for ch in keytext:
#    key.append(hex(ord(ch))[2:])
#print("key = "+str(key))

#print("keyexpand = "+str(keyExpansion(key)))
key = keyExpansion(key)
key2 = keyExpansion(key2)
#print("key = "+str(key))
addRound = addRoundKey(plain,key[:16])
addRound2 = addRoundKey(plain2,key2[:16])
print("Avalanche Effect in Key: ")
print(str(transpose(addRound)))
print(str(transpose(addRound2)))
print("Difference = "+str(difference(addRound,addRound2)))
for i in range(1,11):
    subArray = [[0 for ii in range(4)] for j in range(4)]
    subArray2 = [[0 for ii in range(4)] for j in range(4)]
    for j in range(4):
        subArray[j][0] = subByte(addRound[j][0])
        subArray[j][1] = subByte(addRound[j][1])
        subArray[j][2] = subByte(addRound[j][2])
        subArray[j][3] = subByte(addRound[j][3])
        subArray2[j][0] = subByte(addRound2[j][0])
        subArray2[j][1] = subByte(addRound2[j][1])
        subArray2[j][2] = subByte(addRound2[j][2])
        subArray2[j][3] = subByte(addRound2[j][3])
    shftarray = shiftRow(subArray)
    shftarray2 = shiftRow(subArray2)
    if i != 10:
        mixcolm = mixColoumn(shftarray)
        plain = mixcolm
        addRound = addRoundKey(plain,key[(i*16):((i+1)*16)])

        mixcolm2 = mixColoumn(shftarray2)
        plain2 = mixcolm2
        addRound2 = addRoundKey(plain2,key2[(i*16):((i+1)*16)])
    else:
        addRound = addRoundKey(shftarray,key[(i*16):((i+1)*16)])
        addRound2 = addRoundKey(shftarray2,key2[(i*16):((i+1)*16)])
    print("Avalanche Effect in Key: ")
    print(str(transpose(addRound)))
    print(str(transpose(addRound2)))
    print("Difference = "+str(difference(addRound,addRound2)))


#print("Cipher Text = "+str(addRound))
#print("Cipher Text2 = "+str(addRound2))
 
#for i in range(0,256):
 #   hh = subByte(i)
  #  print("for number "+str(i)+" hex: "+hex(i)[2:]+" sbox entry is "+str(subByte(i))+" which is in hex value: "+hex(hh)[2:])
