import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def tt_um_factory_test(dut):
    # Create clocks
    fast_clock = Clock(dut.clk, 10, units="us")  # Fast clock
    slow_clock = Clock(dut.ui_in[1], 80, units="us")  # Slow clock
    cocotb.start_soon(fast_clock.start())
    cocotb.start_soon(slow_clock.start())

    # Initial reset
    dut.ui_in[2].value = 0  # Reset (block_enable low)
    dut.ui_in[3].value = 0  # Set pdm_in to 0
    await ClockCycles(dut.clk, 5)  # Wait for a few fast clock cycles
    dut.ui_in[2].value = 1  # Release reset (block_enable high)

    # Monitor encPcm for 20 slow clock cycles
    initial_value = int(dut.uo_out[4:1].value)  # Capture the initial encPcm value
    change_detected = False
    for _ in range(20):
        await RisingEdge(dut.ui_in[1])  # Wait for slow clock edges
        current_value = int(dut.uo_out[4:1].value)
        if current_value != initial_value:
            change_detected = True
            break

    assert change_detected, "No change detected in encPcm when it was expected."
