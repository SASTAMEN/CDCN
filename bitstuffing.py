l=[]
def bitstuffing(s):
    idx = 0
    cnt = 0
    f=0
    while idx < len(s):
        if s[idx] == '1':
            cnt += 1
            if cnt == 5:
                # Insert a '0' after five consecutive '1's
                s = s[:idx+1] + '0' + s[idx+1:]
                f+=1
                idx += 1
                cnt = 0
        else:
            cnt = 0
        idx += 1
    l.append(f)
    # Add flag bytes at the start and end
    s = '01111110' + s + '01111110'
    return s

def bitdestuffing(p):
    # Remove the flag bytes from the start and end
    p = p[8:-8]
    idx = 0
    cnt = 0
    while idx < len(p):
        if p[idx] == '1':
            cnt += 1
            if cnt == 5:
                # Remove the stuffed '0' following five consecutive '1's
                p = p[:idx+1] + p[idx+2:]
                cnt = 0
        else:
            cnt = 0
        idx += 1
    return p

# Main code
s = input("Enter the text: ")
s1 = ''
for i in range(len(s)):
    s1 += f'{ord(s[i]):08b}'

f_s = int(input("Enter the frame size: "))
if len(s1) % f_s != 0:
    s1 += ('0' * (f_s - len(s1) % f_s))
nn=len(s1)//f_s

print("Sender's Side:")
print("User text:"+s)
print("User Binary Data:")
for i in range(0,len(s1),f_s):
    print(s1[i:i+f_s])
print("After bit stuffing:")
stuffed_data = ''
i = 0
while i < len(s1):
    frame = s1[i:i+f_s]
    stuffed_frame = bitstuffing(frame)
    print(stuffed_frame)
    stuffed_data += stuffed_frame
    i += f_s

with open("bis.txt","w") as fp:
    fp.write(stuffed_data)
print("Receiver's Side:")
with open("bis.txt","r") as fpp:
    stuffed_dat=fpp.readline().strip()
# Adjust the frame size to include the added flag bytes (16 bits)
f_s += 16
fs=f_s
print("After Bit Destuffing:")
# Destuff the data
destuffed_data = ''
i = 0
j=0
while j < nn:
    if l[j]>0:
        fs+=l[j]
    else:
        fs=f_s
    j+=1
    frame = stuffed_dat[i:i+fs]
    destuffed_frame = bitdestuffing(frame)
    print(destuffed_frame)
    destuffed_data += destuffed_frame
    i += fs

# Convert the binary data back to text
res = ''
idx = 0
while idx < len(destuffed_data):
    byte = destuffed_data[idx:idx+8]
    if len(byte) == 8:
        res += chr(int(byte, 2))
    idx += 8

print("Text converted:", res)
