import os

# This is the Gale-Shapley matcher. Its arg is a formatted input file.
def matcher(input_file):
    # Read the input file.
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    # The first line is n.
    n = int(lines[0])
    
    # The next n lines are hospital preferences.
    hospital_prefs = {}
    for i in range(1, n + 1):
        hospital = i
        prefs = list(map(int, lines[i].split()))
        hospital_prefs[hospital] = prefs
    
    # The next n lines are student preferences.
    student_prefs = {}
    for i in range(n + 1, 2 * n + 1):
        student = i - n
        prefs = list(map(int, lines[i].split()))
        student_prefs[student] = prefs
    
    # Matches are stored as hospital: student and in reverse for lookup.
    matches = {}
    reverse_matches = {}
    
    # Run the Gale-Shapley algorithm.
    unmatched_hospitals = list(range(1, n + 1))
    while unmatched_hospitals:
        h = unmatched_hospitals.pop(0)
        
        for student in hospital_prefs[h]:
            # If student is unmatched, create a new match.
            if student not in reverse_matches:
                matches[h] = student
                reverse_matches[student] = h
                break

            # If student is matched, find their current hospital.
            else:
                current_hospital = reverse_matches[student]
                
                h_pos = student_prefs[student].index(h)
                curr_h_pos = student_prefs[student].index(current_hospital)
                
                # If student prefers new hospital h, update matches.
                if h_pos < curr_h_pos:
                    del matches[current_hospital]
                    del reverse_matches[student]

                    matches[h] = student
                    reverse_matches[student] = h

                    unmatched_hospitals.append(current_hospital)
                    break
                # Otherwise, continue to next student in h's list.
    
    # Print the output
    for hospital in sorted(matches.keys()):
        print(f"{hospital} {matches[hospital]}")


# This is the main function.
def main():
    # Get user input to determine the input file.
    test_num = input("Enter the test number to run (e.g., 1 for test1): ").strip()
    
    # Ensure the input is valid and the file number exists.
    try:
        test_num = int(test_num)
        input_file = f"tests/test{test_num}/test{test_num}_input.txt"
        
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"Test file '{input_file}' not found. Defaulting to test1.")
            input_file = "tests/test1/test1_input.txt"

    except (ValueError, TypeError):
        print("Invalid input, defaulting to test1. Please enter an integer.")
        input_file = "tests/test1/test1_input.txt"
    
    # Run the matcher.
    matcher(input_file)


if __name__ == '__main__':
    main()