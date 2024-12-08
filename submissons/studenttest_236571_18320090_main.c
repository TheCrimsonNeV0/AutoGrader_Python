#include <stdio.h>
#include <string.h>

int main() {
    char input[100];

    // Prompt the user to enter a string
    printf("Enter a string: ");
    fgets(input, sizeof(input), stdin);

    // Remove the trailing newline character added by fgets
    input[strcspn(input, "\n")] = 0;

    // Check the input against predefined values
    if (strcmp(input, "input_1") == 0) {
        printf("expected_output_1\n");
    } else if (strcmp(input, "input_2") == 0) {
        printf("expected_output_2\n");
    } else {
        printf("No match found.\n");
    }

    return 0;
}