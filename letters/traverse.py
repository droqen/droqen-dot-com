import os
import re

root = "."  # base directory

# regex to detect the meta tag in the head
meta_re = re.compile(r'<meta\s+name=["\']letter-title["\']\s+content=["\']([^"\']+)["\']', re.IGNORECASE)

results = []   # (filepath, title)

for entry in os.listdir(root):
    if os.path.isdir(os.path.join(root, entry)) and entry.isdigit():
        year_dir = os.path.join(root, entry)

        for folder, _, files in os.walk(year_dir):
            for f in files:
                if not f.lower().endswith(".html"):
                    continue

                rel_path = os.path.relpath(os.path.join(folder, f), root)
                full_path = os.path.join(folder, f)

                title_found = None

                # read only until </head>
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    for line in fp:
                        # stop early when head ends
                        if "</head>" in line.lower():
                            break

                        m = meta_re.search(line)
                        if m:
                            title_found = m.group(1).strip()
                            break

                results.append((rel_path, title_found))

# Print results
for path, title in results:
	print(f"<a href='{path}'>{title}</a>")