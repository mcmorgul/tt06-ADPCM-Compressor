import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_CIC_ADPCM_Wrapper(dut):
    # Create a 10us period clock on port 'clk'
    clock = Clock(dut.ui_in[0], 10, units="us")
    cocotb.start_soon(clock.start())  # Start the fast clock

    slow_clk = Clock(dut.ui_in[1], 80, units="us")
    cocotb.start_soon(slow_clk.start())  # Start the slow clock
    
    # Reset your module
    dut.ui_in[2].value = 0  # Reset
    dut.ui_in[3].value = 0  # Set pdm_in to 0 and maintain this throughout the test
    await ClockCycles(dut.ui_in[0], 5)
    dut.ui_in[2].value = 1  # Release reset
    await ClockCycles(dut.ui_in[0], 1)

    # Start monitoring encPcm output
    initial_value = dut.u0_out[4].value.binstr

    # Run for 20 slow clock cycles
    for _ in range(20):
        await RisingEdge(dut.ui_in[1])
        current_value = dut.u0_out[4].value.binstr
        if current_value != initial_value:
            print("Change detected in encPcm after 20 slow clock cycles.")
            assert True, "Change in encPcm confirmed"
            return
    
    # If no change is detected, raise an assertion error
    assert False, "No change in encPcm after 20 slow clock cycles"
