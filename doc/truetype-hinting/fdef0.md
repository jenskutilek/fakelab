# Function 0

<table>
    <tr><th>Assembly</th><th></th></tr>
    <tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
    <tr><td>0</td><td><em>function index</em></td></tr>
    <tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
    <tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td></tr>
    <tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
    <tr><td>    <strong>9</strong></td><td><em>lowest grid-fitted ppm</em></td></tr>
    <tr><td>    LT[ ]</td><td>LessThan</td></tr>
    <tr><td>    IF[ ]</td><td>If</td></tr>
    <tr><td>        PUSHB[ ]</td><td>2 values pushed</td></tr>
    <tr><td>        1 1</td></tr>
    <tr><td>        INSTCTRL[ ]</td><td>SetInstrExecControl</td></tr>
    <tr><td>    EIF[ ]</td><td>EndIf</td></tr>
    <tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
    <tr><td>    511</td><td></td></tr>
    <tr><td>    SCANCTRL[ ]</td><td>ScanConversionControl</td></tr>
    <tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
    <tr><td>    <strong>68</strong></td><td><em>stem snap precision</em></td></tr>
    <tr><td>    SCVTCI[ ]</td><td>SetCVTCutIn</td></tr>
    <tr><td>    PUSHW[ ]</td><td>2 values pushed</td></tr>
    <tr><td>    <strong>9</strong></td><td><em>delta base (lowest grid-fitted ppm)</em></td></tr>
    <tr><td>    3</td><td><em>delta shift</em></td></tr>
    <tr><td>    SDS[ ]</td><td>SetDeltaShiftInGState</td></tr>
    <tr><td>    SDB[ ]</td><td>SetDeltaBaseInGState</td></tr>
    <tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>

The value for _lowest grid-fitted ppm_ should be synchronized with the ppm in the `gasp` table at which grid-fitting is activated, and with the lowestRecPPEM value in the `head` table. It will also be used as the delta_base value in the Graphics State.

The value for _stem snap precision_ is taken from FLS5’s General TrueType options, but converted to 64ths of pixels. So the default value of 17/16 pixels is given here as 17 ⋅ 4 = 68.