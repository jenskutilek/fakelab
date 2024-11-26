# Function 2

Round a number of stems

<table>
<tr><th>Assembly</th><th></th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>2</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    1</td><td><em>function index</em></td></tr>
<tr><td>    LOOPCALL[ ]</td><td><a href="fdef1.md">LoopAndCallFunction 1</a></td></tr>
<tr><td>    POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
