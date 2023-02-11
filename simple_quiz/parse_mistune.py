"""
Sample usage of the mistune package.
"""

import mistune


def parse(file_path: str) -> None:
    with open(file_path) as file:
        lines = file.read().splitlines()

        lines = [line.strip() for line in lines]

    lines = "\n".join(lines)

    # Use Mistune to parse markdown into an abstract syntax tree (AST), instead of HTML
    markdown = mistune.Markdown(renderer=mistune.AstRenderer())
    # (based on mistune code in renderers.py. Attempts to use
    # `mistune.create_markdown(renderer=None)` returns HTML instead of an AST,
    # despite what the docs say: https://mistune.lepture.com/en/latest/guide.html#ast)

    document = markdown(lines)

    disassemble_document(document)


def disassemble_document(document: list) -> None:
    current_category_text = None
    current_question_text = None
    current_answer_text = None

    # For each of the top-level elements of the parsed document,
    for child in document:
        # A heading will be treated as a question category
        if child['type'] == 'heading':
            heading_text = child['children'][0]['text']

            print(f'Heading: {heading_text}')

            current_category_text = heading_text

        # A plain paragraph will be treated as a question
        elif child['type'] == 'paragraph':
            question_text = child['children'][0]['text']

            print(f'Question: {question_text}')

            current_question_text = question_text

        # A list will be treated as the answer to the most recent question
        elif child['type'] == 'list':
            list_item = child['children'][0]

            block_text = list_item['children'][0]

            answer_text = block_text['children'][0]['text']

            print(f'Answer: {answer_text}')

            current_answer_text = answer_text

        # Anything else is outside the grammar of this app
        else:
            raise ValueError(f'Did not expect a top-level element of type: {child["type"]}')
