import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_CIC_ADPCM_Wrapper(dut):
    # Create a 10us period clock on port 'clk' for fast clock
    fast_clock = Clock(dut.ui_in[0], 10, units="us")
    cocotb.start_soon(fast_clock.start())

    # Create an 80us period clock on port 'clk' for slow clock
    slow_clock = Clock(dut.ui_in[1], 80, units="us")
    cocotb.start_soon(slow_clock.start())

    # Initial reset of your module
    dut.ui_in[2].value = 0  # Set block_enable to 0 (reset)
    dut.ui_in[3].value = 0  # Set pdm_in to 0 and maintain this throughout the test
    await ClockCycles(dut.ui_in[0], 5)  # Wait for a few fast clock cycles
    dut.ui_in[2].value = 1  # Release reset (block_enable to 1)

    # Ensure pdm_in stays at 0
    dut.ui_in[3].value = 0

    # Initial reading of encPcm output
    initial_value = int(dut.uo_out[4:1].value)  # Capture the initial encPcm value

    # Monitor encPcm for 20 slow clock cycles
    for _ in range(20):
        await RisingEdge(dut.ui_in[1])  # Wait for slow clock edges
        current_value = int(dut.uo_out[4:1].value)
        if current_value != initial_value:
            print("expected change detected in encPcm.")
            assert True, "Output changed."

    # If no change is observed after 20 slow clock cycles, pass the test
    print("No change in encPcm after 20 slow clock cycles as expected.")
    assert False, "Output remains the same."

