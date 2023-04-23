import numpy as np
from gnuradio import gr
import pmt
 
class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
 
    def work(self, input_items, output_items):
        for indx, sample in enumerate(input_items[0]): # Enumerate through the input samples in port in0
            if np.random.rand() > 0.95: # 5% chance this sample is chosen
                key = pmt.intern("example_key")
                value = pmt.intern("example_value")
                self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0) + indx, # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
                )
                 # note: (self.nitems_written(0) + indx) is our current sample, in absolute time
        output_items[0][:] = input_items[0] # copy input to output
        return len(output_items[0])