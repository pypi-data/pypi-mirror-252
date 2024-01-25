import itertools, argparse, glob, subprocess, concurrent.futures
from combocmd.version import __version__

def run_command(cmd):
    """Function to run a single command using subprocess.run."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred while running '{cmd}': {e.stderr}"

def unglob(strings):
    return [globbed_file for pattern in strings for globbed_file in glob.glob(pattern)]

def batch_process(commands, max_processes):
    """Function to process commands in batches."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_processes) as executor:
        # Map the run_command function to all the commands
        futures = {executor.submit(run_command, cmd): cmd for cmd in commands}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(futures):
            cmd = futures[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"Command '{cmd}' generated an exception: {e}")

def main():
	parser = argparse.ArgumentParser(description='Generate all combinations with replacement of strings (A, B) and (B, A), then run cmdAB and (optionally) cmdBA formatted with those strings as {combocmdA} and {combocmdB}.')
	parser.add_argument("--version", action='version', version=f'%(prog)s {__version__}')
	parser.add_argument("--strings", nargs='+', required=True, help="List of strings that will be formed into combinations with replacement and substituted for command template wildcards")
	parser.add_argument("--cmd", type=str, help="Command template to use for all combinations of --strings")
	parser.add_argument("--cmdAB", type=str, help="Command template to use for (A, B) combinations of --strings")
	parser.add_argument("--cmdBA", type=str, help="Command template to use for (B, A) combinations of --strings")
	parser.add_argument("--AisB", type=str, default="both", help="Which command to run for A=B. Options: both (--cmdAB and --cmdBA must be specified), none, cmdAB, cmdBA")
	parser.add_argument("--runRepeats", action='store_true', default=False, help="If true, then runs all formatted commands even when some are duplicates")
	parser.add_argument("--combocmdA", type=str, default="{combocmdA}", help="Wildcard to substitute with A in cmdAB or B in cmdBA. Both substitutions made if --cmd is supplied.")
	parser.add_argument("--combocmdB", type=str, default="{combocmdB}", help="Wildcard to substitute with B in cmdAB or A in cmdBA. Both substitutions made if --cmd is supplied.")
	parser.add_argument("--glob", action='store_true', default=False, help="If using wildcards to specify filenames, unpacks to a list of filenames with glob.")
	parser.add_argument("--processes", type=int, default=1, help="Number of processes to use for multiprocessing commands.")

	args = parser.parse_args()

	files = unglob(args.strings) if args.glob else args.strings
	pairs = [(A, B) for A, B in itertools.combinations_with_replacement(files, 2)]

	commands = []

	for pair in pairs:
		A, B = pair
		ccA = args.combocmdA
		ccB = args.combocmdB

		cmdAB = ""
		cmdBA = ""
		if args.cmd is not None:
			cmdAB = args.cmd.replace(ccA, A).replace(ccB, B)
			cmdBA = args.cmd.replace(ccA, B).replace(ccB, A)
		elif args.cmdAB is not None and args.cmdBA is not None:
			cmdAB = args.cmdAB.replace(ccA, A).replace(ccB, B)
			cmdBA = args.cmdBA.replace(ccA, B).replace(ccB, A)

		if A != B or args.AisB == "both": 
			commands += [cmdAB, cmdBA]
		elif A == B:
			if args.AisB == "cmdAB":
				commands.append(cmdAB)
			elif args.AisB == "cmdBA":
				commands.append(cmdBA)


	if not args.runRepeats:
		commands = list(set(commands))
	batch_process(commands, args.processes)

if __name__ == "__main__":
	main()
