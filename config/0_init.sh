DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export JONTI_HOME=${DIR%/bin}
echo "JONTI_HOME set to: $JONTI_HOME"
export PATH=$JONTI_HOME/bin:$PATH
echo "PATH set to: $PATH"

