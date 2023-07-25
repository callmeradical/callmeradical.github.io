import os
import re

# Map of original tags to new consolidated tags
TAG_MAP = {
    "aws":[
        "Amazon DynamoDB",
        "api gateway",
        "aurora",
        "AWS Lambda",
        "AWS re:Invent",
        "AWS Summit",
        "EC2"
    ],
    "docker": [
        "Docker Hub",
        "Docker Machine",
        "Docker Services",
        "Dockerfile",
        "Dockerfiles",
        "Docker Containers",
        "Docker Networking",
        "Docker Toolkit"
    ],
    "google": [
        "Google Firebase",
        "Google Functions",
        "GCC",
        "GCE"
    ],
    "azure": [
        "Azure CosmosDB",
        "Azure Functions"
    ],
    "Cloud & Serverless Technologies": [
        "Active Directory",
        "Azure",
        "Backend as a Service (BaaS)",
        "esxi",
        "Functions as a Service (FaaS)",
        "serverless",
        "vsphere",
        "zookeeper"
    ],
    "Golang":[
        "Go",
        "Go Plugin"
    ],
    "Programming & Software Development": [
        "Application Deployment",
        "Builder Pattern",
        "coding",
        "Django",
        "development",
        "Java",
        "JavaScript",
        "Node.js",
        "NodeJS",
        "Python",
        "rails",
        "Ruby",
        "Software Deployment",
        "Version Control",
        "Zero Downtime Deploys",
        "puma"
    ],
    "DevOps & Infrastructure Management": [
        "Automation",
        "Chef",
        "ChefSpec",
        "configuration",
        "Consul",
        "Containerization",
        "Containers",
        "HashiCorp",
        "IT Modernization",
        "Registrator",
        "sysadmin",
        "System Administration",
        "replicated state machine"
    ],
    "Networking & Security": [
        "Authentication",
        "Authorization",
        "Infrastructure Security",
        "Kerberos.kdc",
        "Secure Communication",
        "Server Security",
        "SSL Certificate",
        "Networking",
        "Nginx",
        "s3"
    ],
    "Database": [
        "Database Reset",
        "Postgres Database",
        "SQL Server",
        "Oracle"
    ],
    "Operating Systems & Environment Management": [
        "Alpine",
        "Debian",
        "environment variables",
        "Linux",
        "mac",
        "Mac OS X",
        "Mavericks",
        "Mountain Lion",
        "OS X",
        "OS X Lion",
        "OS X Mountain Lion",
        "Red Hat",
        "Windows",
        "Windows Server"
    ],
    "Productivity & Time Management": [
        "Essentialism",
        "Lean Manufacturing",
        "Life Hacking",
        "Meeting Efficiency",
        "Personal Development",
        "Priorities",
        "Process Refinement",
        "Professional Development",
        "Productivity",
        "Time Management",
        "Work Management",
        "Work-life Balance"
    ],
    "Miscellaneous": [
        "Abstraction",
        "Apache",
        "Atom",
        "Boxen",
        "Chat Server",
        "Chromebook",
        "CLI",
        "Client Engagement",
        "Cloud",
        "Collaboration",
        "Command Line",
        "Commands",
        "Conferences",
        "Consulting",
        "CPU Management",
        "Customer Focus",
        "Decision Making",
        "demo",
        "Dependencies",
        "distributed system",
        "DSA Key Pair",
        "Dynamic Configuration",
        "Event Participation",
        "File Transmission",
        "Gems",
        "git",
        "Github",
        "Github Pages",
        "Greg McKeown",
        "IaaS",
        "IDE",
        "Information Capture",
        "installation",
        "IRC",
        "IT Doesn't Matter",
        "James Clear",
        "Jekyll",
        "Key Generation",
        "Language",
        "Las Vegas",
        "Launchd",
        "leader election",
        "Learning Resources",
        "Links Sharing",
        "Lion",
        "Live Blogging",
        "Load Balancing",
        "Local Development",
        "LocalKDC",
        "log replication",
        "Lookup Service",
        "Make",
        "Memory Management",
        "microservices",
        "Microsoft",
        "Multi-Stage Builds",
        "Multitasking",
        "National Vulnerability Database",
        "Netcat",
        "Nick Carr",
        "Nitrous.IO",
        "Octopress",
        "Open Directory",
        "Open Source",
        "Optimization",
        "performance testing",
        "Private Key",
        "Public Key",
        "Quality of Service",
        "raft",
        "Reading",
        "Realtime Rails",
        "Remote Access",
        "Resource Management",
        "Resource Utilization",
        "reverse proxy",
        "screen",
        "Server Migration",
        "Service Discovery",
        "shared workstation",
        "SSH",
        "Terminal Commands",
        "Toolchain",
        "tools",
        "Twitter CLI",
        "Verification Failed",
        "vim",
        "Virtual Hosts",
        "Virtual Machine",
        "Virtualization",
        "vmware",
        "Waste Elimination",
        "web server",
        "Werner Vogels",
        "Wiki Service"
    ]
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

