# Function 6

Round a zone position and vertical width.

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>6</td><td><em>function index</em></td><td>6</td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td><td>cvt_zone cvt_zone</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td><td>cvt_zone cvt_zone cvt_zone</td></tr>
<tr><td>    RCVT[ ]</td><td>ReadCVT</td><td>cvt_zone cvt_zone zone_position</td></tr>
<tr><td>    ROUND[01]</td><td>Round</td><td>cvt_zone cvt_zone round(zone_position)</td></tr>
<tr><td>    WCVTP[ ]</td><td>WriteCVTInPixels</td><td>cvt_zone</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>next CVT index</em></td><td>cvt_zone 1</td></tr>
<tr><td>    ADD[ ]</td><td>Add</td><td>cvt_zone+1</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td><td>cvt_zone+1 cvt_zone+1</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td><td>cvt_zone+1 cvt_zone+1 cvt_zone+1</td></tr>
<tr><td>    RCVT[ ]</td><td>ReadCVT</td><td>cvt_zone+1 cvt_zone+1 zone_width</td></tr>
<tr><td>    RDTG[ ]</td><td>RoundDownToGrid</td></tr>
<tr><td>    ROUND[01]</td><td>Round</td><td>cvt_zone+1 cvt_zone+1 round(zone_width)</td></tr>
<tr><td>    RTG[ ]</td><td>RoundToGrid</td></tr>
<tr><td>    WCVTP[ ]</td><td>WriteCVTInPixels</td><td>cvt_zone+1</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>next CVT index</em></td><td>cvt_zone+1 1</td></tr>
<tr><td>    ADD[ ]</td><td>Add</td><td>cvt_zone+2</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
