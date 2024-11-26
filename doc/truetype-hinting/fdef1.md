# Function 1

Round a stem

<table>
<tr><th>Assembly</th><th></th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>1</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    RCVT[ ]</td><td>ReadCVT</td></tr>
<tr><td>    ROUND[01]</td><td>Round</td></tr>
<tr><td>    WCVTP[ ]</td><td>WriteCVTInPixels</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>next CVT index</em></td></tr>
<tr><td>    ADD[ ]</td><td>Add</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
