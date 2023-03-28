import random


MAX_STATES = 4
MAX_TRANS = MAX_STATES - 1

ranges = {
    '--nstates': (1, MAX_STATES),
    '--sB': (0, 5),
    '--nB': (0, MAX_TRANS),
    '--nBxT': (0, MAX_TRANS),
    '--cBxT': (0, 5),
    '--pBxT': [
        (0.00, 100.00),
        (0.00, 100.00),
        (0.00, 100.00),
        (1, 10),
        (1, 10),
        (0.00, 100.00),
    ],
    '--wBxT': [(0, 0), (0, 0), (0, 0), (0.00, 2000.00), (0.00, 2000.00), (0, 0)],
}
rwm = (1,100)
att_rep = (0.0,500.0)

tx = MAX_TRANS * ['--nBxT', '--cBxT', '--wBxT', '--pBxT' ]
astate =  ['--sB','--nB'] + tx
chain = ['--nstates'] + MAX_STATES * astate


state_params = ['--rwmB','','','','--attB','--repB']

def bit_size(arange):
    range_size = arange[1] - arange[0] + 1
    #If it's a float, the values is suppose to be a range ?
    if(type(arange[0])==type(1.0)):
        range_size *= 100
    # print(arange, " , ",range_size)
    #Depending on the size of the range, return the size of the binary representation
    i = 0
    while(pow(2,i)<range_size):
        i+=1
    return i

def max_range(rangelist):
    max_size = 0
    max_range = (0,0)
    for arange in rangelist:
        s = bit_size(arange)
        if(s>max_size):
            max_size = s
            max_range = arange

    return max_range

def to_binary_string(num, size):
    return "".join(str((int(num) >> i) & 1) for i in range(size-1, -1, -1))

def genome_size():
    bit_count = 0
    for key in chain:
        arange = ranges[key]
        if(type(arange) != type(())):
            arange = max_range(arange)
        bit_count += bit_size(arange)
    return bit_count

def toGenotype(phenotype):
    geno = ''
    i = 0
    nstates = MAX_STATES
    ntrans = MAX_TRANS
    curB = -1
    curT = -1
    last_id = 100
    phenos = phenotype.split('--')[1:]
    for key in chain:
        elem = ranges[key]
        if(type(elem) == type(())):
            arange = elem
            datasize = bit_size(arange)
        else:
            arange = elem[last_id]
            datasize = bit_size(max_range(elem))

        if (arange[1]-arange[0]>0):
            if(key == '--nB'):
                arange = (arange[0],nstates-1)
            elif(key == '--nBxT'):
                arange = (arange[0],nstates-2) #substract two because max transitions is nstates-1 and because count starts at 0

            #Retrieve the value and transform it into a binary value
            if len(phenos) == 0:
                geno+='0'*datasize
                continue
            value = phenos[0].split()[1]
            key_val = phenos[0].split()[0]
            max_value = max(arange[1] - arange[0],0)
            if (type(arange[0])==type(1.0)):
                bit_val = int(round((float(value) - arange[0]) / 0.01, 2)) % (max_value+1)
            else:
                bit_val = int(round(int(value) - arange[0],2)) % (max_value+1)
            bit = to_binary_string(bit_val, datasize)

            if(key == '--sB'):
                curB = curB + 1
                ntrans = MAX_TRANS #reinitialise ntrans to pass condition until we know
                curT = -1
                last_id = int(value)
            elif(key == '--nB'):
                if 's' in key_val: # to fix empty state
                    geno += '0'*datasize
                    continue
                ntrans = int(value)
                if(ntrans == 0):
                    ntrans = -1 #doesn't pass condition below so that -nB 0 is not displayed
            elif(key == '--nBxT'):
                if 's' in key_val: # to fix empty state
                    geno += '0'*datasize
                    continue
                curT = curT + 1
            elif(key == '--cBxT'):
                if 's' in key_val: # to fix empty state
                    geno += '0'*datasize
                    continue
                last_id = int(value)
            elif(key == '--pBxT'):
                if 's' in key_val: # to fix empty state
                    geno += '0'*datasize
                    continue
            elif(key == '--wBxT'):
                if 's' in key_val: # to fix empty state
                    geno += '0'*datasize
                    continue

            if(nstates>curB and ntrans>curT):
                geno += bit
                phenos.pop(0)
                #Handle the option of a state
                if key == '--sB':
                    if value == '0':
                        value = phenos[0].split()[1]
                        key_val = phenos[0].split()[0]
                        phenos.pop(0)
                        max_value = max(rwm[1] - rwm[0],0)
                        bit_val = int(round(int(value) - rwm[0],2)) % (max_value+1)
                        bit = to_binary_string(bit_val, bit_size(rwm))
                        geno += bit
                        geno += '0' * (2 * bit_size(att_rep))
                    elif value == '4':
                        geno += '0' *  bit_size(rwm)
                        value = phenos[0].split()[1]
                        key_val = phenos[0].split()[0]
                        phenos.pop(0)
                        max_value = max(att_rep[1] - att_rep[0],0)
                        bit_val = int(round((float(value) - att_rep[0]) / 0.01, 2)) % (max_value+1)
                        bit = to_binary_string(bit_val, bit_size(att_rep))
                        geno += bit
                        geno += '0' *  bit_size(att_rep)
                    elif value == '5':
                        geno += '0' *  bit_size(rwm)
                        geno += '0' * bit_size(att_rep)
                        value = phenos[0].split()[1]
                        key_val = phenos[0].split()[0]
                        phenos.pop(0)
                        max_value = max(att_rep[1] - att_rep[0],0)
                        bit_val = int(round((float(value) - att_rep[0]) / 0.01, 2)) % (max_value+1)
                        bit = to_binary_string(bit_val, bit_size(att_rep))
                        geno += bit
                    else:
                        # Bit size of rwm att and rep
                        size = bit_size(rwm) + 2 * bit_size(att_rep)
                        geno += '0' * size
                print(key,nstates,curB,ntrans,curT)
        else:
            geno +=  ''.join('0' for _ in range(datasize))
        i+=datasize


    return geno

