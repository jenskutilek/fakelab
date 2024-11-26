# Function 2

Round a number of stems.

Arguments on stack: _cvt_first_stem, stems_count_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>2</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>function index</em></td>                               <td>cvt_first_stem stems_count 1</td></tr>
<tr><td>    LOOPCALL[ ]</td><td><a href="fdef1.md">LoopAndCallFunction 1</a></td><td>cvt_first_stem+stems_count+1</td></tr>
<tr><td>    POP[ ]</td><td>PopTopStack</td>                                      <td>—</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
