import numpy as np
from gnuradio import gr
import pmt
 
class blk(gr.sync_block):
    def __init__(self,tracking_tag="start", length_tag="packet_len",length=512):
        gr.sync_block.__init__(self,name='Tagged Data Dump', in_sig=[np.uint8], out_sig=[np.uint8])
        self.tracking_tag =tracking_tag
        self.length_tag= length_tag
        self.length=length

    def work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))

        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            #value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            #offset= int(pmt.to_python(tag.offset))
            if (key==self.tracking_tag):
                #print('key:', key)
                #print('value:', value, type(value))
                #print("offset", tag.offset)
                #print('')
                #tx_key = pmt.intern("example_key")
                #tx_value = pmt.intern("example_value")
                self.add_item_tag(0, # Write to output port 0
                        tag.offset,
                        pmt.intern(self.length_tag),# Key of the tag
                        pmt.from_double(self.length), #Value of the tag
                )
                

        output_items[0][:] = input_items[0]
        return len(input_items[0])
