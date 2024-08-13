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
// Module:     tests.all_ram2
// Data Model: tests.test_svmako.RamMod
//
//
// Org:         4096x64 (32 KB)
// Wordmasks:   0xFFFFFFFF, 0xFFFFFFFF
// Accesslanes: one='8 KB', two='24 KB'
// Powerlanes:  -
// Constraints: -
// Segmentation:
//     y/x         0
//      0  1024x64/1,acc=one
//      1  1024x64/1,acc=two
//      2  2048x64/1,acc=two
//     Total: 4096x64/1(32 KB)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram2 ( // tests.test_svmako.RamMod
  // main_i
  input  wire                     main_clk_i,
  input  wire                     main_rst_an_i,  // Async Reset (Low-Active)
  // io_i
  // io_one_i
  input  wire                     io_one_ena_i,
  input  wire  [$clog2(1023)-1:0] io_one_addr_i,
  input  wire                     io_one_wena_i,
  input  wire  [63:0]             io_one_wdata_i,
  output logic [63:0]             io_one_rdata_o,
  // io_two_i
  input  wire                     io_two_ena_i,
  input  wire  [$clog2(3071)-1:0] io_two_addr_i,
  input  wire                     io_two_wena_i,
  input  wire  [63:0]             io_two_wdata_i,
  output logic [63:0]             io_two_rdata_o,
  // pwr_i
  // pwr_main_i
  input  wire                     pwr_main_pwr_i
  // tech_i
);



  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  // mem_s
  // mem_y0_x0_s
  logic                    mem_y0_x0_ena_s;
  logic [$clog2(1023)-1:0] mem_y0_x0_addr_s;
  logic                    mem_y0_x0_wena_s;
  logic [63:0]             mem_y0_x0_wdata_s;
  logic [63:0]             mem_y0_x0_rdata_s;
  // mem_y1_x0_s
  logic                    mem_y1_x0_ena_s;
  logic [$clog2(1023)-1:0] mem_y1_x0_addr_s;
  logic                    mem_y1_x0_wena_s;
  logic [63:0]             mem_y1_x0_wdata_s;
  logic [63:0]             mem_y1_x0_rdata_s;
  // mem_y2_x0_s
  logic                    mem_y2_x0_ena_s;
  logic [$clog2(2047)-1:0] mem_y2_x0_addr_s;
  logic                    mem_y2_x0_wena_s;
  logic [63:0]             mem_y2_x0_wdata_s;
  logic [63:0]             mem_y2_x0_rdata_s;


  // ------------------------------------------------------
  //  tests.all_ram2_mux: u_mux
  // ------------------------------------------------------
  all_ram2_mux u_mux (
    // in_i
    // in_one_i
    .in_one_ena_i     (io_one_ena_i     ),
    .in_one_addr_i    (io_one_addr_i    ),
    .in_one_wena_i    (io_one_wena_i    ),
    .in_one_wdata_i   (io_one_wdata_i   ),
    .in_one_rdata_o   (io_one_rdata_o   ),
    // in_two_i
    .in_two_ena_i     (io_two_ena_i     ),
    .in_two_addr_i    (io_two_addr_i    ),
    .in_two_wena_i    (io_two_wena_i    ),
    .in_two_wdata_i   (io_two_wdata_i   ),
    .in_two_rdata_o   (io_two_rdata_o   ),
    // out_o
    // out_y0_x0_o
    .out_y0_x0_ena_o  (mem_y0_x0_ena_s  ),
    .out_y0_x0_addr_o (mem_y0_x0_addr_s ),
    .out_y0_x0_wena_o (mem_y0_x0_wena_s ),
    .out_y0_x0_wdata_o(mem_y0_x0_wdata_s),
    .out_y0_x0_rdata_i(mem_y0_x0_rdata_s),
    // out_y1_x0_o
    .out_y1_x0_ena_o  (mem_y1_x0_ena_s  ),
    .out_y1_x0_addr_o (mem_y1_x0_addr_s ),
    .out_y1_x0_wena_o (mem_y1_x0_wena_s ),
    .out_y1_x0_wdata_o(mem_y1_x0_wdata_s),
    .out_y1_x0_rdata_i(mem_y1_x0_rdata_s),
    // out_y2_x0_o
    .out_y2_x0_ena_o  (mem_y2_x0_ena_s  ),
    .out_y2_x0_addr_o (mem_y2_x0_addr_s ),
    .out_y2_x0_wena_o (mem_y2_x0_wena_s ),
    .out_y2_x0_wdata_o(mem_y2_x0_wdata_s),
    .out_y2_x0_rdata_i(mem_y2_x0_rdata_s)
  );

endmodule // all_ram2

`default_nettype wire
`end_keywords
