from gigachat import GigaChat


class GigaModel:
    def __init__(self):
        self.giga = GigaChat(
        credentials="YTViNDBiOGUtNzE2MS00MmQ1LWE5NmYtZjEzOWYwZjQzZjAxOmU3MTQzOGYxLTc4ZWMtNDFkZS05MzkzLWIxNDQ4NThmMThkOQ==",
        ca_bundle_file="models/russian_trusted_root_ca_pem.crt",
        model='Gigachat-2-Max',
        scope='GIGACHAT_API_B2B')
    

    def question(self, question, text):
        response = self.giga.chat(f"Тебе дан текст: {text}. Ответь на вопрос: {question}. Не более 300 слов")
        res = response.choices[0].message.content
        return res


    def get_topic(self, text):
        response = self.giga.chat(f"Тебе дан текст: {text}. Твоя задача - написать только одно предложение, которое будет являться темой этого текста. Не нужно ничего кроме этой темы.")
        res = response.choices[0].message.content
        return res

if __name__ == '__main__':
    giga = GigaModel()
    print(giga.question("Что такое нейронные сети?", "Нейронные сети - это..."))