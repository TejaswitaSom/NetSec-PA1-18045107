import random

# Input
# n - No. of rounds
# l - total length of block
# b - string representing block of size l
# k - string representing key of size l
# x - whether to change 1 bit in plaintext or 1 bit in key for avalanche effect


def run(n, l, b, k, x):
    # Generation
    def generate_init_permute_box(l):
        arr = list(range(1,l+1))
        random.shuffle(arr)
        return arr

    def generate_inv_init_permute_box(IP):
        invIP = []
        for i in range(1,len(IP)+1):
            invIP.append(IP.index(i, 0, len(IP)+1)+1)
        return invIP

    def generate_Ebox(z):
        Ebox = [z]
        for i in range(1,z):
            if i%4==0:
                Ebox.extend([i, i+1, i])
            else:
                Ebox.append(i)
        Ebox.extend([z,1])
        return Ebox

    def generate_Pbox(z):
        arr = list(range(1,z+1))
        random.shuffle(arr)
        return arr

    def generate_SBoxes(z):
        s = []
        for i in range(int(z/6)):
            lis = []
            for j in range(4):
                mylist = list(range(16))
                random.shuffle(mylist)
                lis.append(mylist)
            s.append(lis)
        return s

    def generate_permuted_choice1_box(l):
        pc = []
        for i in range(1,l+1):
            if i%8 != 0:
                pc.append(i)
        random.shuffle(pc)
        return pc

    def generate_permuted_choice2_box(actual_size, subkey_size):
        pc2 = random.sample(list(range(1,actual_size+1)), subkey_size)
        return pc2


    # Functions
    def create_diff_in1bit(a):
        final = ""
        indToBeChanged = random.randint(0, len(a)-1)
        final += a[:indToBeChanged]
        final += "1" if a[indToBeChanged]=="0" else "0"
        final += a[indToBeChanged+1:]
        return final

    def XOR(a, b):
        X = ""
        for i in range(len(a)):
            if a[i]==b[i]:
                X += "0"
            else:
                X += "1"
        return X

    def bin_to_deci(x):
        val = 0
        for i in range(len(x)):
            if x[len(x)-i-1]=='1':
                val += (2**i)
        return val

    def deci_to_bin(x):
        val = 0
        i = 0
        while x>0:
            val += (x%2)*(10**i)
            x  = int(x/2)
            i += 1
        final = ""
        if (val<10):
            final += ("000" + str(val))
        elif (10<= val <100):
            final += ("00" + str(val))
        elif (100<= val <1000):
            final += ("0" + str(val))
        else:
            final += str(val)
        return final

    def permute(a, arr):
        val = ""
        for i in arr:
            val += a[i-1]
        return val

    def left_shift(a, round_no, sch_leftshift):
        val = ""
        shift = sch_leftshift[round_no]
        val += (a[shift:] + a[:shift])
        return val

    def generate_round_keys(round_no, C, D, PC2, sch_leftshift):
        c = left_shift(C, round_no, sch_leftshift)
        d = left_shift(D, round_no, sch_leftshift)
        PC2_op = permute(c+d, PC2)
        return [PC2_op, c, d]

    def substitution(XF, S):
        s = ""
        a = int(len(XF)/6)
        for i in range(a):
            xr = XF[i*6] + XF[((i+1)*6)-1]
            xc = XF[(i*6)+1:((i+1)*6)-1]
            row = bin_to_deci(xr)
            column = bin_to_deci(xc)
            val = S[i][row][column]
            s += deci_to_bin(val)
        return s

    def find_difference(a, b, l):
        count = []
        for i in range(len(a)):
            c = 0
            for j in range(l):
                if a[i][j]!=b[i][j]:
                    c += 1
            count.append(c)
        return count



    # Main function
    def encrypt(n, l, b, k):

        cipher_per_round = []

        # Steps before round functions
        C = k[0:int(7*l/16)]
        D = k[int(7*l/16):int(7*l/8)]

        IP_op = permute(b,IP)
        L_prev = IP_op[0:int(l/2)]
        R_prev = IP_op[int(l/2):l]


        for i in range(n):
            # Round key generation with Ci and Di
            round_key = generate_round_keys(i, C, D, PC2, sch_leftshift)
            subkey = round_key[0]
            C = round_key[1]
            D = round_key[2]
            round_keys.append(C+D)

            # F block
            E_op = permute(R_prev, E)
            XF = XOR(subkey, E_op)
            S_op = substitution(XF,S)
            P_op = permute(S_op, P)
            
            L = R_prev
            R = XOR(L_prev, P_op)
            if i<n-1:
                cipher_per_round.append(L+R)

            L_prev = L
            R_prev = R
            

        result = R + L  # swapped addition
        InvIP_op = permute(result, InvIP)
        cipher_per_round.append(InvIP_op)

        return cipher_per_round



    # Generation of IP and IPinv
    IP = generate_init_permute_box(l)
    InvIP = generate_inv_init_permute_box(IP)
    # Generation of round boxes
    E = generate_Ebox(int(l/2))
    P = generate_Pbox(int(l/2))
    S = generate_SBoxes(int(3*l/4))
    # Generation of key boxes
    PC1 = generate_permuted_choice1_box(l)
    PC2 = generate_permuted_choice2_box(int(7*l/8), int(3*l/4))
    sch_leftshift = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    # Generate actual effective key
    Key_eff = permute(k,PC1)


    # Data for graph - To plot rounds vs diff_in_cipher and diff_in_key
    round_keys = []
    c1 = []  # ciphertext per round
    c2 = []  # ciphertext per round with altered plaintext or key
    diff_in_cipher = []
    data = []
    alteredtext = ""   # altered plaintext or key
    final_cipher = ""
    re_encrypted_plaintext = ""

    if x == 'p': # If avalanche effect is to be observed with only single change of bit in plaintext
        alteredtext = create_diff_in1bit(b)
        diff_in_cipher.append(1)
        c1.append(b)
        c1.extend(encrypt(n, l, b, Key_eff))
        c2.append(alteredtext)
        c2.extend(encrypt(n, l, alteredtext, Key_eff))
        diff_in_cipher.extend(find_difference(c1, c2, l)) 
    else: # If avalanche effect is to be observed with only single change of bit(not in parity bits) in key
        alteredtext = create_diff_in1bit(Key_eff)
        diff_in_cipher.append(0)
        c1 = encrypt(n, l, b, Key_eff)
        c2 = encrypt(n, l, b, alteredtext)
        diff_in_cipher.extend(find_difference(c1, c2, l))
    final_cipher = c1[len(c1) - 1]
    re_encrypted = encrypt(n, l, final_cipher, Key_eff)
    re_encrypted_plaintext = re_encrypted[len(re_encrypted)-1]

    data.append(diff_in_cipher)
    data.append(round_keys)
    data.append(c1)
    data.append(c2)
    data.append(Key_eff)
    data.append(alteredtext)
    data.append(b)
    data.append(re_encrypted_plaintext)
    
    return data