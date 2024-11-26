# Function 7

Round a number of zones.

Arguments on stack: _cvt_first_zone, zones_count_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>7</td><td><em>function index</em></td><td>7</td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    6</td><td><em>function index</em></td><td>cvt_first_zone zones_count 6</td></tr>
<tr><td>    LOOPCALL[ ]</td><td><a href="fdef6.md">LoopAndCallFunction 6</a></td><td>cvt_last_zone+2</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
