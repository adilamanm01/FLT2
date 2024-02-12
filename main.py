import sys

def MinDFSM(alphabets, transitions, final_states):
    # Initialize the classes A (accepting states) and K-A (non-accepting states)
    A = set(final_states)
    K_A = set(range(1, len(transitions) + 1)) - A
    classes = [A, K_A] if K_A else [A]

    def state_goes_to(state, symbol):
        # Find the transition for a state given an input symbol
        symbol_index = alphabets.index(symbol)
        transition = transitions[state - 1][symbol_index]
        return transition if transition != 0 else None

    def refine(classes):
        new_classes = []
        for e in classes:
            # Use a dictionary to group states by their transition outcomes for each symbol
            temp_classes = {}
            for state in e:
                state_signature = tuple((symbol, state_goes_to(state, symbol)) for symbol in alphabets)
                temp_classes.setdefault(state_signature, set()).add(state)
            new_classes.extend(temp_classes.values())
        return [set(c) for c in new_classes if c]

    while True:
        new_classes = refine(classes)
        # Convert classes to a comparable format (list of frozensets) to check for changes
        if set(map(frozenset, new_classes)) == set(map(frozenset, classes)):
            break
        classes = new_classes

    # Format the output to display each class as a list
    minimized_classes_formatted = [sorted(list(c)) for c in classes]
    minimized_classes_formatted.sort(key=lambda x: x[0])  # Sort by the first state in each class for readability

    return minimized_classes_formatted

def display_dfsm(alphabets, minimized_classes, transitions, final_states):
    print("alphabets :", " ".join(alphabets))
    print("\ntransitions")
    for cls in minimized_classes:
        transition_summary = {}
        for state in cls:
            for symbol_index, symbol in enumerate(alphabets):
                next_state = transitions[state-1][symbol_index]
                if next_state != 0:  # Ignore transitions to state 0 (nonexistent)
                    transition_summary[symbol] = next_state
        # Format and print the transition summary for the current class
        if transition_summary:
            trans_str = " ".join(f"{target}" for symbol, target in transition_summary.items())
            print(f"[{' '.join(map(str, cls))}] : {trans_str}")

    print("\nfinal states :", " ".join(map(str, final_states)))

def parse_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    # Check if the file is empty
    if not lines:
        print("The file is empty.")
        sys.exit(1)  # Exit the script with an error code

    # Initialize lists
    alphabets = []
    transitions = []
    final_states = []

    # Process alphabets
    alphabets = lines[0].split()

    # Process transitions
    index = 2  # Starting index for reading transitions
    while index < len(lines):
        line = lines[index]
        index += 1

        if line.strip() == '':
            # Exit the loop after processing transitions
            break

        parts = line.strip().split(' ')
        transition_row = []
        for part in parts:
            if part == '[]':
                transition_row.append(0)
            else:
                # Convert contents of the brackets to integers
                numbers = [int(x) for x in part.strip('[]').split(',')]
                transition_row.append(numbers if len(numbers) > 1 else numbers[0])
        transitions.append(transition_row)

    # Process final states (start from the line after the empty line)
    for line in lines[index:]:
        final_states.extend([int(x) for x in line.split()])

    return alphabets, transitions, final_states

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Command line path is wrong")
        sys.exit(1)

    file1_path = sys.argv[1]



    alphabets, transitions, final_states = parse_file(file1_path)
    print(alphabets,transitions,final_states,end="\n")

    # Now, call the MinDFSM function with the parsed data
    minimized_classes = MinDFSM(alphabets, transitions, final_states)
    print("Minimized Classes:", minimized_classes)


    display_dfsm(alphabets, minimized_classes, transitions, final_states)
