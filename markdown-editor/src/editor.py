# write your code here

class MarkdownEditor:
    def __init__(self):
        self.markdown_text = []
        self.possible_formats = {'plain': self.plain,
                                 'bold': self.bold,
                                 'italic': self.italic,
                                 'header': self.header,
                                 'link': self.link,
                                 'ordered-list': self.order_unorder_list,
                                 'unordered-list': self.order_unorder_list,
                                 'inline-code': self.inline_code,
                                 'new-line': self.new_line
                                 }

    def new_line(self):
        self.markdown_text.append('\n')

    def plain(self, text):
        self.markdown_text.append(text)

    def bold(self, text):
        bold_text = f'**{text}**'
        self.markdown_text.append(bold_text)

    def italic(self, text):
        italic_text = f'*{text}*'
        self.markdown_text.append(italic_text)

    def inline_code(self, text):
        inline_code = f'`{text}`'
        self.markdown_text.append(inline_code)

    def header(self, level, text):
        header_text = f'{"#" * level} {text}\n'
        self.markdown_text.append(header_text)

    def link(self, label, url):
        link = f'[{label}]({url})'
        self.markdown_text.append(link)

    def order_unorder_list(self, list_type, number_rows):
        row = 1
        while row <= number_rows:
            text = input(f'Row #{row}:')
            if list_type == 'ordered-list':
                self.markdown_text.append(f'{row}. {text}\n')
            else:
                self.markdown_text.append(f'* {text}\n')
            row += 1


    def done(self, output_file='output.md'):
        with open(output_file, 'w') as md_file:
            md_file.write(''.join(self.markdown_text))

    def editor(self):
        while True:
            response = input('Choose a formatter:')
            if response == '!help':
                print(f'Available formatters: {" ".join(self.possible_formats.keys())}')
                print('Special commands: !help !done')
            elif response == '!done':
                self.done()
                break
            elif response in self.possible_formats:
                if response == 'header':
                    while True:
                        level = int(input('Level:'))
                        if level >= 1 and level <= 6:
                            text = input('Text')
                            break
                        else:
                            print('The level should be within the range of 1 to 6')
                    self.header(level, text)
                elif response in ('ordered-list', 'unordered-list'):
                    while True:
                        number_rows = int(input('Number of rows:'))
                        if number_rows <= 0:
                            print('The number of rows should be greater than zero')
                        else:
                            break
                    self.order_unorder_list(response, number_rows)
                elif response == 'new-line':
                    self.new_line()
                elif response == 'link':
                    label = input('Label:')
                    url = input('URL:')
                    self.link(label, url)
                else:
                    text = input('Text:')
                    self.possible_formats[response](text)

                print(''.join(self.markdown_text))
            else:
                print('Unknown formatting type or command')
md = MarkdownEditor()
md.editor()