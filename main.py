import sys

 # Define a function to remove unreachable states from a given set of transitions and final states
def remove_unreachable_states(transitions, final_states):
    # Initialize a set with state 1 as initially reachable
    reachable_states = {1}
    # Flag to indicate whether new reachable states were found in the last iteration
    new_reachables_found = True

    # Continue looping as long as new reachable states are being found
    while new_reachables_found:
        # Reset the flag for this iteration
        new_reachables_found = False
        # Iterate through the currently known reachable states
        for state in list(reachable_states):
            # Iterate through transitions from the current state
            for transition in transitions[state-1]:  # Assumes 1-based indexing for states
                # If a transition leads to an unreachable state (that is not a dummy state represented by 0),
                # add it to the set of reachable states and indicate that new states have been found
                if transition not in reachable_states and transition != 0:
                    reachable_states.add(transition)
                    new_reachables_found = True

    # Create a mapping from old state numbers to new, compacted state numbers based on the set of reachable states
    state_mapping = {old: new for new, old in enumerate(sorted(reachable_states), start=1)}

    # Apply the state number mapping to filter and reorder the transitions for the reachable states
    filtered_transitions = [transitions[old-1] for old in sorted(reachable_states)]
    
    # Apply the state number mapping to filter the final states to include only those that are reachable
    filtered_final_states = [state_mapping[state] for state in final_states if state in reachable_states]
    
    # Return the filtered and renumbered transitions and final states, along with the state mapping
    return filtered_transitions, filtered_final_states, state_mapping



def MinDFSM(alphabets, transitions, final_states):
    # Split states into accepting (A) and non-accepting (K-A) states.
    A = set(final_states)  # Accepting states.
    K_A = set(range(1, len(transitions) + 1)) - A  # Non-accepting states, calculated by subtracting A from all states.
    classes = [A, K_A] if K_A else [A]  # Initial partition of states into two classes, unless there are no non-accepting states.

    def state_goes_to(state, symbol):
        # Determine the state transition for a given state and input symbol.
        symbol_index = alphabets.index(symbol)  # Find the index of the symbol in the alphabet list.
        transition = transitions[state - 1][symbol_index]  # Access the transition for the given state and symbol.
        return transition if transition != 0 else None  # Return the transition state if it exists; otherwise, return None.

    def refine(classes):
        new_classes = []  # Prepare a list for refined classes.
        # Create a mapping from each state to its current class index.
        state_to_class_mapping = {}
        cls_index = 0  # Start class indices from 0.
        for cls in classes:
            for state in cls:
                state_to_class_mapping[state] = cls_index
            cls_index += 1  # Increment class index for each class.

        # Refine classes based on state transitions.
        for e in classes:
            temp_classes = {}  # Temporary storage for newly forming classes.
            for state in e:
                # Create a signature for each state based on transitions to class indices for all alphabets.
                state_signature = tuple(state_to_class_mapping[state_goes_to(state, symbol)] if state_goes_to(state, symbol) in state_to_class_mapping else None for symbol in alphabets)
                temp_classes.setdefault(state_signature, set()).add(state)
            new_classes.extend(temp_classes.values())  # Add newly formed classes to the list of new classes.
        return [set(c) for c in new_classes if c]  # Filter out any empty classes and return the list of new classes.

    # Main loop to refine classes until no further refinement is possible.
    while True:
        new_classes = refine(classes)  # Attempt to refine the current classes.
        # Check if refinement has made any changes; if not, the process is complete.
        if set(map(frozenset, new_classes)) == set(map(frozenset, classes)):
            break  # Exit loop if no changes were made in the last refinement.
        classes = new_classes  # Update classes for the next iteration.

    # Format the minimized classes for output.
    minimized_classes_formatted = [sorted(list(c)) for c in classes]  # Convert each class set to a sorted list.
    minimized_classes_formatted.sort(key=lambda x: x[0])  # Sort the classes based on the first state in each class.

    return minimized_classes_formatted  # Return the formatted list of minimized classes.


