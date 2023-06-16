SCRIPT_PATH="${BASH_SOURCE:-$0}"
ABS_SCRIPT_PATH="$(realpath "${SCRIPT_PATH}")"
ABS_DIRECTORY="$(dirname "${ABS_SCRIPT_PATH}")"
# echo "Value of ABS_SCRIPT_PATH: ${ABS_SCRIPT_PATH}"
# echo "Value of ABS_DIRECTORY: ${ABS_DIRECTORY}"

. "${ABS_DIRECTORY}"/venv/bin/activate
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi
uvicorn app.main:app --reload