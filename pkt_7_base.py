#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_7_base
# Author: Barry Duggan
# Description: Baseband packet
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui

class pkt_7_base(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_7_base")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("pkt_7_base")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pkt_7_base")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.num_key = num_key = "packet_num"
        self.len_key = len_key = "packet_len"
        self.samp_rate = samp_rate = 32e3
        self.hdr_format = hdr_format = digital.header_format_crc(len_key, num_key)

        ##################################################
        # Blocks
        ##################################################
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(hdr_format)
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_pdu_to_tagged_stream_1 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(8, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(37,(75, 90, 49, 66, 76, 90, 32, 84, 104, 105, 115, 32, 105, 115, 32, 84, 101, 115, 116, 32, 81, 80, 83, 75, 32, 84, 114, 97, 115, 110, 109, 105, 115, 115, 105, 111, 110))), 10000)
        self.blocks_message_debug_0_1_0 = blocks.message_debug()
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/primeshp/gnuradio/test.iq', False)
        self.blocks_file_sink_0.set_unbuffered(True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.digital_crc32_async_bb_1, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.blocks_message_debug_0_1_0, 'print_pdu'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.blocks_message_debug_0_1_0, 'print_pdu'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.blocks_pdu_to_tagged_stream_1, 'pdus'))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_1, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_null_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pkt_7_base")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_num_key(self):
        return self.num_key

    def set_num_key(self, num_key):
        self.num_key = num_key
        self.set_hdr_format(digital.header_format_crc(self.len_key, self.num_key))

    def get_len_key(self):
        return self.len_key

    def set_len_key(self, len_key):
        self.len_key = len_key
        self.set_hdr_format(digital.header_format_crc(self.len_key, self.num_key))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format



def main(top_block_cls=pkt_7_base, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
