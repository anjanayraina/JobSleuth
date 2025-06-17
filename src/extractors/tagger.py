
TECH_STACK = [
    "solidity", "python", "javascript", "typescript", "react", "node", "aws",
    "solana", "blockchain", "docker", "kubernetes", "java", "c++", "postgres",
    "mongodb", "redis", "azure", "gcp", "graphql", "rust", "go"
]

def extract_tags(text):
    tags = []
    text_lower = text.lower()
    for stack in TECH_STACK:
        if stack in text_lower and stack not in tags:
            tags.append(stack)
    return tags
