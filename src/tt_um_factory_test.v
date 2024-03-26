/*
 * tt_um_factory_test.v
 *
 * Test user module
 *
 * Author: Sylvain Munaut <tnt@246tNt.com>
 */

`default_nettype none

module tt_um_factory_test (
	input  wire [3:0] ui_in,	// Dedicated inputs
	output wire [4:0] uo_out	// Dedicated outputs
	//input  wire [7:0] uio_in,	// IOs: Input path
	//output wire [7:0] uio_out,	// IOs: Output path
	//output wire [7:0] uio_oe,	// IOs: Enable path (active high: 0=input, 1=output)
	//input  wire       ena,
	//input  wire       clk,
	//input  wire       rst_n
);


	CIC_ADPCM_Wrapper compressor(
		.clk(ui_in[0]),
		.slow_clk(ui_in[1]),
		.block_enable(ui_in[2]),
		.pdm_in(ui_in[3]),
		.outValid(uo_out[0]),
		.encPcm(uo_out[4:1])
	);
	



endmodule // tt_um_factory_test
