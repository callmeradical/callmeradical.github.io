import os
import re

TAGS_REGEX = re.compile(r"^tags = \[(.*?)\]")
CATEGORIES_REGEX = re.compile(r"^categories = \[(.*?)\]")

TAG_MAP = {
    "AWS Lambda": ["AWS"],
    "AWS re:Invent": ["AWS"],
    "AWS Summit": ["AWS"],
    "Azure CosmosDB": ["Azure"],
    "Azure Functions": ["Azure"],
    "Book Review": ["Book Review"],
    "Cloud Computing": ["Cloud Engineering"],
    "Database": ["Database"],
    "DevOps": ["DevOps"],
    "Docker": ["Docker"],
    "Golang": ["Golang"],
    "Google": ["Google"],
    "Kubernetes": ["Kubernetes"],
    "Productivity": ["Productivity"],
    "Puppet": ["Puppet"],
    "Software Development": ["Software Development"],
    "System Administration": ["System Administration"],
    "Terraform": ["Terraform"]
}

CONSOLIDATED_CATEGORIES = {
    "Administration": [
        ".NET", "System Administration", "Server Management", "Server Migration", "vCenter", "vSphere"
    ],
    "Advice": [
        "Life Hacks", "Time Management", "Troubleshooting"
    ],
    "Algorithm": [
        "Development"
    ],
    "Blogging": [
        "Blog Recommendation", "Conference Coverage", "Conference Reflections"
    ],
    "Business Strategy": [
        "Consulting"
    ],
    "Cloud Computing": [
        "Cloud Engineering", "Infrastructure Modernization", "Serverless Computing", "Software as a Service"
    ],
    "Coding": [
        "Development", "Go Programming", "Ruby Programming"
    ],
    "Command Line": [
        "Linux", "macOS", "Networking"
    ],
    "Conferences": [
        "Conference Coverage", "Conference Reflections"
    ],
    "Container Orchestration": [
        "Containerization", "Kubernetes"
    ],
    "Cybersecurity": [
        "Network Architecture", "Networking"
    ],
    "Database": [
        "Databases", "Development"
    ],
    "DevOps": [
        "Development"
    ],
    "Distributed System": [
        "Distributed Systems"
    ],
    "Docker": [
        "Containerization", "Development"
    ],
    "Events": [
        "Conference Coverage", "Conference Reflections"
    ],
    "Go Programming": [
        "Development"
    ],
    "Infrastructure Modernization": [
        "Cloud Engineering", "Cloud Computing"
    ],
    "IT Solutions": [
        "Consulting", "Development"
    ],
    "Kubernetes": [
        "Containerization", "Container Orchestration"
    ],
    "Life": [
        "Life Hacks"
    ],
    "Life Hacks": [
        "Advice"
    ],
    "Linux": [
        "Command Line", "Networking"
    ],
    "macOS": [
        "Command Line", "Networking"
    ],
    "Network Architecture": [
        "Cybersecurity", "Networking"
    ],
    "Networking": [
        "Command Line", "Cybersecurity", "macOS", "Linux"
    ],
    "Open Source": [
        "Development"
    ],
    "Operating Systems": [
        "Development"
    ],
    "Personal Development": [
        "Advice"
    ],
    "Productivity": [
        "Time Management"
    ],
    "Professional Development": [
        "Development"
    ],
    "Programming": [
        "Development"
    ],
    "Ruby Programming": [
        "Development", "Coding"
    ],
    "Programming": [
        "Development"
    ],
    "Security": [
        "Cybersecurity"
    ],
    "Server Management": [
        "Administration"
    ],
    "Server Migration": [
        "Administration"
    ],
    "Serverless Computing": [
        "Cloud Computing"
    ],
    "Servers": [
        "Administration"
    ],
    "Software as a Service": [
        "Cloud Computing"
    ],
    "Software Development": [
        "Development"
    ],
    "SSL Certificates": [
        "Security"
    ],
    "System Administration": [
        "Administration"
    ],
    "Teamwork": [
        "Development"
    ],
    "Technology": [
        "Development"
    ],
    "Technology Trends": [
        "Development"
    ],
    "Time Management": [
        "Advice"
    ],
    "Troubleshooting": [
        "Advice"
    ],
    "vCenter": [
        "Administration"
    ],
    "vSphere": [
        "Administration"
    ],
    "Web Client": [
        "Development"
    ],
    "Web Development": [
        "Development"
    ],
    "Work Management": [
        "Development"
    ],
    "Workstation": [
        "Development"
    ]
}

def replace_tags_in_file(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        tags = set()
        categories = set()

        for line in lines:
            tags_match = TAGS_REGEX.match(line)
            categories_match = CATEGORIES_REGEX.match(line)

            if tags_match:
                tags_str = tags_match.group(1)
                tags_list = eval("[" + tags_str + "]")  # Convert the string to a list
                tags.update(tags_list)

            if categories_match:
                categories_str = categories_match.group(1)
                categories_list = eval("[" + categories_str + "]")  # Convert the string to a list
                categories.update(categories_list)

            file.write(line)

        # Append the consolidated categories to the tags
        tags.update(CONSOLIDATED_CATEGORIES)
        file.write(f"\ntags = {list(tags)}\n")
        file.write(f"categories = {list(categories)}\n")


def main():
    # Replace tags in all markdown files in the 'posts' directory
    for filename in os.listdir("posts"):
        if filename.endswith(".md"):
            file_path = os.path.join("posts", filename)
            replace_tags_in_file(file_path)


if __name__ == "__main__":
    main()
