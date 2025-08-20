# Change this information
TRAINER_NAME="matheus.c"
DB_NAME="finance"
INTERFACE_NUM="3"
COMPLEXITY_LEVEL="hard"
POD_NAME="fabio_pod"
WEEK="week_8"

# --- Get the current UNIX timestamp ---
# This command gets the number of seconds since the Unix epoch
TIMESTAMP=$(date +%s)

# --- Construct the DIR name ---
DIR="${TRAINER_NAME}-${DB_NAME}-${INTERFACE_NUM}-${COMPLEXITY_LEVEL}-${TIMESTAMP}"

# --- Create the file PATH
FILES_PATH="./${WEEK}/${POD_NAME}/${DIR}"

git checkout -b $DIR # I'm using file anme as the branch name

mkdir $FILES_PATH

touch "${FILES_PATH}/task.json"

echo "Switched to a new branch '${FILES_PATH}' and created folder structure successfully."
