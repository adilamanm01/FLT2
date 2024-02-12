import sys

def MinDFSM(alphabets, transitions, final_states):
    A = set(final_states)
    K_A = set(range(1, len(transitions) + 1)) - A
    classes = [A, K_A] if K_A else [A]

    def state_goes_to(state, symbol):
        symbol_index = alphabets.index(symbol)
        return transitions[state - 1][symbol_index]

    def find_class(state, classes):
        for c in classes:
            if state in c:
                return c
        return None

    def refine(classes):
        new_classes = []
        for e in classes:
            if len(e) > 1:
                temp_classes = {}
                for state in e:
                    for symbol in alphabets:
                        destination_class = find_class(state_goes_to(state, symbol), classes)
                        destination_class_key = frozenset(destination_class) if destination_class else frozenset()
                        if destination_class_key not in temp_classes:
                            temp_classes[destination_class_key] = set()
                        temp_classes[destination_class_key].add(state)
                new_classes.extend([set(group) for group in temp_classes.values()])
            else:
                new_classes.append(e)
        return new_classes

    while True:
        new_classes = refine(classes)
        if set(map(frozenset, new_classes)) == set(map(frozenset, classes)):
            break
        classes = new_classes

    return classes




def eps(transitions, q, epsilon_symbol, alphabets):
    """
    Compute the epsilon closure of a state q in a finite automaton.
    Assumes states are 1-indexed in the automaton and maps them to a 0-indexed array.

    :param transitions: A list of lists representing the state transitions.
    :param q: The state (1-indexed) for which to compute the epsilon closure.
    :param epsilon_symbol: The symbol in the alphabets list representing epsilon transitions.
    :param alphabets: The list of alphabet symbols.
    :return: A set containing the epsilon closure of the given state.
    """
    epsilon_index = alphabets.index(epsilon_symbol)  # Find the index of epsilon in alphabets
    q_index = q - 1  # Adjust for 0-indexed array
    closure = {q}  # Initialize closure with state q itself

    # List to keep track of states to explore
    states_to_explore = [q_index]

    while states_to_explore:
        current_state = states_to_explore.pop()
        epsilon_transitions = transitions[current_state][epsilon_index]

        # Handle both list of transitions and single transition (non-zero integer)
        if epsilon_transitions != 0:
            # Ensure epsilon_transitions is a list for consistency
            epsilon_transitions = epsilon_transitions if isinstance(epsilon_transitions, list) else [epsilon_transitions]

            for state in epsilon_transitions:
                state_1_indexed = state  # State is 1-indexed
                if state_1_indexed not in closure:
                    closure.add(state_1_indexed)
                    states_to_explore.append(state - 1)  # Adjust for 0-indexed array

    return closure



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




