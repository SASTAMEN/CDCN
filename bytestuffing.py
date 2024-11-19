s=input("enter the message:")
user_data=s
f=0
l=0
while(l!=len(s)):
    if s[l]!=' ':
        l+=1
    else:
        temp=s[f:l]
        if temp=='flag' or temp=='esc':
            s=s[:f]+'esc '+s[f:]
            l+=4
        l+=1
        f=l
temp=s[f:l]
if temp=='flag' or temp=='esc':
    s=s[:f]+'esc '+s[f:]  
s='flag '+s+' flag'
print("sender's side:/n"+"user data:"+user_data+"\nafter byte stuffing:"+s)
with open('C:/Users/B317-CSE-Sys13/Desktop/bytestuffing.txt','w') as file:
    file.write(s)
with open('C:/Users/B317-CSE-Sys13/Desktop/bytestuffing.txt','r') as file:
    recieved_data=file.read()
s=recieved_data

f=0
l=0
prev=''
while(l!=len(s)):
    if s[l]!=' ':
        l+=1
    else:
        temp=s[f:l]
        if (temp=='flag' or temp=='esc'):
            if prev!='esc':
                s=s[:f]+s[l+1:]
                l-=(l-f+1)
            else:
                if temp=='esc':
                    temp='esc1'
        l+=1
        f=l
        prev=temp
temp=s[f:l]
if (temp=='flag' or temp=='esc'):
    if prev!='esc':
        s=s[:f]+s[l:]
print("receiver's side:/n"+"received data:"+recieved_data+"\nafter byte destuffing:"+s)
