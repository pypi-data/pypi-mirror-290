from ai_commit_msg.core.gen_commit_msg import generate_commit_message
from ai_commit_msg.services.git_service import GitService
from ai_commit_msg.utils.logger import Logger
from ai_commit_msg.utils.utils import execute_cli_command

def print_summary(summary):
  Logger().log(f"""Here is a summary of your changes:

  {summary}

to use this summary run: `git commit -m "{summary}"`
""")

def summary_handler(args):
  if args.unstaged:
    Logger().log("Fetching your unstaged changes...\n")
    unstaged_changes_diff = execute_cli_command(['git', 'diff'])
    ai_commit_msg = generate_commit_message(unstaged_changes_diff.stdout)
    print_summary(ai_commit_msg)
    return

  Logger().log("Fetching your staged changes...\n")

  if(len(GitService.get_staged_files()) == 0):
    Logger().log("🚨 No files are staged for commit. Run `git add` to stage some of your changes")
    return

  staged_changes_diff = execute_cli_command(['git', 'diff', '--staged'])
  ai_commit_msg = generate_commit_message(staged_changes_diff.stdout)

  print_summary(ai_commit_msg)