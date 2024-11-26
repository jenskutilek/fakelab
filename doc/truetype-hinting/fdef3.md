# Function 3

Double Link without stem.

Arguments on stack: _pt1, pt2_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>3</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt1 pt2 pt2</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>pt1 pt2 coord2</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>pt1 pt2 coord2 3</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td>pt1 pt2 coord2 pt1</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>pt1 pt2 coord2 coord1</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td>                 <td>pt1 pt2 coord2>coord1</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>pt1 pt2</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>pt2 pt1</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>pt1|pt2 pt2|pt1</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt1|pt2 pt2|pt1 pt2|pt1</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>pt2|pt1 pt2|pt1 pt1|pt2</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt2|pt1 pt2|pt1 pt1|pt2 pt1|pt2</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>pt2|pt1 pt1|pt2 pt1|pt2 pt2|pt1</td></tr>
<tr><td>    MD[0]</td><td>MeasureDistance</td>             <td>pt2|pt1 pt1|pt2 dist(pt1|pt2 pt2|pt1)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td>pt2|pt1 pt1|pt2 abs(dist(pt1|pt2 pt2|pt1))</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 pt2|pt1</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 coord2|coord1</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 coord2|coord1 coord2|coord1</td></tr>
<tr><td>    ROUND[00]</td><td>Round</td>                   <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 coord2|coord1 round(coord2|coord1)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 coord2|coord1-round(coord2|coord1)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1))</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td>                                <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1)) 4</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1)) pt1|pt2</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1)) coord1|coord2</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1)) coord1|coord2 coord1|coord2</td></tr>
<tr><td>    ROUND[00]</td><td>Round</td>                   <td>pt1|pt2 abs(dist(pt1|pt2 pt2|pt1)) pt2|pt1 abs(coord2|coord1-round(coord2|coord1)) coord1|coord2 round(coord1|coord2)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td>TODO</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td></tr>
<tr><td>    IF[ ]</td><td>If</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td></tr>
<tr><td>        NEG[ ]</td><td>Negate</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    MDAP[1]</td><td>MoveDirectAbsPt</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    0</td><td></td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td></tr>
<tr><td>    IF[ ]</td><td>If</td></tr>
<tr><td>        ROUND[01]</td><td>Round</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        0</td><td></td></tr>
<tr><td>        EQ[ ]</td><td>Equal</td></tr>
<tr><td>        IF[ ]</td><td>If</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td>   <td></td></tr>
<tr><td>            64</td><td></td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td></tr>
<tr><td>        ROUND[01]</td><td>Round</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        0</td><td></td></tr>
<tr><td>        EQ[ ]</td><td>Equal</td></tr>
<tr><td>        IF[ ]</td><td>If</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            64</td><td></td></tr>
<tr><td>            NEG[ ]</td><td>Negate</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    MSIRP[0]</td><td>MoveStackIndirRelPt</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>