![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# IMA ADPCM Audio Compression Accelerator

- [Read the documentation for project](docs/info.md)

## What is this project

This HDL block accepts a pulse density modulated (PDM) microphone signal and produces an encoded output at a lower sampling frequency while maintaining audio intelligibility.

Expected Inputs: clk (clk) slow_clk (ui_in[1]) for the ADPCM block at 1/8 frequency of clk Pulse Density Modulated input pdm_in (ui_in[2]) at clocked with clk block_enable (ui_in[3]) (active high): single bit enable for the entire block

Outputs: encPcm (uo_out[4:1]): the final 4 bit ADPCM encoded output outValid (uo_out[0]): Output Valid flag for the ADPCM block, goes high for one cycle of slow_clk each time a new valid adpcm value is output


## Verilog Files

1. CICDecimatorVerilogBlock.v
   The CIC decimation filter to parallelize serial pdm microphone data and decimate by a factor of 64
   
2. CIC_ADPCM_Wrapper.v
  The wrapper block with control logic for block_enable and connections between the CIC and encoder
   
   
3. ima_adpcm_enc.v
  The IMA ADPCM encoder which encodes the 16 bit output of the CIC filter to 4 bit adpcm samples
   
   
4. tt_um_factory_test.v
   A Top level wrapper to match the tinytapeout signal names


## Resources

- [CIC Filter Explanation](https://wirelesspi.com/cascaded-integrator-comb-cic-filters-a-staircase-of-dsp/)
- [CIC Filter Continued](https://www.dsprelated.com/showarticle/1337.php)
- [IMA ADPCM Standard] (https://ww1.microchip.com/downloads/en/AppNotes/00643b.pdf)