# Define a function to display the DFSM in a human-readable format and write it to a file
def display_dfsm(alphabets, minimized_classes, transitions, final_states):
    # Open the specified file in write mode
    with open(file2_path, 'w') as file:
        # Start building the output string with the alphabets separated by spaces
        output = " ".join(alphabets) + "\n\n"
        
        # Initialize a dictionary to store the new transitions for each state
        new_transitions = {}
        # Create default self-transitions for each state based on the minimized classes
        for i in range(1, len(minimized_classes) + 1):
            new_transitions[i] = {symbol: i for symbol in alphabets}
        
        # Iterate through the minimized classes to adjust the transitions based on the minimization results
        state = 1
        for cls in minimized_classes:
            for symbol in alphabets:
                symbol_index = alphabets.index(symbol)
                transition_states = set()
                # Collect the transition states for each original state in the class
                for orig_state in cls:
                    transition_state = transitions[orig_state-1][symbol_index]
                    transition_states.add(transition_state)
                
                # Assuming there is only one transition state per symbol, adjust the transitions accordingly
                if transition_states:
                    new_state_index = 1  # Initialize the state numbering for the new transitions
                    for trans_state in transition_states:
                        found = False  # Flag to indicate if the transition state has been found in the minimized classes
                        for new_cls in minimized_classes:
                            if trans_state in new_cls:
                                # Update the transition for the current state and symbol
                                new_transitions[state][symbol] = new_state_index
                                found = True
                                break  # Stop searching once the transition state is found
                            new_state_index += 1  # Increment the state number for each checked class
                        if found:
                            break  # Exit the loop if the transition state has been matched
                    new_state_index = 1  # Reset the state index for the next symbol's transition

            state += 1  # Increment the state counter after processing each class
        
        # Compile the new transitions into the output string
        for state in range(1, len(new_transitions) + 1):
            trans_dict = new_transitions[state]
            # Format each state's transitions for the output
            trans_line = ' '.join(str(trans_dict[s]) for s in alphabets)
            output_line = f"{trans_line}\n"
            output += output_line  # Add the formatted transition line to the output
        
        # Initialize a set to hold the new final states based on the minimized classes
        new_final_states_set = set()
        new_state = 1  # Start numbering the new final states
        for cls in minimized_classes:
            for original_final_state in final_states:
                if original_final_state in cls:
                    new_final_states_set.add(new_state)
                    break  # Only add the state once if it matches an original final state
            new_state += 1  # Increment the state number for each processed class

        # Sort and format the new final states for the output
        minimized_final_states = sorted(list(new_final_states_set))
        # Compile the final states into the output string
        final_states_output = " ".join(map(str, minimized_final_states))
        output += "\n" + final_states_output + "\n"
        
        # Print the complete output to the console
        print(output.strip())
        # Write the output to the file
        file.write(output)





def parse_file(file_name):
    with open(file_name, 'r') as file:  # Open the file in read mode.
        lines = file.readlines()  # Read all lines in the file and store them in a list.
    
    # Check if the file is empty
    if not lines:  # Check if the list of lines is empty, indicating the file is empty.
        print("The file is empty.")
        sys.exit(1)  # Exit the program with an error status 1 if the file is empty.

    # Initialize lists
    alphabets = []  # List to store alphabets used in the finite state machine.
    transitions = []  # List to store transitions between states.
    final_states = []  # List to store final (accepting) states.

    # Process alphabets
    alphabets = lines[0].split()  # Split the first line by whitespace to get the alphabet.

    # Process transitions
    index = 2  # Start processing transitions from the third line (index 2).
    while index < len(lines):  # Loop through the lines starting from the third.
        line = lines[index]  # Get the current line.
        index += 1  # Increment the index to move to the next line.

        if line.strip() == '':  # Check if the line is empty (a blank line).
            break  # Stop processing transitions if an empty line is found.

        parts = line.strip().split(' ')  # Split the line into parts based on whitespace.
        transition_row = []  # List to store transitions for a single state.
        for part in parts:  # Loop through each part in the line.
            if part == '[]':  # Check if the part represents an empty transition.
                transition_row.append(0)  # Use 0 to represent an empty transition.
            else:
                # Convert the string within brackets to a list of integers.
                numbers = [int(x) for x in part.strip('[]').split(',')]
                # If there is more than one number, store it as a list; otherwise, store just the number.
                transition_row.append(numbers if len(numbers) > 1 else numbers[0])
        transitions.append(transition_row)  # Add the transitions for this state to the main list.

    # Process final states (start from the line after the empty line)
    for line in lines[index:]:  # Loop through the remaining lines to process final states.
        # Split the line by whitespace and convert each part to an integer, then extend the final_states list with these integers.
        final_states.extend([int(x) for x in line.split()])

    return alphabets, transitions, final_states  # Return the processed data.

