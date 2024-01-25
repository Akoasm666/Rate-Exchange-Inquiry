# Function defined for replacing repeated characters
def replace_repeated_chars(input):
    # Make a list to store the final result
    result = []
    for i in range(len(input)):
        # Check if the current character is in the last 10 characters, if so, append "-" to the result list
        if input[i] in input[max(0, i-10):i]:
            result.append('-')
        else:
            result.append(input[i])
    return ''.join(result)


# Test the code
if __name__ == "__main__":
    input = "abcdefaxc"
    output = replace_repeated_chars(input)
    print("input:", input)
    print("output:", output)

    input = "abcdefaxcqwertba"
    output = replace_repeated_chars(input)
    print("input:", input)
    print("output:", output)


################## Test Result ##################
# input: abcdefaxc
# output: abcdef-x-
# input: abcdefaxcqwertba
# output: abcdef-x-qw-rtb-