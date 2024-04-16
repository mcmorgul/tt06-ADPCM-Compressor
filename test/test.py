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

    slow_clock = Clock(dut.slow_clock, 80, units="us")
    cocotb.start_soon(slow_clock.start())  # Start the clock
    

    # Reset your module
    dut.block_enable.value = 0
    dut.pdm_in.value = 0  # Set pdm_in to 0 and maintain this throughout the test
    await ClockCycles(dut.clk, 5)
    dut.block_enable.value = 1
    await ClockCycles(dut.clk, 1)

    # Drive pdm_in to 0 for 16 clock cycles
    for _ in range(18):
        dut.pdm_in.value = 0
        await RisingEdge(dut.slow_clock)

    # After 16 cycles, keep monitoring the encPcm output for its MSB to go high
    while True:
        await RisingEdge(dut.slow_clock)
        if dut.encPcm.value.binstr[-1] == '1':  # Check if MSB of encPcm is high
            print("MSB of encPcm went high after the initial 16 clock cycles.")
            break



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
