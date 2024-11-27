# Function 3

Double Link without stem.

Sorts the two points that make up the Double Link by their coordinate, measures which point is closer to the grid and rounds it to the grid. Rounds the other point and makes it distance to the first point at least 64/64 pixels.

Arguments on stack: _point1, point2_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>3</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>point1 point2 point2</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>point1 point2 coord2</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>point1 point2 coord2 3</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td>point1 point2 coord2 point1</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>point1 point2 coord2 coord1</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td>                 <td>point1 point2 coord2>coord1</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>point1 point2</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>point2 point1</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>ptmax ptmin</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmax ptmin ptmin</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>ptmin ptmin ptmax</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmin ptmin ptmax ptmax</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>ptmin ptmax ptmax ptmin</td></tr>
<tr><td>    MD[0]</td><td>MeasureDistance</td>             <td>ptmin ptmax dist(ptmax,ptmin)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td>ptmin ptmax abs(dist(ptmax,ptmin))</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>ptmax abs(dist(ptmax,ptmin)) ptmin</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmax abs(dist(ptmax,ptmin)) ptmin ptmin</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>ptmax abs(dist(ptmax,ptmin)) ptmin coordmin</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmax abs(dist(ptmax,ptmin)) ptmin coordmin coordmin</td></tr>
<tr><td>    ROUND[00]</td><td>Round</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin coordmin round(coordmin)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin coordmin-round(coordmin)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin))</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    4</td><td></td>                                <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) 4</td></tr>
<tr><td>    CINDEX[ ]</td><td>CopyXToTopStack</td>         <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) ptmax</td></tr>
<tr><td>    GC[0]</td><td>GetCoordOnPVector</td>           <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) coordmax</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) coordmax coordmax</td></tr>
<tr><td>    ROUND[00]</td><td>Round</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) coordmax round(coordmax)</td></tr>
<tr><td>    SUB[ ]</td><td>Subtract</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) coordmax-round(coordmax)</td></tr>
<tr><td>    ABS[ ]</td><td>Absolute</td>                   <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin)) abs(coordmax-round(coordmax))</td></tr>
<tr><td>    GT[ ]</td><td>GreaterThan</td>                 <td>ptmax abs(dist(ptmax,ptmin)) ptmin abs(coordmin-round(coordmin))>abs(coordmax-round(coordmax))</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>ptmax abs(dist(ptmax,ptmin)) ptmin</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>ptmax ptmin abs(dist(ptmax,ptmin))</td></tr>
<tr><td>        NEG[ ]</td><td>Negate</td>                 <td>ptmax ptmin neg(abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>ptmin neg(abs(dist(ptmax,ptmin))) ptmax</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)) ptmax|ptmin</td></tr>
<tr><td>    MDAP[1]</td><td>MoveDirectAbsPt</td>           <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)) neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    0</td><td></td>                                <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)) neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)) 0</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)) neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))>=0</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))</td></tr>
<tr><td>        ROUND[01]</td><td>Round</td>               <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td>      <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        0</td><td></td>                            <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) 0</td></tr>
<tr><td>        EQ[ ]</td><td>Equal</td>                   <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))==0</td></tr>
<tr><td>        IF[ ]</td><td>If</td>                      <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>ptmin|ptmax</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            64</td><td></td>                       <td>ptmin|ptmax 64</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td>                  <td>ptmin|ptmax 64|round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>ptmin|ptmax neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))</td></tr>
<tr><td>        ROUND[01]</td><td>Round</td>               <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td>      <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        0</td><td></td>                            <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) 0</td></tr>
<tr><td>        EQ[ ]</td><td>Equal</td>                   <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))) round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))==0</td></tr>
<tr><td>        IF[ ]</td><td>If</td>                      <td>ptmin|ptmax round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>ptmin|ptmax</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            64</td><td></td>                       <td>ptmin|ptmax 64</td></tr>
<tr><td>            NEG[ ]</td><td>Negate</td>             <td>ptmin|ptmax -64</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td>                  <td>ptmin|ptmax -64|round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>ptmin|ptmax 64|round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))|neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin))|-64|round(neg(abs(dist(ptmax,ptmin)))|abs(dist(ptmax,ptmin)))</td></tr>
<tr><td>    MSIRP[0]</td><td>MoveStackIndirRelPt</td>      <td>—</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
