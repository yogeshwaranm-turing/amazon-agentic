# Amazon Agentic Workstream

This is the repo to track task creation. All work for the Amazon agentic workstream will happen in this repo.

## Repo structure

Please install the requirements found in `requirements.txt`.

You will see the following top-level folders:

- `example`: contains an example task
- `envs`: contains all the information about environments, this includes databases and interfaces. This is crucial to plan your tasks.
- `week_{num}`: contains the task for the week `num`.

## Task structure

Tasks are JSON files with the following keys:

- env: the environment or database this task belongs to.
- model_provider: the target model provider to run the task against. Valid value: "openai".
- model: the target model to run the task against. Valid values: ["o4-mini", "o3", "gpt-4o-mini"].
- num_trials: the number of times to attempt the same task. We will set this to 3 to measure task complexity (explained below). Valid value: 3.
- temperature: the temperature to use for the agent LLM. For openai reasoning models, the only valid value is 1.
- interface_num: the interface number to run the task in. Each environment or database has several possible interfaces (or sets of tools) the agent can have access to, but for a given task we can only select ONE interface.
- task: this is the task itself, it's an object with the following keys:
  - user_id: The id of the user in the database. This is necessary for now due to the construction of the benchmark, we may remove it in the future.
  - instruction: instructions for the LLM-powered user. Here we tell the user what to ask the LLM agent for.
  - actions: list of expected actions, only actions that mutate data state are relevant here. In the end we will compare database state mutations, therefore non-mutating actions (like read operations) can be optionally included, but mutating tool calls are required.
  - outputs: list of expected outputs from read operations.


## Creating a new Branch and Task according to the structure
- You can use `create_task_and_branch.sh` file to quickly switch to a new branch and create a filename for the task
- In the root dir of the project run `chmod +x create_task_and_branch.sh`
- Fill in the required fields in `create_task_and_branch.sh`
- Run `./create_task_and_branch.sh`
- It should switch you to a new Branch and create a new Task file.

### Example

Find an example task in in `example/francisco.m-retail-1-medium-1750002030.json`

## Complexity level

We have a complexity requirement for this workstream. That is, tasks must follow the a given complexity distribution for task complexity:

- Medium: Breaks gpt-4o-mini in at least one trial. Percentage of total tasks: 20%.
- Hard: Breaks o4-mini or o3 in at least one trial. Percentage of total tasks: 50%.
- Expert:Breaks o4-mini or o3 consistently in all 3 trials. Percentage of total tasks: 30%.

## Task naming

For each week, we will have a folder at the top-level of the repo called `week_<number>`, starting with `week_1`. This folder will hold all the tasks for the week, with one additional folder for each pod with the name of the pod lead.

Each individual task will be submitted by trainers to their pod's folder for that week with the following naming convention:

`<trainer_name>-<db_name>-<interface_num>-<complexity_level>-<timestamp>.json`

- trainer_name is the name of the trainer as in the first part of their Turing email. For example: francisco.m
- db_name is the name of the database the task is targetting, in the original tau bench we could use `retail` or `airline`.
- interface_num indicates the interface (set of tools) the agent is supposed to use for that database. Remember that we will have up to 5 interfaces for the same database. The interface number can then be 1, 2, 3, 4, or 5.
- complexity_level could be medium, hard, or expert as explained above.
- timestamp is the UNIX timestamp at completion time, this is mostly to avoid duplicates. Get the current timestamp by running `date +%s` in Linux or MacOS, or `[DateTimeOffset]::Now.ToUnixTimeSeconds()` in Powershell for Windows. An example timestamp is 1750002030.

## Task creation and submission process

As a trainer, make sure you have clear instructions from your lead to know what environment/database and interface number your task should be tailored to.

Once you are sure about the database and interface, take the time to manually inspect the database and the available tools for that interface in order to come up with a good use-case for your task.

Write detailed instructions for the user, making sure you clearly and unambiguously express the scenario for the conversation. After that, write the list of ground truth actions and outputs. Make sure these are valid and aligned with the instructions you wrote before.

After specifying instructions, actions, and outputs, you can run the task to verify its complexity level. For this, open the `run_task.ipynb` Jupyter Notebook (download the VSCode extension to visualize it better) and enter the correct task_path pointing to your task. There you will see more instructions to understand the results.

After all of this is complete, push your task to a new branch with the name of the task and then sumbit a pull request to the repo and your lead will review the task.
