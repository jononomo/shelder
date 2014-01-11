deactivate > /dev/null 2>&1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/0_init.sh
python $JONTI_HOME/bin/3_build.py
python $JONTI_HOME/bin/4_build_venv.py $JONTI_HOME/bin/JONTI
rm $JONTI_HOME/bin/4_build_venv.py
source $JONTI_HOME/bin/JONTI/bin/activate
pip install -r $JONTI_HOME/bin/requirements.txt

