*** Settings ***
Variables   testdata.py

*** Test Cases ***
#{% for tc in testcases %}
${T_tc.name}
    [Tags]    {% for tag in tc.tags %} {{tag}} {% endfor %}
    Log Many    Global variable      ${global_var}
    # ${T_tc.data.var} will be replaced by its value in each test case
    Log Many    Template variable    ${T_tc.data.var}
    # ${testcases}[0][data][var] 
    # will be replaced by 
    # ${testcases}[i][data][var], i=0,...,len(testcases)-1
    Log Many    Scalar variable      ${testcases}[0][data][var]
    Log Many    List variable        @{testcases}[0][data][list]
    Log Many    Dict variable        &{testcases}[0][data][dict]
#{% endfor %}
