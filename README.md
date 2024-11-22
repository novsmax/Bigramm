# **Анализ текстов и граф частей речи**

## **Описание**
Данная программа выполняет анализ текстов и визуализацию переходов между частями речи. Основные функции программы включают:

---

## **Функциональность**

1. **Загрузка текстов**:
   - Автоматически загружает тексты с ресурса [GitHub](https://github.com/nevmenandr/word2vec-russian-novels/tree/master/books_before).

2. **Морфологический анализ**:
   - Для каждого слова определяется его часть речи с использованием русскоязычной морфологии.
   - Части речи выводятся в формате на русском языке.

3. **Построение графа**:
   - Создаётся ориентированный граф, где:
     - **Вершины** графа — это части речи, а также специальные метки: **Начало предложения** и **Конец предложения**.
     - **Рёбра** графа соответствуют переходам между словами в предложении.

4. **Расчёт вероятностей переходов**:
   - Для каждой дуги графа вычисляется вероятность перехода от одной части речи к другой.
   - Вероятности округляются до **5 знаков после запятой**.

5. **Визуализация графа**:
   - Граф визуализируется с указанием частей речи (на русском языке) и вероятностей переходов.
   - Сохраняется в формате `.png` для удобного просмотра.

6. **Анализ графа**:
   - Выводятся **все пары для числительного**, включая каждую часть речи, с указанием вероятности перехода.
   - Определяются **топ-5 пар частей речи** с максимальными вероятностями переходов.
   - Выводятся **пары частей речи, для которых отсутствуют переходы**.
   - Находится третья по популярности часть речи, с которой чаще всего начинаются предложения, с указанием её вероятности.

---

## **Технологии и библиотеки**

- **Python**: Язык программирования.
- **pymorphy3**: Для морфологического анализа русского текста.
- **nltk**: Для токенизации предложений и слов.
- **graphviz**: Для визуализации графа переходов между частями речи.

---

## **Вывод данных**

1. **Граф переходов**:
   - Граф сохраняется как изображение в формате `.png`.

2. **Статистика**:
   - Все рассчитанные вероятности, переходы и анализы сохраняются в JSON-файлы и выводятся в консоль.

---

## **Как использовать**

1. Убедитесь, что у вас установлен Python версии 3.8 или выше.
2. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
3. Запустите программу
   ```bash
   python main.py
4. После выполения:
    - Граф будет сохранён как файл pos_graph.png.
    - Статистика будет доступна в консоли и соответствующих JSON-файлах.

   
