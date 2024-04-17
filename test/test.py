import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, Timer

@cocotb.test()
async def tt_um_factory_test(dut):
    # Create a fast clock
    fast_clock = Clock(dut.clk, 10, units="us")  # Fast clock
    cocotb.start_soon(fast_clock.start())

    # Initial reset
    dut.ena.value = 0
    dut.ui_in[2].value = 0  # Reset (block_enable low)
    dut.ui_in[3].value = 0  # Set pdm_in to 0
    await ClockCycles(dut.clk, 5)  # Wait for a few fast clock cycles
    dut.ui_in[2].value = 1  # Release reset (block_enable high)

    # Software managed "slow clock" effect
    slow_clk_period = 80  # In microseconds, adjust as needed
    initial_value = int(dut.uo_out.value.binstr[-5:-1], 2)  # Assuming slicing fixed

    # Manually toggle pdm_in to simulate slow clock effect
    change_detected = False
    for _ in range(20):  # Less number, since we wait more due to slow_clk_period
        await Timer(slow_clk_period, units='us')
        dut.ui_in[3].value = not dut.ui_in[3].value  # Toggle pdm_in
        await RisingEdge(dut.clk)
        current_value = int(dut.uo_out.value.binstr[-5:-1], 2)
        if current_value == initial_value:
            change_detected = True
            break

    assert change_detected, "Change detected in encPcm when it was not expected."
