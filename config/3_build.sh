import virtualenv, textwrap, os
file_contents = None
jonti_home = os.environ['JONTI_HOME']
with open(jonti_home+'/config/venv_init.py', 'r') as f:
    print 'loading venv_init.py into 4_build_venv.py'
    file_contents = f.read()
output = virtualenv.create_bootstrap_script(textwrap.dedent(file_contents))
print 'generating source for 4_build_venv.py'
f = open(jonti_home+'/config/4_build_venv.py', 'w').write(output)
