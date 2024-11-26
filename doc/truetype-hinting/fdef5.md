# Function 5

This function is not used by FLS5.

Arguments on stack: _cvt, ppem1, ppem2_

<table>
<tr><th>Assembly</th><th></th>                             <th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>5</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td>        <td>cvt ppem1 ppem2 ppem</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt ppem1 ppem2 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt ppem1 ppem2 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt ppem1 ppem ppem ppem2</td></tr>
<tr><td>    LT[ ]</td><td>LessThan</td>                    <td>cvt ppem1 ppem ppem&lt;ppem2</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt ppem1 ppem</td></tr>
<tr><td>        LTEQ[ ]</td><td>LessThenOrEqual</td>       <td>cvt ppem1&lt;=ppem</td></tr>
<tr><td>        IF[ ]</td><td>If</td>                      <td>cvt</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            128</td><td></td>                      <td>cvt 128</td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td> <td>—</td></tr>
<tr><td>        ELSE[ ]</td><td>Else</td>                  <td>cvt</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            64</td><td></td>                       <td>cvt 64</td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td> <td>—</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td>                  <td>—</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>cvt ppem1 ppem</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt ppem1</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt</td></tr>
<tr><td>        DUP[ ]</td><td>DuplicateTopStack</td>      <td>cvt cvt</td></tr>
<tr><td>        RCVT[ ]</td><td>ReadCVT</td>               <td>cvt z</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        192</td><td></td>                          <td>cvt z 192</td></tr>
<tr><td>        LT[ ]</td><td>LessThan</td>                <td>cvt z&lt;192</td></tr>
<tr><td>        IF[ ]</td><td>If</td>                      <td>cvt</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            192<td></td>                           <td>cvt 192</td></tr>
<tr><td>            WCVTP[ ]</td><td>WriteCVTInPixels</td> <td>—</td></tr>
<tr><td>        ELSE[ ]</td><td>Else</td>                  <td>cvt</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>—</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
