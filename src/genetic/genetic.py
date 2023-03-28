"""
Laurent Colpaert - Thesis 2022-2023
"""
import random

class Genetic():
    """
    Class Genetic : contain transformation function as well as crossover and mutation function
    """
    def __init__(self) -> None:
        self.state_params = ['--rwmB','','','','--attB','--repB']
        self.MAX_STATES = 4
        self.MAX_TRANS = self.MAX_STATES - 1
        self.ranges = {
            '--nstates': (1, self.MAX_STATES),
            '--sB': (0, 5),
            '--nB': (0, self.MAX_TRANS),
            '--nBxT': (0, self.MAX_TRANS),
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
        self.rwm = (1,100)
        self.att_rep = (0.0,500.0)
        self.tx = self.MAX_TRANS * ['--nBxT', '--cBxT', '--wBxT', '--pBxT' ]
        self.astate =  ['--sB','--nB'] + self.tx
        self.chain = ['--nstates'] + self.MAX_STATES * self.astate

    def bit_size(self,arange : tuple) -> int:
        """
        Compute the bit size of a range

        Args:
            -arange (tuple(int)): the range list 

        Returns:
            -int: the bit size 
        """
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

    def max_range(self,rangelist : tuple)-> int:
        """
        Compute difference between two value of a tuple

        Args:
            -rangelist (tuple(int)): the range list 

        Returns:
            -int: the maximum range
        """
        max_size = 0
        max_range = (0,0)
        for arange in rangelist:
            s = self.bit_size(arange)
            if(s>max_size):
                max_size = s
                max_range = arange

        return max_range

    def to_binary_string(self,num : int, size : int)-> str:
        """
        Transform an integer into a bit of size 'size'

        Args:
            -num (int): the integer to be transformed
            -size (int): the size of the bit string

        Returns:
            -str: the bit string
        """
        return "".join(str((int(num) >> i) & 1) for i in range(size-1, -1, -1))

    def twopoint_crossover(self,g1 : str,g2 : str) -> tuple:
        """
        Apply a two point crossover algorithm on two genotypes

        Args:
            -g1 (str): the first pfsm in the form of a genotype
            -g2 (str): the second pfsm in the form of a genotype

        Returns:
            -str: the first crossed pfsm in the form of a genotype
            -str: the second crossed pfsm in the form of a genotype
        """
        # Generate two random crossover points
        p1 = random.randint(0, len(g1) - 1)
        p2 = random.randint(0, len(g1) - 1)
        if p1 > p2:
            p1, p2 = p2, p1
        
        # Extract the substring between p1 and p2 from each string
        s1_crossover = g1[p1:p2]
        s2_crossover = g2[p1:p2]
        
        # Swap the substrings between the two strings
        g1 = g1[:p1] + s2_crossover + g1[p2:]
        g2 = g2[:p1] + s1_crossover + g2[p2:]
        return g1,g2

    def crossover(self,g1 : str,g2 : str,p : int) -> tuple:
        """
        Run a crossover function if a certain probability is reached

        Args:
            -g1 (str): the first pfsm in the form of a genotype
            -g2 (str): the second pfsm in the form of a genotype
            -p (int): the probability of flipping a bit

        Returns:
            -str: the first crossed pfsm in the form of a genotype
            -str: the second crossed pfsm in the form of a genotype
        """
        if random.random() < p:
            g1,g2 = self.twopoint_crossover(g1,g2)
        return g1,g2

    def mutate(self,g : str, p: int)-> str:
        """
        Mutate a genotype by changing it's bit randomly by following a probability p

        Args:
            -g (str): a pfsm in the form of a genotype
            -p (int): the probability of flipping a bit

        Returns:
            -str: a mutated pfsm in the form of a genotype 
        """
        mutated = ""
        for i in range(len(g)):
            if random.random() < p:
                # Toggle the bit at the current index
                mutated += "1" if g[i] == "0" else "0"
            else:
                mutated += g[i]
        return mutated

    def toGenotype(self,phenotype : str,verbose : bool = False) -> str:
        """
        Transform a phenotype into a genotype. 
        A genotype is a bit string that will be able to encode all the possible value of a given pfsm.

        It will loop over the variable chain which generate all the key of the longest possible pfsm
        For each of the key, it will read the phenotype and transform it into a binary.

        Args:
            -phenotype (str): a pfsm in the form of a phenotype
            -verbose (bool): allows to enable prints to help debugging

        Returns:
            -str: a pfsm in the form of a genotype (binary string)
        """
        geno = ''
        i = 0
        nstates = self.MAX_STATES
        ntrans = self.MAX_TRANS
        curB = -1
        curT = -1
        last_id = 100
        phenos = phenotype.split('--')[1:]
        for key in self.chain:
            elem = self.ranges[key]
            if(type(elem) == type(())):
                arange = elem
                datasize = self.bit_size(arange)
            else:
                arange = elem[last_id]
                datasize = self.bit_size(self.max_range(elem))

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

                if verbose:
                    print("-------------")
                    print("--key : ", key)
                    print("--pheno : ", phenos[0])
                    print("--range : ", arange)
                    # print("--bit : ", bit)
                if (type(arange[0])==type(1.0)):
                    bit_val = int(round((float(value) - arange[0]) / 0.01, 2)) % (max_value+1)
                else:
                    bit_val = int(round(int(value) - arange[0],2)) % (max_value+1)
                bit = self.to_binary_string(bit_val, datasize)

                if(key == '--sB'):
                    curB = curB + 1
                    ntrans = self.MAX_TRANS #reinitialise ntrans to pass condition until we know
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
                            max_value = max(self.rwm[1] - self.rwm[0],0)
                            bit_val = int(round(int(value) - self.rwm[0],2)) % (max_value+1)
                            bit = self.to_binary_string(bit_val, self.bit_size(self.rwm))
                            geno += bit
                            geno += '0' * (2 * self.bit_size(self.att_rep))
                        elif value == '4':
                            geno += '0' *  self.bit_size(self.rwm)
                            value = phenos[0].split()[1]
                            key_val = phenos[0].split()[0]
                            phenos.pop(0)
                            max_value = max(self.att_rep[1] - self.att_rep[0],0)
                            bit_val = int(round((float(value) - self.att_rep[0]) / 0.01, 2)) % (max_value+1)
                            bit = self.to_binary_string(bit_val, self.bit_size(self.att_rep))
                            geno += bit
                            geno += '0' *  self.bit_size(self.att_rep)
                        elif value == '5':
                            geno += '0' *  self.bit_size(self.rwm)
                            geno += '0' * self.bit_size(self.att_rep)
                            value = phenos[0].split()[1]
                            key_val = phenos[0].split()[0]
                            phenos.pop(0)
                            max_value = max(self.att_rep[1] - self.att_rep[0],0)
                            bit_val = int(round((float(value) - self.att_rep[0]) / 0.01, 2)) % (max_value+1)
                            bit = self.to_binary_string(bit_val, self.bit_size(self.att_rep))
                            geno += bit
                        else:
                            # Bit size of rwm att and rep
                            size = self.bit_size(self.rwm) + 2 * self.bit_size(self.att_rep)
                            geno += '0' * size
            else:
                geno +=  ''.join('0' for _ in range(datasize))
            i+=datasize
        return geno

    def toPhenotype(self,genome,verbose = False):
        """
        Transform a genotype into a phenotype. 
        A phenotype is the grammatical representation of a given pfsm.

        It will loop over the variable chain which generate all the key of the longest possible pfsm
        For each of the key, it will read the binary string and retrieve the value.

        -> This function was taken from the genetic algorithm of Pomodoro and adapted to the new grammatical rules
        Args:
            -genotype (str): a pfsm in the form of a genotype (binary string)
            -verbose (bool): allows to enable prints to help debugging

        Returns:
            -str: a pfsm in the form of a phenotype 
        """
        phenotype = ''
        i = 0
        nstates = self.MAX_STATES
        ntrans = self.MAX_TRANS
        curB = -1
        curT = -1
        last_id = 100
        for key in self.chain:
            elem = self.ranges[key]
            if(type(elem) == type(())):
                arange = elem
                datasize = self.bit_size(arange)
            else:
                arange = elem[last_id]
                datasize = self.bit_size(self.max_range(elem))
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
                if verbose:
                    print("-------------")
                    print("--key : ", key)
                    print("--bit_value : ", bit_val)
                    print("--range : ", max_value)
                    print("--value : ",val)
                    print(f'--att{curB} {val}' )
                if(key == '--nstates'):
                    nstates = val
                elif(key == '--sB'):
                    curB = curB + 1
                    ntrans = self.MAX_TRANS #reinitialise ntrans to pass condition until we know
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
                        key = self.state_params[last_id]
                    phenotype += key.replace('B',str(curB)).replace('T',str(curT)) + ' ' + str(val) + ' '
                    if key == '--sB':
                        if val == 0:
                            size = self.bit_size(self.rwm)
                            bit_val = int(genome[i+datasize:i+datasize+size],2)
                            max_value = max(self.rwm[1] - self.rwm[0],0)
                            val = round(self.rwm[0] + (bit_val % (max_value+1)), 2)
                            phenotype += f'--rwm{curB} {val}'
                        elif val == 4:
                            size = self.bit_size(self.att_rep)
                            offset = self.bit_size(self.rwm)
                            bit_val = int(genome[i+datasize + offset:i+datasize+offset+size],2)
                            max_value = max(self.att_rep[1] - self.att_rep[0],0)
                            val = round(self.att_rep[0] + (bit_val % (max_value+1)), 2) * 0.01
                            phenotype += f'--att{curB} {val}'    
                        elif val == 5:
                            size = self.bit_size(self.att_rep)
                            offset = self.bit_size(self.rwm) + self.bit_size(self.att_rep)
                            bit_val = int(genome[i+datasize + offset:i+datasize+offset+size],2)
                            max_value = max(self.att_rep[1] - self.att_rep[0],0)
                            val = round(self.att_rep[0] + (bit_val % (max_value+1)), 2) * 0.01
                            phenotype += f'--rep{curB} {val}'
                        datasize +=  self.bit_size(self.rwm) + 2 * self.bit_size(self.att_rep)
                        phenotype += " "
            i+=datasize
        return phenotype


def test_crossover():
    """
    Example of how to use the crossover function
    """
    genetic = Genetic()
    phenotype1 = "--nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"
    phenotype2 = "--nstates 4 --s0 2 --n0 2 --n0x0 2 --c0x0 3 --w0x0 2.53 --p0x0 4 --n0x1 1 --c0x1 0 --p0x1 0.28 --s1 4 --att1 3.57 --n1 3 --n1x0 1 --c1x0 4 --w1x0 6.31 --p1x0 8 --n1x1 0 --c1x1 2 --p1x1 0.84 --n1x2 1 --c1x2 3 --w1x2 19.49 --p1x2 7 --s2 4 --att2 3.54 --n2 1 --n2x0 1 --c2x0 0 --p2x0 0.95 --s3 0 --rwm3 51 --n3 2 --n3x0 1 --c3x0 4 --w3x0 0.60 --p3x0 7 --n3x1 2 --c3x1 1 --p3x1 0.77"
    
    g1 = genetic.toGenotype(phenotype1)
    g2 = genetic.toGenotype(phenotype2)
    print(genetic.toPhenotype(g2))
    g1,g2 = genetic.twopoint_crossover(g1,g2)

    print("Crossed over 1 : ",genetic.toPhenotype(g1,verbose = False))
    print("Crossed over 2 : ",genetic.toPhenotype(g2,verbose = False))

def test_mutate():
    """
    Example of how to use the mutate function
    """
    genetic = Genetic()
    phenotype1 = "--nstates 4 --s0 4 --att0 3.25 --n0 2 --n0x0 0 --c0x0 5 --p0x0 0.23 --n0x1 2 --c0x1 0 --p0x1 0.70 --s1 2 --n1 3 --n1x0 0 --c1x0 4 --w1x0 8.91 --p1x0 7 --n1x1 1 --c1x1 0 --p1x1 0.15 --n1x2 2 --c1x2 3 --w1x2 1.68 --p1x2 10 --s2 1 --n2 1 --n2x0 0 --c2x0 3 --w2x0 6.93 --p2x0 4 --s3 4 --att3 3.71 --n3 2 --n3x0 0 --c3x0 1 --p3x0 0.50 --n3x1 2 --c3x1 5 --p3x1 0.62"
    g = genetic.toGenotype(phenotype1)
    g = genetic.mutate(g,0.06)
    print("Mutated phenotype : ",genetic.toPhenotype(g))

if __name__ == "__main__":
    print("Test Genetic class")
    # test_crossover()
    # test_mutate()
