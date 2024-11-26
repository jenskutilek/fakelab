# Function 4

Double Link with stem

<table>
<tr><th>Assembly</th><th></th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>4</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td></tr>
<tr><td>    IF[ ]</td><td>If</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    ROUND[10]</td><td>Round</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    ROUND[10]</td><td>Round</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td></tr>
<tr><td>    IF[ ]</td><td>If</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    MDAP[1]</td><td>MoveDirectAbsPt</td></tr>
<tr><td>    MIRP[11101]</td><td>MoveIndirectRelPt</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
</table>