def toPhenotype(genome):
    phenotype = ''
    i = 0
    nstates = MAX_STATES
    ntrans = MAX_TRANS
    curB = -1
    curT = -1
    last_id = 100
    for key in chain:
        elem = ranges[key]
        if(type(elem) == type(())):
            arange = elem
            datasize = bit_size(arange)
        else:
            arange = elem[last_id]
            datasize = bit_size(max_range(elem))
        if(arange[1]-arange[0]>0):
            if(key == '--nB'):
                arange = (arange[0],nstates-1)
            elif(key == '--nBxT'):
                arange = (arange[0],nstates-2) #substract two because max transitions is nstates-1 and because count starts at 0
            
            bit_val = int(genome[i:i+datasize],2)
          
            mul = 1
            max_value = max(arange[1] - arange[0],0)
            if(type(arange[0])==type(1.0)):
                mul = 0.01
            
            val = round(arange[0] + (bit_val % (max_value+1))*mul, 2)
            if(key == '--nstates'):
                nstates = val
            elif(key == '--sB'):
                curB = curB + 1
                ntrans = MAX_TRANS #reinitialise ntrans to pass condition until we know
                curT = -1
                last_id = val
            elif(key == '--nB'):
                ntrans = val
                if(ntrans == 0):
                    ntrans = -1 #doesn't pass condition below so that -nB 0 is not displayed
            elif(key == '--nBxT'):
                curT = curT + 1
            elif(key == '--cBxT'):
                last_id = val
            if(nstates>curB and ntrans>curT):
                if(key == '--pB'):
                    key = state_params[last_id]
                phenotype += key.replace('B',str(curB)).replace('T',str(curT)) + ' ' + str(val) + ' '
                if key == '--sB':
                    if val == 0:
                        size = bit_size(rwm)
                        bit_val = int(genome[i+datasize:i+datasize+size],2)
                        max_value = max(rwm[1] - rwm[0],0)
                        val = round(rwm[0] + (bit_val % (max_value+1)), 2)
                        phenotype += f'--att{curB} {val}'
                    elif val == 4:
                        size = bit_size(att_rep)
                        offset = bit_size(rwm)
                        bit_val = int(genome[i+datasize + offset:i+datasize+offset+size],2)
                        max_value = max(att_rep[1] - att_rep[0],0)
                        val = round(att_rep[0] + (bit_val % (max_value+1)), 2) * 0.01
                        phenotype += f'--att{curB} {val}'    
                    elif val == 5:
                        size = bit_size(att_rep)
                        offset = bit_size(rwm) + bit_size(att_rep)
                        bit_val = int(genome[i+datasize + offset:i+datasize+offset+size],2)
                        max_value = max(att_rep[1] - att_rep[0],0)
                        val = round(att_rep[0] + (bit_val % (max_value+1)), 2) * 0.01
                        phenotype += f'--rep{curB} {val}'
                    datasize +=  bit_size(rwm) + 2 * bit_size(att_rep)
                    phenotype += " "
        i+=datasize
    return phenotype

if __name__ == "__main__":
    print("Test crossover")
    # random.seed(0)
    # genotype = ''.join([str(random.randint(0, 1)) for _ in range(genome_size())])
    # print(genotype)
    # genotype = "1101111110010010100110111011100010110100000100110110101101101000011000000110011111010110001001011000000000010100000010001010001110010010111000001101001111110010101001111011100010001110110010101100111101000011100000000110011001101010010000111011110011000111101001001110101001001111100111101011011001000000100111101010101010001001110000001110010111111000111001"
    # phenotype = toPhenotype(genotype)
    # print(chain)
    # print("---------")
    # print(phenotype)

    phenotype = "--nstates 4 --s0 4 --att 3.25 --n0 2 --n0x0 2 --c0x0 3 --p0x0 10 --w0x0 0.03 --n0x1 0 --c0x1 4 --p0x1 9 --w0x1 0.03 --s1 1 --s2 1 --n2 3 --n2x0 0 --c2x0 1 --p2x0 0.01 --n2x1 0 --c2x1 0 --p2x1 0.0 --n2x2 0 --c2x2 1 --p2x2 0.01 --s3 2"
    phenotype = "--nstates 4 --s0 0 --rwm0 9 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"
    phenotype = "--nstates 1 --s0 5 --rep0 1.69"
    slkjsdflk = "--nstates 4 --s0 0 --att0 9 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.7 --s1 2  --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1  --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.5 --n3x1 2 --c3x1 5 --p3x1 0.62 "
    geno = toGenotype(phenotype=phenotype)
    print("Genotype is \n",geno)
    print("Len genotype is \n",len(geno))
    print(toPhenotype(geno))
