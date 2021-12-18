def read_quiz():
    with open(f'question.txt','r') as file:
        text=file.read()
        yield text

def uploads():
    for text in read_quiz():
        sections_text=text.split('\n')
    for section in sections_text:
        if section.strip().startswith('Вопрос'):
            question=' '.join(section.strip().splitlines()[1:])
            continue
        if section.strip().startswith('Ответ'):
            answer=' '.join(section.strip().splitlines()[1:])


def main():
    uploads()

if __name__=='__main__':
    main()
            
