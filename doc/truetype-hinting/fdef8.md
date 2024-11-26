# Function 8

Set a stem to the pixel width defined in the Stems TrueType options.

Arguments on stack: _cvt_stem, ppm6, ppm5, ppm4, ppm3, ppm2, ppm1_

<table>
<tr><th>Assembly</th><th></th><th>Stack</th></tr>
<tr><td>PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>8</td><td><em>function index</em></td></tr>
<tr><td>FDEF[ ]</td><td>FunctionDefinition</td></tr>
<tr><td>    MPPEM[ ]</td><td>MeasurePixelPerEm</td>        <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppm1 ppem</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppm1 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppm1 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppem ppem ppm1</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppem ppem>=ppm1</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppem</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        64</td><td></td>                           <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppem 64</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        0</td><td></td>                            <td>cvt_stem ppm6 ppm5 ppm4 ppm3 ppm2 ppem 0</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>cvt_stem ppm6 ppm5 ppm4 ppm2 ppem 64|0 ppm3</td></tr>
<tr><td>    ROLL[ ]</td><td>RollTopThreeStack</td>         <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppm3 ppem</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppm3 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppm3 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppem ppem ppm3</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppem ppem>=ppm3</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem ppm6 ppm5 ppm4 ppm2 64|0 ppem</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 ppm2 ppem 64|0</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_stem ppm6 ppm5 ppm4 ppm2 ppem</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        128</td><td></td>                          <td>cvt_stem ppm6 ppm5 ppm4 ppm2 ppem 128</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 ppm4 ppem 128 ppm2</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 ppm4 128 ppm2 ppem</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 ppm4 64|0 ppem ppm2</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 64|0 ppm2 ppem</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 128|64|0 ppm2 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem ppm6 ppm5 ppm4 128|64|0 ppm2 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem ppm6 ppm5 ppm4 128|64|0 ppem ppem ppm2</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem ppm6 ppm5 ppm4 128|64|0 ppem ppem>=ppm2</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem ppm6 ppm5 ppm4 128|64|0 ppem</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppm5 ppm4 ppem 128|64|0</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_stem ppm6 ppm5 ppm4 ppem</td></tr>
<tr><td>        PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>        192</td><td></td>                          <td>cvt_stem ppm6 ppm5 ppm4 ppem 192</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 ppem 192 ppm4</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 192 ppm4 ppem</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppm5 128|64|0 ppem ppm4</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppm5 128|64|0 ppm4 ppem</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem ppm6 ppm5 192|128|64|0 ppm4 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem ppm6 ppm5 192|128|64|0 ppm4 ppem ppem 3</td></tr></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem ppm6 ppm5 192|128|64|0 ppem ppem ppm4</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem ppm6 ppm5 192|128|64|0 ppem ppem>=ppm4</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem ppm6 ppm5 192|128|64|0 ppem</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppm5 ppem 192|128|64|0</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_stem ppm6 ppm5 ppem</td></tr>
<tr><td>        PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>        256</td><td></td>                          <td>cvt_stem ppm6 ppm5 ppem 256</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 ppem 256 ppm5</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 256 ppm5 ppem</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>cvt_stem ppm6 ppm5 192|128|64|0 ppem</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppm6 192|128|64|0 ppem ppm5</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 192|128|64|0 ppm5 ppem</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem ppm6 256|192|128|64|0 ppm5 ppem ppem</td></tr>
<tr><td>    PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem ppm6 256|192|128|64|0 ppm5 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem ppm6 256|192|128|64|0 ppem ppem ppm5</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem ppm6 256|192|128|64|0 ppem ppem>=ppm5</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem ppm6 256|192|128|64|0 ppem</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem ppm6 ppem 256|192|128|64|0</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_stem ppm6 ppem</td></tr>
<tr><td>        PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>        320</td><td></td>                          <td>cvt_stem ppm6 ppem 320</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem ppem 320 ppm6</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem 320 ppm6 ppem</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>cvt_stem ppm6 256|192|128|64|0 ppem</td></tr>
<tr><td>        ROLL[ ]</td><td>RollTopThreeStack</td>     <td>cvt_stem 256|192|128|64|0 ppem ppm6</td></tr>
<tr><td>        SWAP[ ]</td><td>SwapTopStack</td>          <td>cvt_stem 256|192|128|64|0 ppm6 ppem</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    DUP[ ]</td><td>DuplicateTopStack</td>          <td>cvt_stem 320|256|192|128|64|0 ppm6 ppem ppem</td></tr>
<tr><td>    PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>    3</td><td></td>                                <td>cvt_stem 320|256|192|128|64|0 ppm6 ppem ppem 3</td></tr>
<tr><td>    MINDEX[ ]</td><td>MoveXToTopStack</td>         <td>cvt_stem 320|256|192|128|64|0 ppem ppem ppm6</td></tr>
<tr><td>    GTEQ[ ]</td><td>GreaterThanOrEqual</td>        <td>cvt_stem 320|256|192|128|64|0 ppem ppem>=ppm6</td></tr>
<tr><td>    IF[ ]</td><td>If</td>                          <td>cvt_stem 320|256|192|128|64|0 ppem</td></tr>
<tr><td>        PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>        3</td><td></td>                            <td>cvt_stem 320|256|192|128|64|0 ppem 3</td></tr>
<tr><td>        CINDEX[ ]</td><td>CopyXToTopStack</td>     <td>cvt_stem 320|256|192|128|64|0 ppem cvt_stem</td></tr>
<tr><td>        RCVT[ ]</td><td>ReadCVT</td>               <td>cvt_stem 320|256|192|128|64|0 ppem stem</td></tr>
<tr><td>        PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>        384</td><td></td>                          <td>cvt_stem 320|256|192|128|64|0 ppem stem 384</td></tr>
<tr><td>        LT[ ]</td><td>LessThan</td>                <td>cvt_stem 320|256|192|128|64|0 ppem stem&lt;384</td></tr>
<tr><td>        IF[ ]</td><td>If</td>                      <td>cvt_stem 320|256|192|128|64|0 ppem</td></tr>
<tr><td>            SWAP[ ]</td><td>SwapTopStack</td>      <td>cvt_stem ppem 320|256|192|128|64|0</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>cvt_stem ppem</td></tr>
<tr><td>            PUSHW[ ]</td><td>1 value pushed</td></tr>
<tr><td>            384</td><td></td>                      <td>cvt_stem ppem 384</td></tr>
<tr><td>            SWAP[ ]</td><td>SwapTopStack</td>      <td>cvt_stem 384 ppem</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>cvt_stem 384</td></tr>
<tr><td>        ELSE[ ]</td><td>Else</td>                  <td>cvt_stem 320|256|192|128|64|0 ppem</td></tr>
<tr><td>            PUSHB[ ]</td><td>1 value pushed</td></tr>
<tr><td>            3</td><td></td>                        <td>cvt_stem 320|256|192|128|64|0 ppem 3</td></tr>
<tr><td>            CINDEX[ ]</td><td>CopyXToTopStack</td> <td>cvt_stem 320|256|192|128|64|0 ppem cvt_stem</td></tr>
<tr><td>            RCVT[ ]</td><td>ReadCVT</td>           <td>cvt_stem 320|256|192|128|64|0 ppem stem</td></tr>
<tr><td>            SWAP[ ]</td><td>SwapTopStack</td>      <td>cvt_stem 320|256|192|128|64|0 stem ppem</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>cvt_stem 320|256|192|128|64|0 stem</td></tr>
<tr><td>            SWAP[ ]</td><td>SwapTopStack</td>      <td>cvt_stem stem 320|256|192|128|64|0</td></tr>
<tr><td>            POP[ ]</td><td>PopTopStack</td>        <td>cvt_stem stem</td></tr>
<tr><td>        EIF[ ]</td><td>EndIf</td></tr>
<tr><td>    ELSE[ ]</td><td>Else</td>                      <td>cvt_stem 320|256|192|128|64|0 ppem</td></tr>
<tr><td>        POP[ ]</td><td>PopTopStack</td>            <td>cvt_stem 320|256|192|128|64|0</td></tr>
<tr><td>    EIF[ ]</td><td>EndIf</td>                      <td>cvt_stem 384|320|256|192|128|64|0|stem</td></tr></tr>
<tr><td>    WCVTP[ ]</td><td>WriteCVTInPixels</td></tr>
<tr><td>ENDF[ ]</td><td>EndFunctionDefinition</td></tr>
</table>
