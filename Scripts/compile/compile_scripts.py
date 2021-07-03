import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

release_dir = os.path.join('..', '..', 'Release')

Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNHaterKeepHatin'), names_of_modules_include=('cnhaterskeephatin',), output_ts4script_name='cn_haters_keep_hatin')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNRealisticSalaries'), names_of_modules_include=('cnrealisticsalaries',), output_ts4script_name='cn_realistic_salaries')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNNoRelationshipDecay'), names_of_modules_include=('cnnorelationshipdecay',), output_ts4script_name='cn_no_relationship_decay')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNTEI'), names_of_modules_include=('cntei',), output_ts4script_name='cn_tei')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNNoQuickMeals'), names_of_modules_include=('cnnoquickmeals',), output_ts4script_name='cn_no_quick_meals')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNOfferBlood'), names_of_modules_include=('cnofferblood',), output_ts4script_name='cn_offer_blood')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'CNChangeMotives'), names_of_modules_include=('cnchangemotives',), output_ts4script_name='cn_change_motives')
Unpyc3PythonCompiler.compile_mod(folder_path_to_output_ts4script_to=os.path.join(release_dir, 'S4AutosaveMod'), names_of_modules_include=('s4autosavemod',), output_ts4script_name='s4autosavemod')
