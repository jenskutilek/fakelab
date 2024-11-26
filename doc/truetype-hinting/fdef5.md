# Function 5

<table>
<tr><th>Assembly</th><th></th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>5</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td></tr>
<tr><td>    LT[ ]</td><td>LessThan</td></tr>
<tr><td>    IF[ ]</td><td>If</td></tr>
<tr><td>        LTEQ[ ]</td><td>LessThenOrEqual</td></tr>
<tr><td>        IF[ ]</td><td>If</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            128</td><td></td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td></tr>
<tr><td>        ELSE[ ]</td><td>Else</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            64</td><td></td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td></tr>
<tr><td>        RCVT[ ]</td><td>ReadCVT</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        192</td><td></td></tr>
<tr><td>        LT[ ]</td><td>LessThan</td></tr>
<tr><td>        IF[ ]</td><td>If</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            192<td></td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td></tr>
<tr><td>        ELSE[ ]</td><td>Else</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>