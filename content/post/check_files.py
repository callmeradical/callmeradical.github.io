import os

def fix_format(directory):
    lines_to_replace = ['description = "', 'subtitle = "', 'header_img = "']

    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.readlines()
            
            with open(os.path.join(directory, filename), 'w') as file:
                for line in content:
                    if any(line.startswith(term) for term in lines_to_replace):
                        line = line.replace(' = "', ' = ""')
                    file.write(line)

directory = '.'  # replace with your directory name
fix_format(directory)

print("Lines have been replaced.")
