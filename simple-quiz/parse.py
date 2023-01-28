from enum import Enum


class ParserState(Enum):
    DEFAULT = 0
    IN_QUESTION = 1


def parse(file_path: str) -> None:
    with open(file_path) as file:
        lines = file.read().splitlines()

        lines = [line.strip() for line in lines]

    _parse_inner(lines)


def _parse_inner(lines: list[str]) -> None:
    state = ParserState.DEFAULT

    all_questions_answers = []

    current_heading = []
    current_question = ""
    current_answer = []

    for line in lines:
        # print(f'[{line}]')

        if is_heading(line):
            current_heading = get_heading(line)

            print(f'New heading: {current_heading}')

        elif is_empty(line):
            if state != ParserState.DEFAULT:
                question_answer = {
                    'question': current_question,
                    'answer': current_answer
                }

                all_questions_answers.append(question_answer)

                print(f'Logged question & answer:' +
                    f'\nQuestion: {question_answer["question"]}'
                    f'\nAnswer:   {question_answer["answer"]}')

                state = ParserState.DEFAULT

                current_question = ""
                current_answer = []

            continue

        elif state == ParserState.DEFAULT:
            current_question = line

            current_answer = []

            state = ParserState.IN_QUESTION

        elif state == ParserState.IN_QUESTION:
            current_answer.append(line)


def is_heading(line: str) -> bool:
    return line.startswith('#')


def get_heading(line: str) -> str:
    return line.replace('#', '').strip()


def is_empty(line: str) -> bool:
    return line.strip() == ""
