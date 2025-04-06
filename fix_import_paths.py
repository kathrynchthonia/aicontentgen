import os
import re

ROOT_DIR = "backend/app"

# Patterns to match import paths starting with "app.app"
patterns = [
    (re.compile(r"\bfrom\s+app\.app(\.[\w\.]*)?\b"), r"from app\1"),
    (re.compile(r"\bimport\s+app\.app(\.[\w\.]*)?\b"), r"import app\1"),
]

def fix_imports():
    for subdir, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                for pattern, replacement in patterns:
                    new_content = pattern.sub(replacement, new_content)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Fixed imports in {file_path}")

if __name__ == "__main__":
    fix_imports()
