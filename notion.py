import requests

# Replace this with the correct page ID and token
page_id = "3b60d162-471f-4ff8-8c1e-388ea3fc555a"
url = f"https://api.notion.com/v1/blocks/{page_id}/children"
headers = {
    "Authorization": "Bearer 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",
    "Notion-Version": "2022-06-28"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  # JSON data from Notion API
    content = []

    # Parse each block and organize based on type
    for block in data.get("results", []):
        block_type = block["type"]

        # Helper function to get text content if rich_text is not empty
        def get_text(block_content):
            return block_content["rich_text"][0]["text"]["content"] if block_content["rich_text"] else ""

        if block_type in ["heading_1", "heading_2", "heading_3"]:
            # Extract text from headings if available
            heading_text = get_text(block[block_type])
            heading_level = int(block_type[-1])  # Extract the level from the type (e.g., "heading_2" -> 2)
            if heading_text:
                content.append(f"{'#' * heading_level} {heading_text}")

        elif block_type == "to_do":
            # Handle to-do items (tasks) if available
            todo_text = get_text(block["to_do"])
            checked = block["to_do"]["checked"]
            status = "[x]" if checked else "[ ]"
            if todo_text:
                content.append(f"- {status} {todo_text}")

        elif block_type == "paragraph":
            # Handle paragraph text if available
            paragraph_text = get_text(block["paragraph"])
            if paragraph_text:
                content.append(paragraph_text)

        elif block_type == "bulleted_list_item":
            # Handle bullet list items if available
            bullet_text = get_text(block["bulleted_list_item"])
            if bullet_text:
                content.append(f"- {bullet_text}")

    # Print organized content
    print("\n".join(content))

else:
    print(f"Error: {response.status_code}")
    print(response.text)
