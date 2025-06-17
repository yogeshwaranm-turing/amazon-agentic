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
# This combines all your parts into the desired format
FILENAME="${TRAINER_NAME}-${DB_NAME}-${INTERFACE_NUM}-${COMPLEXITY_LEVEL}-${TIMESTAMP}.json"

# --- Create the file using the constructed filename ---
# 'touch' creates an empty file if it doesn't exist, or updates its timestamp if it does
FILE_PATH="./${WEEK}/${POD_NAME}/${FILENAME}"

git checkout -b $FILENAME
echo "File '${FILE_PATH}' created successfully."
touch $FILE_PATH

echo "File '${FILE_PATH}' created successfully."
