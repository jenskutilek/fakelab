# Function 4

Double Link with stem.

Sorts the two points that make up the Double Link by their coordinate, measures which point is closer to the grid and rounds it to the grid. Moves the other point so that its distance from the first point equals the CVT stem.

Arguments on stack: _point1, cvt_stem, point2_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>4</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td colspan="2">point1 cvt_stem point2 point2</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td colspan="2">point1 cvt_stem point2 coord2</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td>                                <td colspan="2">point1 cvt_stem point2 coord2 4</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td colspan="2">point1 cvt_stem point2 coord2</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td colspan="2">point1 cvt_stem point2 coord2 point1</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td>                 <td colspan="2">point1 cvt_stem point2 coord2>point1</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td colspan="2">point1 cvt_stem point2</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td colspan="2">point1 point2 cvt_stem</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td colspan="2">point2 cvt_stem point1</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td colspan="2">ptmax cvt_stem ptmin</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td colspan="2">ptmax cvt_stem ptmin ptmin</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td colspan="2">ptmax cvt_stem ptmin coordmin</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td colspan="2">ptmax cvt_stem ptmin coordmin coordmin</td></tr>
<tr><td>    ROUND[10]</td><td>Round</td>                   <td colspan="2">ptmax cvt_stem ptmin coordmin round(coordmin)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td colspan="2">ptmax cvt_stem ptmin coordmin-round(coordmin)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin))</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td>                                <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) 4</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) ptmax</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) coordmax</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) coordmax coordmax</td></tr>
<tr><td>    ROUND[10]</td><td>Round</td>                   <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) coordmax round(coordmax)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) coordmax-round(coordmax)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin)) abs(coordmax-round(coordmax))</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td>                 <td colspan="2">ptmax cvt_stem ptmin abs(coordmin-round(coordmin))>abs(coordmax-round(coordmax))</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>ptmax cvt_stem ptmin</td>    <td>ptmax cvt_stem ptmin</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>ptmax ptmin cvt_stem</td>    <td>|</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>ptmin cvt_stem ptmax</td>    <td>|</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>ptmin cvt_stem ptmax</td>    <td>ptmax cvt_stem ptmin</td></tr>
<tr><td>    MDAP[1]</td><td>MoveDirectAbsPt</td>           <td>ptmin cvt_stem</td>          <td>ptmax cvt_stem</td></tr>
<tr><td>    MIRP[11101]</td><td>MoveIndirectRelPt</td>     <td colspan="2">—</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
</table>
