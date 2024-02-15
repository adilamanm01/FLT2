import sys

def remove_unreachable_states(transitions, final_states):
    reachable_states = {1}
    new_reachables_found = True

    while new_reachables_found:
        new_reachables_found = False
        for state in list(reachable_states):
            for transition in transitions[state-1]:  # -1 for 0-based index
                if transition not in reachable_states and transition != 0:
                    reachable_states.add(transition)
                    new_reachables_found = True

    # Filter out unreachable transitions
    filtered_transitions = [transitions[i-1] for i in reachable_states if i-1 < len(transitions)]
    
    # Update final states to include only reachable states
    filtered_final_states = [state for state in final_states if state in reachable_states]
    
    return filtered_transitions, filtered_final_states


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
        cls_index = 0  # Start indexing from 0
        for cls in classes:
            for state in cls:
                state_to_class_mapping[state] = cls_index
            cls_index += 1  # Increment the index manually after processing each class


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
        output = " ".join(alphabets) + "\n\n"
        
        # Initialize new_transitions with default self-transitions for each state
        new_transitions = {}
        for i in range(1, len(minimized_classes) + 1):
            new_transitions[i] = {symbol: i for symbol in alphabets}
        
        # Adjust new_transitions based on the minimization results
        state = 1
        for cls in minimized_classes:
            for symbol in alphabets:
                symbol_index = alphabets.index(symbol)
                transition_states = set()
                for orig_state in cls:
                    transition_state = transitions[orig_state-1][symbol_index]
                    transition_states.add(transition_state)
                
                # For simplicity, assuming single transition state per symbol, adjust as necessary
                    if transition_states:
                        # Find the new state number for the transition state
                        new_state_index = 1  # Start the new state numbering from 1
                        for trans_state in transition_states:
                            found = False  # Flag to check if the transition state is found in minimized classes
                            for new_cls in minimized_classes:
                                if trans_state in new_cls:
                                    new_transitions[state][symbol] = new_state_index
                                    found = True
                                    break  # Break inner loop if transition state is found
                                new_state_index += 1  # Increment new state number after checking each class
                            if found:
                                break  # Break outer loop if transition state is found
                            new_state_index = 1  # Reset the new state index for the next symbol's transition state

            state += 1
        
        # Writing to file and printing
        for state in range(1, len(new_transitions) + 1):
            trans_dict = new_transitions[state]
            trans_line = ' '.join(str(trans_dict[s]) for s in alphabets)
            output_line = f"{trans_line}\n"
            output += output_line
        
        # Initialize the set to hold new final states
        new_final_states_set = set()

        # Manually manage new state numbers
        new_state = 1
        for cls in minimized_classes:
            for original_final_state in final_states:
                if original_final_state in cls:
                    new_final_states_set.add(new_state)
                    break  # Once the final state is found in a class, no need to check other classes for this state
            new_state += 1  # Increment the new state number for the next class


        minimized_final_states = sorted(list(new_final_states_set))
        
        # Existing output formatting logic for transitions
        
        # Adjust output for final states to reflect minimized states
        final_states_output = " ".join(map(str, minimized_final_states))
        output += "\n" + final_states_output + "\n"
        
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
    # try:
        if len(sys.argv) != 3:
            print("Command line path is wrong")
            sys.exit(1)

        file1_path = sys.argv[1]
        file2_path = sys.argv[2]



        alphabets, transitions, final_states = parse_file(file1_path)

        alphalength=len(alphabets)
        translength=len(transitions)

        # print(alphalength,"\n")
        # print(translength,"\n")
        for i in range(len(alphabets)):
                if len(alphabets[i])!=1:
                    print("alphabet length is more than 2")
                    exit(1)

        if len(final_states)==0:
            print("Invalid DFSM...")
            exit(1)

        for i in range(translength):
            if len(transitions[i])!= alphalength:
                print("Invalid DFSM")
                exit(1)

        # Iterate through each row and each integer in the transitions matrix
        for i in range(translength):
            for j in range(len(transitions[i])):  # Assuming alphalength is the length of a row, which is 2 in your example
                if transitions[i][j] > translength:
                        print(f"Error: Integer {transitions[i][j]} at transitions[{i}][{j}] is not <= {translength}")
                        sys.exit("DFSM Invalid.")
        
        for i in range(len(transitions)):
            for j in range(len(transitions[i])):
                element = transitions[i][j]
                # Check if the element is a string that represents a digit
                if isinstance(element, str) and not element.isdigit():
                    print(f"Error: Element '{element}' at transitions[{i}][{j}] is not a digit.")
                    sys.exit("DFSM Invalid.")
                # Additional check if the element is an integer and not <= translength
                elif isinstance(element, int) and element > len(transitions):
                    print(f"Error: Integer {element} at transitions[{i}][{j}] is not <= {len(transitions)}")
                    sys.exit("DFSM Invalid.")

        for i in range(len(final_states)):
            if final_states[i] > translength:
                print("Invalid DFSM..")
                exit(1)
        

        
        print(alphabets,transitions,final_states,end="\n")


        # Removing unreachable states and updating transitions and final states
        transitions, final_states = remove_unreachable_states(transitions, final_states)

        print("After removing Unrechable :",alphabets,transitions,final_states,end="\n")

        # Now, call the MinDFSM function with the parsed data
        minimized_classes = MinDFSM(alphabets, transitions, final_states)
        print("Minimized Classes:", minimized_classes)


        display_dfsm(alphabets, minimized_classes, transitions, final_states)


        # print(len(alphabets[0]))
    # except Exception as e:
        # # This catches any exception raised during the execution of the script
        # print(f"Invalid DFSM")
        # # Optionally, exit the script with a non-zero exit code to indicate an error
        # sys.exit(1)
