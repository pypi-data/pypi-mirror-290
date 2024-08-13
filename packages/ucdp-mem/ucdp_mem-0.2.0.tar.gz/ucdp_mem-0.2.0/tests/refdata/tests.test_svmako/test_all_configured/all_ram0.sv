// =============================================================================
//
// THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
//
//  MIT License
//
//  Copyright (c) 2024 nbiotcloud
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
// =============================================================================
//
// Module:     tests.all_ram0
// Data Model: tests.test_svmako.RamMod
//
//
// Org:         100x8 (100 bytes)
// Wordmasks:   0xFF
// Accesslanes: -
// Powerlanes:  -
// Constraints: MemTechConstraints(max_depth=2048, max_width=32, depth_inc=32, width_inc=4)
// Segmentation:
//     y/x      0
//      0  100(128)x8/1
//     Total: 100x8/1(100 bytes)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram0 ( // tests.test_svmako.RamMod
  // main_i
  input  wire                   main_clk_i,
  input  wire                   main_rst_an_i,   // Async Reset (Low-Active)
  // io_i
  // io_main_i
  input  wire                   io_main_ena_i,
  input  wire  [$clog2(99)-1:0] io_main_addr_i,
  input  wire                   io_main_wena_i,
  input  wire  [7:0]            io_main_wdata_i,
  output logic [7:0]            io_main_rdata_o,
  // pwr_i
  // pwr_main_i
  input  wire                   pwr_main_pwr_i
  // tech_i
);



  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  // mem_s
  // mem_y0_x0_s
  logic                   mem_y0_x0_ena_s;
  logic [$clog2(127)-1:0] mem_y0_x0_addr_s;
  logic                   mem_y0_x0_wena_s;
  logic [7:0]             mem_y0_x0_wdata_s;
  logic [7:0]             mem_y0_x0_rdata_s;


  // ------------------------------------------------------
  //  tests.all_ram0_mux: u_mux
  // ------------------------------------------------------
  all_ram0_mux u_mux (
    // in_i
    // in_main_i
    .in_main_ena_i    (io_main_ena_i    ),
    .in_main_addr_i   (io_main_addr_i   ),
    .in_main_wena_i   (io_main_wena_i   ),
    .in_main_wdata_i  (io_main_wdata_i  ),
    .in_main_rdata_o  (io_main_rdata_o  ),
    // out_o
    // out_y0_x0_o
    .out_y0_x0_ena_o  (mem_y0_x0_ena_s  ),
    .out_y0_x0_addr_o (mem_y0_x0_addr_s ),
    .out_y0_x0_wena_o (mem_y0_x0_wena_s ),
    .out_y0_x0_wdata_o(mem_y0_x0_wdata_s),
    .out_y0_x0_rdata_i(mem_y0_x0_rdata_s)
  );

endmodule // all_ram0

`default_nettype wire
`end_keywords
