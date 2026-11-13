import json
import re
from collections import Counter
from datetime import datetime

# Sector rules and keyword patterns
CATEGORIES = {
    'Бьюти / Салоны красоты': [
        r'\bсалон\b', r'\bкрасот', r'\bbeauty\b', r'\bмоне\b', r'\bmon[eé]\b', r'\bволос', r'\bhair\b',
        r'\bманикюр', r'\bпедикюр', r'\bnail', r'\bноготоч', r'\bногт', r'\bресниц', r'\blash',
        r'\bбров', r'\bbrow', r'\bэпил', r'\bдепил', r'\blaser', r'\bлазер', r'\bперманент',
        r'\bтатуаж', r'\bкосметол', r'\bчистк', r'\bвизаж', r'\bмакияж', r'\bстилист', r'\bколорист',
        r'\bбарбер', r'\bbarber', r'\bпарикмахер', r'\bстрижк', r'\bукладк', r'\bблонд', r'\bботокс',
        r'\bкератин', r'\bнаращиван', r'\bафро', r'\bсоляри', r'\btan\b', r'\bзагар', r'\bspa\b', r'\bспа\b'
    ],
    'Здоровье / Медицина / Массаж': [
        r'\bмассаж', r'\bmassage', r'\bклиник', r'\bclinic\b', r'\bмедицин', r'\bмедцентр', r'\bстоматолог',
        r'\bзуб', r'\bdent', r'\bортопед', r'\bостеопат', r'\bподолог', r'\bpodolog', r'\bпсихолог',
        r'\bпсихотерап', r'\bтерапевт', r'\bневролог', r'\bгинеколог', r'\bанализ', r'\bмрт\b', r'\bузи\b',
        r'\bздоровь', r'\bhealth\b', r'\bправка\b', r'\bкинезио', r'\bреабилитац', r'\bлфк\b', r'\bтрихолог'
    ],
    'Фитнес / Спорт / Йога': [
        r'\bфитнес', r'\bfitness', r'\bспорт', r'\bsport', r'\bйог', r'\byoga', r'\bпилатес', r'\bpilates',
        r'\bрастяжк', r'\bstretching', r'\bстретчинг', r'\bтренер', r'\bтренировк', r'\bgym\b', r'\bзал\b',
        r'\bкроссфит', r'\bcrossfit', r'\bбокс\b', r'\bединоборств', r'\bплавани', r'\bбассейн', r'\bтанц',
        r'\bdance', r'\bтанцы', r'\bхореограф', r'\bбалет', r'\bполдэнс', r'\bбатут', r'\bскалодром'
    ],
    'Автобизнес / Детейлинг / Мойки': [
        r'\bавто\b', r'\bавтомойк', r'\bмойка\b', r'\bмойк', r'\bдетейл', r'\bdetailing', r'\bтонировк',
        r'\bполировк', r'\bшиномонтаж', r'\bавтосервис', r'\bсервис\b', r'\bсто\b', r'\bгараж\b', r'\bкузов',
        r'\bхимчистк[а-я]* авто', r'\bceramic', r'\bпленк', r'\bтритон\b'
    ],
    'Животные / Груминг / Вет': [
        r'\bгрум', r'\bgroom', r'\bвет\b', r'\bветеринар', r'\bзоо', r'\bzoo\b', r'\bсобак', r'\bкошек',
        r'\bхвост', r'\bлап[ки]', r'\bпитом', r'\bсобач'
    ],
    'Образование / Курсы / Дети': [
        r'\bшкол', r'\bschool', r'\bкурс', r'\bобучен', r'\bакадеми', r'\bacademy', r'\bцентр развити',
        r'\bдетск', r'\bдети', r'\bрепетитор', r'\bязык', r'\bанглийск', r'\benglish', r'\bлогопед',
        r'\bвокал', r'\bгитар', r'\bмузык', r'\bрисовани', r'\bарт\b', r'\bart\b', r'\bлепка', r'\bпродленк',
        r'\bсад\b', r'\bсадик', r'\bмастер-класс'
    ],
    'Развлечения / Квесты / VR': [
        r'\bквест', r'\bquest', r'\bvr\b', r'\bвиртуальн', r'\bлазертаг', r'\bпейнтбол', r'\bкартинг',
        r'\bкомпьютерн[а-я]* клуб', r'\bcyber', r'\bкибер', r'\bplaystation', r'\bps[45]', r'\bантикафе',
        r'\bнастол', r'\bпарк развлечен', r'\bлофт\b', r'\bloft\b', r'\bгончарн'
    ],
    'Фото / Видеостудии': [
        r'\bфото', r'\bphoto', r'\bвидео\b', r'\bvideo', r'\bсъемк', r'\bстудия фото', r'\bфотоовал',
        r'\bфотосесси', r'\bлокаци'
    ],
    'Тату / Пирсинг': [
        r'\bтату\b', r'\btattoo', r'\bпирсинг', r'\bpiercing', r'\bбоди-арт'
    ],
    'Бытовые услуги / Аренда': [
        r'\bаренд', r'\bпрокат', r'\bхимчистк', r'\bклининг', r'\bcleaning', r'\bремонт\b', r'\bателье',
        r'\bпошив', r'\bобув'
    ],
    'Рестораны / Бары / Кейтеринг': [
        r'\bресторан', r'\bкафе\b', r'\bбар\b', r'\bкофе', r'\bcoffee', r'\bкофейн', r'\bдоставк[а-я]* ед',
        r'\bбанкет', r'\bкейтеринг', r'\bкальян', r'\blounge', r'\bhookah'
    ]
}

def classify_company(name, text=''):
    combined = f'{name} {text}'.lower()
    
    # Priority checks for specialized niches first
    for cat in ['Животные / Груминг / Вет', 'Автобизнес / Детейлинг / Мойки', 'Тату / Пирсинг', 
                'Развлечения / Квесты / VR', 'Фото / Видеостудии', 'Образование / Курсы / Дети',
                'Фитнес / Спорт / Йога', 'Здоровье / Медицина / Массаж', 'Бытовые услуги / Аренда',
                'Рестораны / Бары / Кейтеринг', 'Бьюти / Салоны красоты']:
        for pattern in CATEGORIES[cat]:
            if re.search(pattern, combined):
                return cat
                
    # Fallback default: since 85%+ of YClients is beauty, check if general salon
    if 'студи' in combined or 'мастер' in combined or 'lab' in combined or 'studio' in combined:
        return 'Бьюти / Салоны красоты'
        
    return 'Другие сферы'

if __name__ == '__main__':
    print('Classifier loaded successfully.')
