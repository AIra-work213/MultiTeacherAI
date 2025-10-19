from gigachat import GigaChat
import json

class GigaModel:
    def __init__(self):
        self.giga = GigaChat(
        credentials="YTViNDBiOGUtNzE2MS00MmQ1LWE5NmYtZjEzOWYwZjQzZjAxOmU3MTQzOGYxLTc4ZWMtNDFkZS05MzkzLWIxNDQ4NThmMThkOQ==",
        ca_bundle_file="models/russian_trusted_root_ca_pem.crt",
        model='Gigachat-2-Max',
        scope='GIGACHAT_API_B2B')
    

    def question(self, question, text):
        response = self.giga.chat(f"Тебе дан текст: {text}. Ответь на вопрос: {question}. Отвечай на вопрос только в том случае, если ты уверен что этот вопрос по тому контексту, который тебе предоставили, иначе ответь: Я не могу ответить на текущий вопрос. Не более 300 слов")
        res = response.choices[0].message.content
        return res


    def get_topic(self, text):
        response = self.giga.chat(f"Тебе дан текст: {text}. Твоя задача - написать только одно предложение, которое будет являться темой этого текста. Не нужно ничего кроме этой темы.")
        res = response.choices[0].message.content
        return res
    
    def get_questions(self, text):
        response = self.giga.chat(f"""Тебе дан текст: {text}. Твоя задача - составить 10 вопросов по этому тексту и ответы к ним, пусть на вопросы можно будет ответить 1-2 предложениями и сами вопросы небольшие. Никакого текста кроме вопросов и ответов.
                                  Ответ представь в формате JSON:""" + "\n{questions: [вопрос 1, вопрос 2, вопрос 3, вопрос 4, вопрос 5, вопрос 6, вопрос 7, вопрос 8, вопрос 9, вопрос 10], answers: [ответ 1, ответ 2, ответ 3, ответ 4, ответ 5, ответ 6, ответ 7, ответ 8, ответ 9, ответ 10]}"
                                  )
        start_index = response.choices[0].message.content.find('{')
        end_index = response.choices[0].message.content.rfind('}') + 1
        res = response.choices[0].message.content[start_index:end_index]
        res = json.loads(res)
        return res

if __name__ == '__main__':
    giga = GigaModel()
    print(giga.question("Что такое нейронные сети?", "Нейронные сети - это..."))