# Function 9

This function is not used by FLS5.

Make two CVT values equal up to a specified ppm.

Arguments on stack: _cvt_child, cvt_parent, max_ppm_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>9</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td>        <td>cvt_child cvt_parent max_ppm ppm</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_child cvt_parent max_ppm>=ppm</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_child cvt_parent</td></tr>
<tr><td>        RCVT[ ]</td><td>ReadCVT</td>               <td>cvt_child parent</td></tr>
<tr><td>        WCVTP[ ]</td><td>WriteCVTInPixels</td>     <td>—</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>cvt_child cvt_parent</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_child</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>—</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
