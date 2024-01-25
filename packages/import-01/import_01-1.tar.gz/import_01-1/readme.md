this has been created for college lab exams.

# this version - for 5th sem DL lab



<p style="color:#346EB0; font-family: Arial; font-size: 30px; font-weight: light"><em>dl_01 or dl-01 has been deleted by ddcrpf due it being circulated out to people of non authority. new module will be created.</em></p>


use - 

``` py
pip install dl_01
from dl_01 import main 
```

this will generate a list of all the codes available. copy the exact name of the corresponding code that you want to use.

```py
from dl_01 import name_you_copied
```

this will print the code with target output in  output of your screen




### for next attempt  or to make changes - 
1. first delete folders - 1. dist  2. src/dl_01.engg-info
2. update - in steup.cfg update version no.
then run cmd - 
1. activate venv - source venv/bin/activate
2. python3 -m build
3. twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDY4N2U5OWM3LTg1ODgtNGZhYi05MjY4LTVjNmE2ZDhmMWJjYQACKlszLCIyNDQ3YWE1ZS05YjFkLTRlZjctOTFlZS03OGExZDk4Mjk2ODgiXQAABiBHdxCGRM8vPTy4p57PzclmhYpBUpDKEc-PCo9oUFyM_g dist/*

or 

2. twine upload dist/*   ## some times this cmd not work. so use other option.


### if trying to use this code new module - 
1. follow above steps plus
2. change dl_01 name in src directory
3. update name in steup.cfg
4. run cmds' listed above
