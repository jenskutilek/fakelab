# Function 0

Deactivates grid-fitting if the current pixels per em are less than the _lowestRecPPEM_ value set in FLS5’s font info under _TrueType-specific settings > Font flags: [head] table._ It also sets the [dropout_control](https://learn.microsoft.com/en-us/typography/opentype/spec/tt_instructions#scan-conversion-control) to “Always do dropout control” using the `SCANCTRL` instruction, and sets the control_value_cut_in value, delta_base, and delta_shift in the Graphics State.

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>0</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td>                                     <td>ppem</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    <strong>9</strong></td><td><em>lowest grid-fitted ppm</em></td>             <td>ppem 9</td></tr>
<tr><td>    LT[ ]</td><td>LessThan</td>                                                 <td>ppem&lt;9</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                                                       <td>—</td></tr>
<tr><td>        PUSHB[ ]</td><td>2 values pushed</td></tr>
<tr><td>        1 1</td>                                                                <td>1 1</td></tr>
<tr><td>        INSTCTRL[ ]</td><td>SetInstrExecControl</td>                            <td>—</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    511</td><td></td>                                                           <td>511</td></tr>
<tr><td>    SCANCTRL[ ]</td><td>ScanConversionControl</td>                              <td>—</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    <strong>68</strong></td><td><em>stem snap precision</em></td>               <td>68</td></tr>
<tr><td>    SCVTCI[ ]</td><td>SetCVTCutIn</td>                                          <td>—</td></tr>
<tr><td>    PUSHW[ ]</td><td>2 values pushed</td></tr>
<tr><td>    <strong>9</strong></td><td><em>delta base (lowest grid-fitted ppm)</em></td><td>9</td></tr>
<tr><td>    3</td><td><em>delta shift</em></td>                                         <td>9 3</td></tr>
<tr><td>    SDS[ ]</td><td>SetDeltaShiftInGState</td>                                   <td>9</td></tr>
<tr><td>    SDB[ ]</td><td>SetDeltaBaseInGState</td>                                    <td>—</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>

The value for _lowest grid-fitted ppm_ should be synchronized with the ppm in the `gasp` table at which grid-fitting is activated, and with the lowestRecPPEM value in the `head` table. It will also be used as the delta_base value further down in the function.

The value for _stem snap precision_ is taken from FLS5’s General TrueType options, but converted to 64ths of pixels. So the default value of 17/16 pixels is given here as 17 ⋅ 4 = 68.

> 17/16 is also the default value, and could be omitted.
