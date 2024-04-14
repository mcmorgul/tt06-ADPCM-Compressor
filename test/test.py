# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_CIC_ADPCM_Wrapper(dut):
    # Create a 10us period clock on port 'clk'
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())  # Start the clock

    # Reset your module
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    # You can now drive signals like 'clk_enable' and 'filter_in'
    # For example, if you want to send a sequence of values:
    dut.clk_enable.value = 1
    for value in range(10):  # Replace with your actual data
        dut.filter_in.value = BinaryValue(value)
        await RisingEdge(dut.clk)

    # Here you can add checks for 'outValid' and 'outSamp' signals
    # For example, you can wait for 'outValid' to assert and then check 'outSamp'
    await RisingEdge(dut.outValid)
    out_sample = dut.outSamp.value
    # Add your assertions here

# Run this testbench using the cocotb Makefile or by setting the appropriate environment variables.






#import cocotb
#from cocotb.clock import Clock
#from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_loopback(dut):
#     dut._log.info("Start")

#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1

#     # ui_in[0] == 0: Copy bidirectional pins to outputs
#     dut.ui_in.value = 0b0
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     for i in range(256):
#         dut.uio_in.value = i
#         await ClockCycles(dut.clk, 1)
#         assert dut.uo_out.value == i


# @cocotb.test()
# async def test_counter(dut):
#     dut._log.info("Start")

#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # ui_in[0] == 1: bidirectional outputs enabled, put a counter on both output and bidirectional pins
#     dut.ui_in.value = 0b1
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 2)

#     dut._log.info("Testing counter")
#     for i in range(256):
#         assert dut.uo_out.value == dut.uio_out.value
#         assert dut.uo_out.value == i
#         await ClockCycles(dut.clk, 1)
