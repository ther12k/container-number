from config import IP, USERNAME, PASSWORD
from adam_io import Adam6050D, DigitalOutput

class Adam6060Output:
    def __init__(self):
        self.adam           = Adam6050D(IP, USERNAME, PASSWORD)
        self.initial_array  = [1,1,1,1,1,1]
        self.dig_out        = DigitalOutput(array=self.initial_array)
        
    def di_output(self, di=None):
        '''
        digital output adam,
        and convert digital output to bolean (True/False)
        Args:
            di = Optional -> 1,2,3,4,5,6
        return:
            output = True/False
            
        '''
        dig_in = self.adam.input(0)
        if dig_in[di-1] == 0: return False
        else: return True

    def di_outputs(self):
        '''
        digital output adam,
        and convert digital output to bolean (True/False)
        Args:
            di = Optional -> 1,2,3,4,5,6
        return:
            output = List[True/False]
        '''
        dig_in = self.adam.input(0)
        output = [False if i==0 else True for i in dig_in]
        return output