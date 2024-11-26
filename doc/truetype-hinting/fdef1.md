# Function 1

Round a stem.

Arguments on stack: _cvt_stem_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>1</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem cvt_stem</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem cvt_stem cvt_stem</td></tr>
<tr><td>    RCVT[ ]</td><td>ReadCVT</td>                   <td>cvt_stem cvt_stem stem</td></tr>
<tr><td>    ROUND[01]</td><td>Round</td>                   <td>cvt_stem cvt_stem round(stem)</td></tr>
<tr><td>    WCVTP[ ]</td><td>WriteCVTInPixels</td>         <td>cvt_stem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>next CVT index</em></td>         <td>cvt_stem 1</td></tr>
<tr><td>    ADD[ ]</td><td>Add</td>                        <td>cvt_stem+1</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>

Returns on stack: The CVT index of the last stem + 1 (next CVT stem index)
