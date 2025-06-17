# Change this information
TRAINER_NAME="adnan.k1"
DB_NAME="airline"
INTERFACE_NUM="1"
COMPLEXITY_LEVEL="medium"
POD_NAME="michael_pod"
WEEK="week_1"

# --- Get the current UNIX timestamp ---
# This command gets the number of seconds since the Unix epoch
TIMESTAMP=$(date +%s)

# --- Construct the full filename ---
FILENAME="${TRAINER_NAME}-${DB_NAME}-${INTERFACE_NUM}-${COMPLEXITY_LEVEL}-${TIMESTAMP}.json"

# --- Create the file PATH
FILE_PATH="./${WEEK}/${POD_NAME}/${FILENAME}"

git checkout -b $FILENAME # I'm using file anme as the branch name

touch $FILE_PATH

echo "Switched to a new branch and File '${FILE_PATH}' created successfully."
