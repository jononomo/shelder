deactivate > /dev/null 2>&1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/0_init.sh
source $JONTI_HOME/bin/5_activate.sh
python $JONTI_HOME/jonti/jonti.py

