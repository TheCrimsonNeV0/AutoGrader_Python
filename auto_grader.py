import csv
import subprocess
import os

folder_path = "submissions"

# List of expected outputs for each run
expected_outputs = ["expected_output_1", "expected_output_2"]  # Replace with the actual expected outputs

# List of input data for each run
input_data_list = ["input_1", "input_2"]  # Replace with the actual input data

# List of program arguments (if any). Leave empty if none are needed.
program_args = []

# CSV file path to store results
csv_file_path = "output_results.csv"

# File path to store all outputs from every program execution
all_outputs_file_path = "all_outputs.txt"

with open(csv_file_path, mode="w", newline="") as csv_file, open(all_outputs_file_path, mode="w") as all_outputs_file:
    csv_writer = csv.writer(csv_file)

    # Dynamically create the header row with columns for each comparison
    header_row = ["name"] + [f"match_{i+1}" for i in range(len(input_data_list))]
    csv_writer.writerow(header_row)

    # Iterate over all C files in the submissions folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".c"):
            file_path = os.path.join(folder_path, filename)

            # Extract binary name without the ".c" extension
            binary_name = filename[:-2]
            binary_path = os.path.join(folder_path, binary_name + ".o")  # Use ".o" as the extension for compiled binaries
            binary_identifier = binary_name.split('_', 1)[0]

            # Compile the C file
            compile_result = subprocess.run(["gcc", file_path, "-o", binary_path], capture_output=True, text=True)

            # Check if the compilation was successful
            if compile_result.returncode == 0:
                match_results = []  # Store the match result for each run

                # Loop through each input/expected output pair
                for idx, (input_data, expected_output) in enumerate(zip(input_data_list, expected_outputs)):
                    command = [binary_path] + program_args if program_args else [binary_path]

                    try:
                        # Run the compiled program with the current input data and set a timeout
                        run_result = subprocess.run(command, input=input_data, capture_output=True, text=True, timeout=5)

                        # Compare the program's output to the expected output
                        output_matches = 1 if expected_output.strip().lower() in run_result.stdout.strip().lower() else 0

                        # Append the match result for this run
                        match_results.append(output_matches)

                        # Write the output to the all_outputs.txt file
                        all_outputs_file.write(f"{binary_identifier} (Run {idx+1}):\n{run_result.stdout}\n")
                        all_outputs_file.write("=" * 33 + "\n")
                        all_outputs_file.flush()  # Flush the output after writing

                    except subprocess.TimeoutExpired:
                        # Handle timeout
                        match_results.append(0)
                        all_outputs_file.write(f"{binary_identifier} (Run {idx+1}):\nCode timed out (5 seconds)\n")
                        all_outputs_file.write("=" * 33 + "\n")
                        all_outputs_file.flush()  # Flush the output after writing

                # Write the match results for this binary to the CSV file
                csv_writer.writerow([binary_identifier] + match_results)

                # Remove the compiled binary after use
                os.remove(binary_path)
            else:
                # If compilation failed, write a -1 for each run to indicate failure
                csv_writer.writerow([binary_identifier] + [-1] * len(input_data_list))

                # Write the compilation error to the all_outputs.txt file
                all_outputs_file.write(f"{binary_identifier}:\nCompilation failed.\n")
                all_outputs_file.write("=" * 33 + "\n")
                all_outputs_file.flush()  # Flush the output after writing

print(f"Results written to {csv_file_path}")
print(f"All outputs written to {all_outputs_file_path}")