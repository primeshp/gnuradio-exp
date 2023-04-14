#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_xmt_gr38_qpsk
# Author: Primesh Pinto
# Description: QPSK packet transmit using UHD (for GNURadio 3.8)
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import numpy
import packet_format_gr38


class pkt_xmt_gr38_qpsk(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_xmt_gr38_qpsk")

        ##################################################
        # Variables
        ##################################################
        self.usrp_rate = usrp_rate = 768000
        self.sps = sps = 2
        self.samp_rate = samp_rate = 48000
        self.rs_ratio = rs_ratio = 1.000
        self.qpsk = qpsk = digital.constellation_qpsk().base()
        self.msg = msg = "This is KC1BLZ. Gnuradio QPSK Testing"
        self.excess_bw = excess_bw = 0.35

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, -1)
        self.packet_format_gr38 = packet_format_gr38.blk(message=msg)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, 1.0/((usrp_rate/samp_rate)*rs_ratio))
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(9,[71,78,85,32,82,97,100,105,111])), 200)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.packet_format_gr38, 'PDU_in'))
        self.msg_connect((self.packet_format_gr38, 'PDU_out0'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.zeromq_pub_sink_0, 0))


    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_msg(self):
        return self.msg

    def set_msg(self, msg):
        self.msg = msg
        self.packet_format_gr38.message = self.msg

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw





def main(top_block_cls=pkt_xmt_gr38_qpsk, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
