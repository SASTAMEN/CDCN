def div(di,d):
    ans=''
    d=list(map(int,d))
    di=list(map(int,di))
    for i in range(len(d)-len(di)+1):
        if d[i]==1:
            for j in range(len(di)):
                d[i+j]^=di[j]
    d=d[-(len(di)-1):]
    return ''.join(map(str,d))
       
def tobi(di,x):
    for i in range(x[0],0,-1):
        if i in x:
            di+='1'
        else:
            di+='0'
    return di

print("Sender's side: ")
d=input('User Data: ')
t=input('Polynomial expression: ')
di=""
if t[-2:]=='+1':
    x=list(map(int,(t.replace('+',' ').replace('x',' '))[:-1].split()))
    di=tobi("",x)
    di+='1'
else:
    x=list(map(int,(t.replace('+',' ').replace('x',' ')).split()))
    di=tobi("",x)
    di+='0'
for _ in range(x[0]):
    d+='0'
r=div(di,d)
cw=d[:len(d)-len(di)+1]+r
print("Divisor: "+di)
print("CRC: "+r)
print('Code word: '+cw)
print("Receiver's side: ")

print('Case 1:')
rcw=cw
print("Received code word: "+rcw)
r=div(di,rcw)
print("Divisor: "+di)
print("Syndrome: "+r)
if '1' in r:
    print('Received code word has error, so it is discarded')
else:
    print('Received code word has no errors, so it is accepted')

print('Case 2:')
rcw=cw.replace('0','1',1)
print("Received code word: "+rcw)
r=div(di,rcw)
print("Divisor: "+di)
print("Syndrome: "+r)
if '1' in r:
    print('Received code word has error, so it is discarded')
else:
    print('Received code word has no errors, so it is accepted')
