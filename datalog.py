import rk_mcprotocol as mc
import time

HOST = '192.168.3.250'
PORT = 1025
s = ''
# try:
#     s = mc.open_socket(HOST,PORT) 
# except Exception as e:
#     print(f"Error connecting to PLC: {e}")

print(mc.write_sign_word(s,headdevice = 'd0' , data_list = [-999] ,signed_type =True))
print(mc.write_sign_word(s,headdevice = 'd1' , data_list = [36] ,signed_type =True))

d0 = mc.read_sign_word(s,headdevice = 'd0' , length = 1, signed_type=True)[0]
d1 = mc.read_sign_word(s,headdevice = 'd1' , length = 1, signed_type=True)[0]
print(mc.write_sign_word(s,headdevice = 'd2' , data_list = [d0+d1] ,signed_type =True))


while True :
    st = time.time()
    f = open('log.txt','a')
    f.write(f"{st} SM5500 {mc.read_sign_word(s,headdevice = 'SM5500' , length = 1, signed_type=True)} SM5501 {mc.read_sign_word(s,headdevice = 'SM5501' , length = 1, signed_type=True)} SM5502 {mc.read_sign_word(s,headdevice = 'SM5502' , length = 1, signed_type=True)} SM5503 {mc.read_sign_word(s,headdevice = 'SM5503' , length = 1, signed_type=True)} SD5502 {mc.read_sign_word(s,headdevice = 'SD5502' , length = 2, signed_type=True)} SD5542 {mc.read_sign_word(s,headdevice = 'SD5542' , length = 2, signed_type=True)} SD5582 {mc.read_sign_word(s,headdevice = 'SD5582' , length = 2, signed_type=True)} SD5622 {mc.read_sign_word(s,headdevice = 'SD5622' , length = 2, signed_type=True)} SD5504 {mc.read_sign_word(s,headdevice = 'SD5504' , length = 2, signed_type=True)} SD5544 {mc.read_sign_word(s,headdevice = 'SD5544' , length = 2, signed_type=True)} SD5584 {mc.read_sign_word(s,headdevice = 'SD5584' , length = 2, signed_type=True)} SD5624 {mc.read_sign_word(s,headdevice = 'SD5624' , length = 2, signed_type=True)}")
    f.close()
    print(f"SM5500 {mc.read_sign_word(s,headdevice = 'SM5500' , length = 1, signed_type=True)} SM5501 {mc.read_sign_word(s,headdevice = 'SM5501' , length = 1, signed_type=True)} SM5502 {mc.read_sign_word(s,headdevice = 'SM5502' , length = 1, signed_type=True)} SM5503 {mc.read_sign_word(s,headdevice = 'SM5503' , length = 1, signed_type=True)}")
    print(f"SD5502 {mc.read_sign_word(s,headdevice = 'SD5502' , length = 2, signed_type=True)} SD5542 {mc.read_sign_word(s,headdevice = 'SD5542' , length = 2, signed_type=True)} SD5582 {mc.read_sign_word(s,headdevice = 'SD5582' , length = 2, signed_type=True)} SD5622 {mc.read_sign_word(s,headdevice = 'SD5622' , length = 2, signed_type=True)}")
    print(f"SD5504 {mc.read_sign_word(s,headdevice = 'SD5504' , length = 2, signed_type=True)} SD5544 {mc.read_sign_word(s,headdevice = 'SD5544' , length = 2, signed_type=True)} SD5584 {mc.read_sign_word(s,headdevice = 'SD5584' , length = 2, signed_type=True)} SD5624 {mc.read_sign_word(s,headdevice = 'SD5624' , length = 2, signed_type=True)}")
    # print(mc.read_bit(s,headdevice = 'y0' , length = 8 ))   
    print(mc.read_sign_word(s,headdevice = 'd0' , length = 1, signed_type=True))
    print(mc.read_sign_word(s,headdevice = 'd1' , length = 1, signed_type=True))
    print(mc.read_sign_word(s,headdevice = 'd2' , length = 1, signed_type=True))
    # print(mc.read_sign_Dword(s,headdevice = 'r0' , length =480 , signed_type=True))      
    # print(mc.write_bit(s,headdevice = 'm0' , data_list = [1]*3584 )) 
    # print(mc.write_sign_word(s,headdevice = 'd0' , data_list = [-999] ,signed_type =True))
    # print(mc.write_sign_word(s,headdevice = 'd1' , data_list = [36] ,signed_type =True))
    # print(mc.write_sign_Dword(s,headdevice = 'r0' , data_list = [9999999]*480 ,signed_type =True))

    et = time.time()
    elapsed = et -st
    time.sleep(1)  
    
    print (f' elapsed time = {elapsed}')

