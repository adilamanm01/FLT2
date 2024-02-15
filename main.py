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
        output = " ".join(alphabets) + "\n"
        print("\n")
        print(output.strip())
        print("\n")
        file.write(output)
        
        # Initialize an empty dictionary for mapping classes to new state IDs
        class_to_new_state = {}
        cls_index = 1  # Start indexing from 1 since state numbering begins from 1

        for cls in minimized_classes:
            class_to_new_state[frozenset(cls)] = cls_index
            cls_index += 1  # Increment the index manually for each class

        
        # Initialize new transitions dictionary
        new_transitions = {i+1: {} for i in range(len(minimized_classes))}
        
        # Initialize a variable for output string accumulation
        output = "\n"

        # Manually manage the index for cls_index starting from 1
        cls_index = 1
        for cls in minimized_classes:
            new_state = cls_index  # Use the manually managed index for new_state
            for state in cls:
                symbol_index = 0  # Initialize symbol_index manually
                for symbol in alphabets:
                    original_transition = transitions[state-1][symbol_index]
                    if original_transition != 0:
                        # Manually manage the index for target_cls_index starting from 1
                        target_cls_index = 1
                        for target_cls in minimized_classes:
                            if original_transition in target_cls:
                                new_target_state = target_cls_index  # Use the manually managed index for new_target_state
                                new_transitions[new_state][symbol] = new_target_state
                                break  # Exit the loop once the matching target class is found
                            target_cls_index += 1  # Increment the target_cls_index manually
                    symbol_index += 1  # Increment the symbol_index manually after each iteration
            cls_index += 1  # Increment the cls_index manually


        
        # Writing and printing the new transitions in the desired format
        for state, transitions_dict in new_transitions.items():
            transition_list = [str(transitions_dict[symbol] if transitions_dict[symbol] is not None else state) for symbol in alphabets]
            line = f"{' '.join(transition_list)}\n"
            print(line.strip())
            output += line
        
        file.write(output)
        
        # Updating final states based on minimized classes
        new_final_states = set()
        new_final_states = set()
        cls_index = 1  # Start indexing from 1 since state numbering begins from 1
        for cls in minimized_classes:
            if set(cls).intersection(set(final_states)):
                new_final_states.add(cls_index)
            cls_index += 1  # Increment the index manually

        output = "\n" + " ".join(map(str, sorted(new_final_states))) + "\n"
        print("\n")
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
    try:
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

        # Now, call the MinDFSM function with the parsed data
        minimized_classes = MinDFSM(alphabets, transitions, final_states)
        print("Minimized Classes:", minimized_classes)


        display_dfsm(alphabets, minimized_classes, transitions, final_states)


        # print(len(alphabets[0]))
    except Exception as e:
        # This catches any exception raised during the execution of the script
        print(f"Invalid DFSM")
        # Optionally, exit the script with a non-zero exit code to indicate an error
        sys.exit(1)
