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
        # Create a mapping from state to its current class
        state_to_class_mapping = {}
        for cls_index, cls in enumerate(classes):
            for state in cls:
                state_to_class_mapping[state] = cls_index

        for e in classes:
            temp_classes = {}
            for state in e:
                # Adjust to capture state transitions as transitions to classes
                state_signature = tuple(state_to_class_mapping[state_goes_to(state, symbol)] if state_goes_to(state, symbol) in state_to_class_mapping else None for symbol in alphabets)
                temp_classes.setdefault(state_signature, set()).add(state)
            new_classes.extend(temp_classes.values())
        return [set(c) for c in new_classes if c]

    while True:
        new_classes = refine(classes)
        if set(map(frozenset, new_classes)) == set(map(frozenset, classes)):
            break
        classes = new_classes

    minimized_classes_formatted = [sorted(list(c)) for c in classes]
    minimized_classes_formatted.sort(key=lambda x: x[0])

    return minimized_classes_formatted


def display_dfsm(alphabets, minimized_classes, transitions, final_states):
    with open(file2_path, 'w') as file:
        output = "\nalphabets : " + " ".join(alphabets) + "\n"
        print(output.strip())
        file.write(output)
        
        # Assigning new numerical state IDs to minimized classes
        class_to_new_state = {frozenset(cls): i + 1 for i, cls in enumerate(minimized_classes)}
        
        # Initialize new transitions dictionary
        new_transitions = {i+1: {} for i in range(len(minimized_classes))}
        
        # Mapping transitions of old states to new state IDs
        output = "\ntransitions\n"
        for cls_index, cls in enumerate(minimized_classes):
            new_state = cls_index + 1
            for state in cls:
                for symbol_index, symbol in enumerate(alphabets):
                    original_transition = transitions[state-1][symbol_index]
                    if original_transition != 0:
                        for target_cls_index, target_cls in enumerate(minimized_classes):
                            if original_transition in target_cls:
                                new_target_state = target_cls_index + 1
                                new_transitions[new_state][symbol] = new_target_state
        
        # Writing and printing the new transitions in the desired format
        for state, transitions_dict in new_transitions.items():
            transition_list = [str(transitions_dict[symbol] if transitions_dict[symbol] is not None else state) for symbol in alphabets]
            line = f"[{state}] : {' '.join(transition_list)}\n"
            print(line.strip())
            output += line
        
        file.write(output)
        
        # Updating final states based on minimized classes
        new_final_states = set()
        for cls_index, cls in enumerate(minimized_classes):
            if set(cls).intersection(set(final_states)):
                new_final_states.add(cls_index + 1)

        output = "\nfinal states : " + " ".join(map(str, sorted(new_final_states))) + "\n"
        print(output.strip())
        file.write(output)



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
    if len(sys.argv) != 3:
        print("Command line path is wrong")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]



    alphabets, transitions, final_states = parse_file(file1_path)
    print(alphabets,transitions,final_states,end="\n")

    # Now, call the MinDFSM function with the parsed data
    minimized_classes = MinDFSM(alphabets, transitions, final_states)
    print("Minimized Classes:", minimized_classes)


    display_dfsm(alphabets, minimized_classes, transitions, final_states)
