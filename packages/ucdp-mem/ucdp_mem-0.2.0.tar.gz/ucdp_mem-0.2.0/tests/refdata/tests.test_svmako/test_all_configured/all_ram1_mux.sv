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
// Module:     tests.all_ram1_mux
// Data Model: tests.test_svmako.SegMuxMod
//
//
// y/x     1         0
//  0  1024x32/1 1024x32/1
// Total: 1024x64/1(8 KB)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram1_mux ( // tests.test_svmako.SegMuxMod
  // in_i
  // in_main_i
  input  wire                     in_main_ena_i,
  input  wire  [$clog2(1023)-1:0] in_main_addr_i,
  input  wire                     in_main_wena_i,
  input  wire  [63:0]             in_main_wdata_i,
  output logic [63:0]             in_main_rdata_o,
  // out_o
  // out_y0_x0_o
  output logic                    out_y0_x0_ena_o,
  output logic [$clog2(1023)-1:0] out_y0_x0_addr_o,
  output logic                    out_y0_x0_wena_o,
  output logic [31:0]             out_y0_x0_wdata_o,
  input  wire  [31:0]             out_y0_x0_rdata_i,
  // out_y0_x1_o
  output logic                    out_y0_x1_ena_o,
  output logic [$clog2(1023)-1:0] out_y0_x1_addr_o,
  output logic                    out_y0_x1_wena_o,
  output logic [31:0]             out_y0_x1_wdata_o,
  input  wire  [31:0]             out_y0_x1_rdata_i
);

// TODO

endmodule // all_ram1_mux

`default_nettype wire
`end_keywords
