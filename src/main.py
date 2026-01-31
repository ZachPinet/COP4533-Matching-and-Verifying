import os
import time


# This is the Gale-Shapley matcher. Its arg is a formatted input file.
def matcher(input_file):
    try:
        # Read the input file.
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        
        # Check if the file is empty.
        if not lines:
            print("Error: input file is invalid!")
            return None
        
        # The first line is n.
        n = int(lines[0])
        
        # Check if there is the correct number of lines.
        if len(lines) != 2 * n + 1:
            print("Error: input file is invalid!")
            return None
        
        # The next n lines are hospital preferences.
        hospital_prefs = {}
        for i in range(1, n + 1):
            hospital = i
            prefs = list(map(int, lines[i].split()))
            
            # Check that each list of preferences has length n.
            if len(prefs) != n:
                print("Error: input file is invalid!")
                return None
            
            # Check that each list has no duplicate values.
            if len(set(prefs)) != n:
                print("Error: input file is invalid!")
                return None
            
            # Check that each list has all values in range 1-n.
            if any(p < 1 or p > n for p in prefs):
                print("Error: input file is invalid!")
                return None
            
            hospital_prefs[hospital] = prefs
        
        # The next n lines are student preferences.
        student_prefs = {}
        for i in range(n + 1, 2 * n + 1):
            student = i - n
            prefs = list(map(int, lines[i].split()))
            
            # Check that each list of preferences has length n.
            if len(prefs) != n:
                print("Error: input file is invalid!")
                return None
            
            # Check that each list has no duplicate values.
            if len(set(prefs)) != n:
                print("Error: input file is invalid!")
                return None
            
            # Check that each list has all values in range 1-n.
            if any(p < 1 or p > n for p in prefs):
                print("Error: input file is invalid!")
                return None
            
            student_prefs[student] = prefs
        
        # Matches are stored as {h: s} and in reverse for lookup.
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
        
        return matches
    
    except (ValueError, IndexError, KeyError):
        print("Error: input file is invalid!")
        return None


# This is the verifier. It checks an output's validity and stability.
def verifier(matches, input_file):
    if matches is None:
        return
    
    try:
        # Read the input file.
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        
        n = int(lines[0])
        
        # Get hospital preferences.
        hospital_prefs = {}
        for i in range(1, n + 1):
            hospital = i
            prefs = list(map(int, lines[i].split()))
            hospital_prefs[hospital] = prefs
        
        # Get student preferences.
        student_prefs = {}
        for i in range(n + 1, 2 * n + 1):
            student = i - n
            prefs = list(map(int, lines[i].split()))
            student_prefs[student] = prefs
        
        is_valid = True
        # Check that each hospital is matched up.
        if len(matches) != n:
            is_valid = False
            print(f"INVALID: Found {len(matches)} matches instead of {n}.")

        # Check for duplicate hospitals.
        if len(matches.keys()) != len(set(matches.keys())):
            is_valid = False
            print("INVALID: Duplicate hospitals in matching.")
        
        # Check for duplicate students.
        matched_students = list(matches.values())
        if len(matched_students) != len(set(matched_students)):
            is_valid = False
            print("INVALID: Duplicate students in matching.")
        
        is_stable = True
        reverse_matches = {s: h for h, s in matches.items()}
        # Check all possible pairs for blocking pairs
        found_blocking_pair = False
        for h in range(1, n + 1):
            if found_blocking_pair:
                break
            for s in range(1, n + 1):
                # Skip if this is already the current match.
                if matches.get(h) == s:
                    continue
                
                # Get the current matches.
                curr_student = matches.get(h)
                curr_hospital = reverse_matches.get(s)
                
                # Check if h prefers s to current match.
                if curr_student is not None:
                    s_pos = hospital_prefs[h].index(s)
                    curr_s_pos = hospital_prefs[h].index(curr_student)
                    if s_pos < curr_s_pos:
                        h_prefers_s = True
                    else:
                        h_prefers_s = False
                else:
                    h_prefers_s = True
                
                # Check if s prefers h to current match.
                if curr_hospital is not None:
                    h_pos = student_prefs[s].index(h)
                    curr_h_pos = student_prefs[s].index(curr_hospital)
                    if h_pos < curr_h_pos:
                        s_prefers_h = True
                    else:
                        s_prefers_h = False
                else:
                    s_prefers_h = True
                
                # A blocking pair exists if both prefer each other.
                if h_prefers_s and s_prefers_h:
                    is_stable = False
                    found_blocking_pair = True
                    print(f"UNSTABLE: ({h}, {s})")
                    break
        
        if is_valid and is_stable:
            print("VALID STABLE")
    
    except Exception as e:
        print(f"Error during verification: {e}")


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
    
    # Run the matcher and measure its time.
    start_time = time.time()
    matches_output = matcher(input_file)
    matcher_time = time.time() - start_time

    # Run the verifier and measure its time.
    start_time = time.time()
    verifier(matches_output, input_file)
    verifier_time = time.time() - start_time
    
    # Print timing results
    print(f"\nMatcher runtime: {matcher_time:.6f} seconds")
    print(f"Verifier runtime: {verifier_time:.6f} seconds")
    verifier(matches_output, input_file)


if __name__ == '__main__':
    main()