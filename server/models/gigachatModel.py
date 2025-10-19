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
        print(f"Получение вопросов для текста: {text}")
        response = self.giga.chat(
            "Тебе дан текст:\n" +
            f"{text}\n\n" +
            "Составь 10 коротких вопросов по тексту и краткие ответы на них.\n" +
            "Верни строго валидный JSON без какого-либо дополнительного текста, без markdown, без комментариев.\n" +
            'Строгий формат:\n' +
            '{"questions": ["вопрос 1", "вопрос 2", "...", "вопрос 10"], ' +
            '"answers": ["ответ 1", "ответ 2", "...", "ответ 10"]}'
            )
        start_index = response.choices[0].message.content.find('{')
        end_index = response.choices[0].message.content.rfind('}') + 1
        res = response.choices[0].message.content[start_index:end_index]
        print(res)
        return json.loads(res)

if __name__ == '__main__':
    giga = GigaModel()
    print(giga.question("Что такое нейронные сети?", "Нейронные сети - это..."))