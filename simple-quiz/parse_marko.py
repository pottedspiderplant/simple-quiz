"""
Sample usage of the marko package
"""

from marko import Markdown
from marko.block import Document, Heading, Paragraph, BlankLine, List
from marko.inline import RawText


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


def parse(file_path: str) -> list[Question]:
    with open(file_path) as file:
        lines = file.read().splitlines()

        lines = [line.strip() for line in lines]

    lines = "\n".join(lines)

    document = Markdown().parse(lines)

    return disassemble_document(document)


def disassemble_document(document: Document) -> list[Question]:
    all_questions_answers = []

    current_category_text = None
    current_question_text = None
    current_answer_text = None

    # For each of the top-level elements of the parsed document,
    for child in document.children:
        # A heading will be treated as a question category
        if isinstance(child, Heading):
            first_child = child.children[0]

            if isinstance(first_child, RawText):
                heading_text = first_child.children

                print(f'Heading: {heading_text}')

                current_category_text = heading_text

        # A plain paragraph will be treated as a question
        elif isinstance(child, Paragraph):
            first_child = child.children[0]

            question_text = first_child.children

            print(f'Question: {question_text}')

            current_question_text = question_text

        # A list will be treated as the answer to the most recent question
        elif isinstance(child, List):
            # Get the text of the first list item. Assume that the first list item has no
            # formatting and is therefore a plain string. In this assumed situation, Marko
            # represents the list as a List object, containing one or more ListItem objects,
            # containing a Paragraph object, containing a RawText object, containing a string
            answer_text = child.children[0].children[0].children[0].children

            print(f'Answer: {answer_text}')

            current_answer_text = answer_text

            question_answer = Question(current_question_text, current_answer_text)

            all_questions_answers.append(question_answer)

        # Ignore blank lines
        elif isinstance(child, BlankLine):
            continue

        # Anything else is outside the grammar of this app
        else:
            raise ValueError(f'Did not expect a top-level element of type: {type(child)}')

    return all_questions_answers
