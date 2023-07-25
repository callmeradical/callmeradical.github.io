import os
import re

# Map of original tags to new consolidated tags
TAG_MAP = {
    "AWS": ["Amazon DynamoDB", "api gateway", "aurora", "AWS Lambda", "AWS re:Invent", "AWS Summit", "EC2"],
    "Cloud Engineering": ["Cloud & Serverless Technologies"],
    "Software Development": ["Blogging", "Build Process", "Cross-Platform Development", "Git", "Microservices", "Programming & Software Development", "Rails", "ruby", "teamwork"],
    "System Administration": ["linux", "Networking & Security", "nginx", "Open-Source", "Operating Systems & Environment Management", "VMware"],
    "Miscellaneous": ["apache", "Burlington Ruby Conference", "consensus algorithm", "covid", "re:Invent", "Value Stream"]
}

# Directory containing markdown files
POST_DIR = "."

# Regex to match a tags line
TAGS_REGEX = re.compile(r"^tags = \[(.*?)\]")

def replace_tags_in_file(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            match = TAGS_REGEX.match(line)
            if match:
                tags = match.group(1).split(',')
                new_tags = []
                
                for tag in tags:
                    tag = tag.strip().strip("\"")
                    for top_tag, nested_tags in TAG_MAP.items():
                        if tag in nested_tags:
                            tag = top_tag
                            break

                    new_tags.append("\"{}\"".format(tag))

                # Remove duplicates from new_tags list
                new_tags = list(dict.fromkeys(new_tags))

                line = "tags = [{}]\n".format(", ".join(new_tags))
            
            file.write(line)

# Go through each markdown file in the directory
for file_name in os.listdir(POST_DIR):
    if file_name.endswith(".md"):
        print("reading:" + file_name)
        replace_tags_in_file(os.path.join(POST_DIR, file_name))

