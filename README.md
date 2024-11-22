Программу которая выполняет следующие действия:

#Загрузка текстов с ресурса https://github.com/nevmenandr/word2vec-russian-novels/tree/master/books_before
#Для каждого слова определяется часть речи (на русском языке)
#Строится граф, в котором в качестве вершин выступают части речи (+ начало предложения + конец предложения), а дуги соответствуют переходам между словами в предложении.
#Для каждой дуги рассчитать вероятность перехода по дуге.
#Визуализировать граф с указанием частей речи (на русском языке) и значений вероятностей с точностью 5-ть знаков после запятой.
#Вывести все пары для числительного (числительное + каждая часть речи) с указанием вероятности перехода.
#Вывести топ-5 пар частей речи с максимальными вероятностями.
#Вывести пары частей речи, для которых отсутствуют переходы.
#Вывести название части речи, которая является третьей по счету частью речи, с которой чаще всего начинается предложение, с указанием вероятности.