def state_goes_to(state, symbol, state_mapping):
    # Adjust state number according to mapping
    if state in state_mapping:  # Check if the current state has a mapping.
        mapped_state = state_mapping[state]  # Get the mapped state.
        symbol_index = alphabets.index(symbol)  # Get the index of the symbol in the alphabet list.
        transition = transitions[mapped_state - 1][symbol_index]  # Get the transition for the mapped state and symbol.
        return transition if transition != 0 else None  # Return the transition if it exists; otherwise, return None.
    else:
        return None  # Return None if the state is not in the mapping.



if __name__ == "__main__":
    try:
        # Check if the correct number of command-line arguments are provided
        if len(sys.argv) != 3:
            print("Command line path is wrong")
            sys.exit(1)

        # Assign the first and second command-line arguments to file paths
        file1_path = sys.argv[1]
        file2_path = sys.argv[2]

        # Parse the DFSM from the input file
        alphabets, transitions, final_states = parse_file(file1_path)

        # Validate the alphabet and transitions lengths
        alphalength = len(alphabets)
        translength = len(transitions)

        # Ensure each alphabet symbol is a single character
        for i in range(len(alphabets)):
            if len(alphabets[i]) != 1:
                print("alphabet length is more than 2")
                exit(1)

        # Check that there is at least one final state
        if len(final_states) == 0:
            print("Invalid DFSM...")
            exit(1)

        # Validate that each state has a transition for each alphabet symbol
        for i in range(translength):
            if len(transitions[i]) != alphalength:
                print("Invalid DFSM")
                exit(1)

        # Ensure all transitions are to valid states
        for i in range(translength):
            for j in range(len(transitions[i])):
                if transitions[i][j] > translength:
                    print(f"Error: Integer {transitions[i][j]} at transitions[{i}][{j}] is not <= {translength}")
                    sys.exit("DFSM Invalid.")

        # Check for non-digit elements in transitions and validate transition values
        for i in range(len(transitions)):
            for j in range(len(transitions[i])):
                element = transitions[i][j]
                if isinstance(element, str) and not element.isdigit():
                    print(f"Error: Element '{element}' at transitions[{i}][{j}] is not a digit.")
                    sys.exit("DFSM Invalid.")
                elif isinstance(element, int) and element > len(transitions):
                    print(f"Error: Integer {element} at transitions[{i}][{j}] is not <= {len(transitions)}")
                    sys.exit("DFSM Invalid.")

        # Validate that all final states refer to valid states
        for i in range(len(final_states)):
            if final_states[i] > translength:
                print("Invalid DFSM..")
                exit(1)

        # Print the initial DFSM components
        print(alphabets, transitions, final_states, end="\n")

        # Remove unreachable states from the DFSM
        transitions, final_states, state_mapping = remove_unreachable_states(transitions, final_states)

        # Print the DFSM after removing unreachable states
        print("After removing Unreachable :", "alphabets \n:", alphabets, "transitions : \n", transitions, "final states", final_states)

        # Minimize the DFSM
        minimized_classes = MinDFSM(alphabets, transitions, final_states)
        print("Minimized Classes:", minimized_classes)

        # Display and write the minimized DFSM to a file
        display_dfsm(alphabets, minimized_classes, transitions, final_states)

    except Exception as e:
        # This catches any exception raised during the execution of the script
        print(f"Invalid DFSM")
        # Optionally, exit the script with a non-zero exit code to indicate an error
        sys.exit(1)
