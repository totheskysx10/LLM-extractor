from typing import Dict, List


class TestData:
    def tests_definition(self) -> List[Dict]:
        return [
            {
                "document_type": "Водительские права",
                "field_name": "Имя и отчество",
                "learn_examples": [
                    {
                        "value": "Александр Сергеевич",
                        "ocr_file": "dataset/vu1.png.json",
                    },
                    {
                        "value": "Дмитрий Витальевич",
                        "ocr_file": "dataset/vu2.png.json",
                    },
                ],
                "apply_values": [
                    {
                        "value": "Александр Евгеньевич",
                        "ocr_file": "dataset/vu3.png.json",
                    },
                    {
                        "value": "Алексей Евгеньевич",
                        "ocr_file": "dataset/vu4.png.json",
                    },
                    {
                        "value": "Александр Владимирович",
                        "ocr_file": "dataset/vu5.png.json",
                    },
                    {
                        "value": "Михаил Владимирович",
                        "ocr_file": "dataset/vu6.png.json",
                    },
                    {
                        "value": "Станислав Геннадьевич",
                        "ocr_file": "dataset/vu7.png.json",
                    },
                ],
            },
            {
                "document_type": "Паспорт",
                "field_name": "Фамилия",
                "learn_examples": [
                    {
                        "value": "Лепп",
                        "ocr_file": "dataset/pass1.png.json",
                    },
                    {
                        "value": "Депардьё",
                        "ocr_file": "dataset/pass2.png.json",
                    },
                ],
                "apply_values": [
                    {
                        "value": "Макеев",
                        "ocr_file": "dataset/pass3.png.json",
                    },
                    {
                        "value": "Золотарев",
                        "ocr_file": "dataset/pass4.png.json",
                    },
                    {
                        "value": "Кузеванов",
                        "ocr_file": "dataset/pass5.png.json",
                    },
                    {
                        "value": "Подлужный",
                        "ocr_file": "dataset/pass6.png.json",
                    },
                    {
                        "value": "Шатов",
                        "ocr_file": "dataset/pass7.png.json",
                    },
                ],
            },
            {
                "document_type": "Паспорт",
                "field_name": "Дата выдачи",
                "learn_examples": [
                    {
                        "value": "14.01.2010",
                        "ocr_file": "dataset/pass1.png.json",
                    },
                    {
                        "value": "17.04.2013",
                        "ocr_file": "dataset/pass2.png.json",
                    },
                ],
                "apply_values": [
                    {
                        "value": "23.07.2019",
                        "ocr_file": "dataset/pass3.png.json",
                    },
                    {
                        "value": "19.12.2010",
                        "ocr_file": "dataset/pass4.png.json",
                    },
                    {
                        "value": "18.01.2011",
                        "ocr_file": "dataset/pass5.png.json",
                    },
                    {
                        "value": "06.03.2013",
                        "ocr_file": "dataset/pass6.png.json",
                    },
                    {
                        "value": "01.04.2010",
                        "ocr_file": "dataset/pass7.png.json",
                    },
                ],
            },
            {
                "document_type": "Снилс",
                "field_name": "Номер",
                "learn_examples": [
                    {
                        "value": "001-001-001 00",
                        "ocr_file": "dataset/snils1.png.json",
                    },
                    {
                        "value": "123-456-789 00",
                        "ocr_file": "dataset/snils2.png.json",
                    },
                ],
                "apply_values": [
                    {
                        "value": "126-029-036 24",
                        "ocr_file": "dataset/snils3.png.json",
                    },
                    {
                        "value": "114-341-457 79",
                        "ocr_file": "dataset/snils4.png.json",
                    },
                    {
                        "value": "156-125-394 57",
                        "ocr_file": "dataset/snils5.png.json",
                    },
                    {
                        "value": "123-456-789 10",
                        "ocr_file": "dataset/snils6.png.json",
                    },
                    {
                        "value": "152-080-942 39",
                        "ocr_file": "dataset/snils7.png.json",
                    },
                ],
            },
            {
                "document_type": "Договор купли-продажи авто",
                "field_name": "Марка, модель",
                "learn_examples": [
                    {
                        "value": "Мерседес S600",
                        "ocr_file": "dataset/dkp1.png.json",
                    },
                    {
                        "value": "Porsche Cayenne 957 S",
                        "ocr_file": "dataset/dkp2.png.json",
                    },
                ],
                "apply_values": [
                    {
                        "value": "Subaru Impreza",
                        "ocr_file": "dataset/dkp3.png.json",
                    },
                    {
                        "value": "Toyota Chaser",
                        "ocr_file": "dataset/dkp4.png.json",
                    },
                    {
                        "value": "Фольксваген Поло",
                        "ocr_file": "dataset/dkp5.png.json",
                    },
                    {
                        "value": "BMW X5",
                        "ocr_file": "dataset/dkp6.png.json",
                    },
                    {
                        "value": "Lada Granta",
                        "ocr_file": "dataset/dkp7.png.json",
                    },
                ],
            },
        ]