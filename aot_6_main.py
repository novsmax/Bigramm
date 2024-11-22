from graphviz import Digraph
from aot_6_loader import load_pos_tags_from_json, save_to_json


def find_probability_of_beginning_ending(pos_tags):
    total_starts = 0
    pos_start_counts = {pos: 0 for pos in pos_translation.keys()}

    total_ends = 0
    pos_end_counts = {pos: 0 for pos in pos_translation.keys()}

    for tag in pos_tags.values():

        if tag['word_index'] == 0:
            total_starts += tag['count']
            pos = tag['pos']
            pos_start_counts[pos] += tag['count']
        if tag['next_word_index'] == -1:
            total_ends += tag['count']
            pos = tag['pos']
            pos_end_counts[pos] += tag['count']

    # print(total_starts)

    start_probabilities = {pos_translation.get(pos): round(count / total_starts, 5) for pos, count in pos_start_counts.items() if total_starts > 0}
    end_probabilities = {pos_translation.get(pos): round(count / total_ends, 5) for pos, count in pos_end_counts.items()
                         if total_ends > 0}

    # print(start_probabilities)
    return start_probabilities, end_probabilities


def make_graph(pos_probs_without_indexes, begin_probs, end_probs):
    dot = Digraph(comment='Граф переходов по частям речи', format='png')
    dot.node("Начало", label="Начало", shape="ellipse", style="filled", fillcolor="lightblue")
    dot.node("Конец", label="Конец", shape="ellipse", style="filled", fillcolor="lightblue")

    for pos in begin_probs:
        if pos == "конец предложения":
            continue
        dot.edge("Начало", pos, label=str(begin_probs[pos]), len="4.0")
        dot.edge(pos, "Конец", label=str(end_probs[pos]), len="2.0")
    for pos in pos_probs_without_indexes:
        if pos == "END":
            continue
        for next_pos in pos_probs_without_indexes[pos]:
            if next_pos == "END":
                continue
            dot.edge(pos_translation.get(pos), pos_translation.get(next_pos),
                     label=str(pos_probs_without_indexes[pos][next_pos]), len="2.0")

    dot.render('pos_connections', view=True)


def find_connections_and_probs(pos_tags):
    all_pos = set([tag['next_pos'] for tag in pos_tags.values()])
    all_index = set([tag['word_index'] for tag in pos_tags.values()])
    count_of_bigrams = sum([tag['count'] for tag in pos_tags.values()])
    #print(count_of_bigrams)

    pos_connections = {pos:
                           {next_pos:
                                {index:
                                     0
                                 for index in all_index}
                            for next_pos in all_pos}
                       for pos in all_pos}

    for tag in pos_tags.values():
        pos = tag['pos']
        next_pos = tag['next_pos']
        index = tag['word_index']
        pos_connections[pos][next_pos][index] += tag['count']

    pos_probs_without_indexes = {pos:
                                     {next_pos:
                                          round(sum([pos_connections[pos][next_pos][index] for index in
                                                     range(230)]) / count_of_bigrams, 5)
                                      for next_pos in all_pos}
                                 for pos in all_pos}

    save_to_json(pos_probs_without_indexes, "pos_probs_without_indexes.json")
    save_to_json(pos_connections, "pos_connections.json")

    return pos_probs_without_indexes
    # index_stats = {index: 0 for index in all_index}
    # for tag in pos_tags.values():
    #     index = tag['word_index']
    #     index_stats[index] += tag['count']
    #
    # pos_probability = {pos:
    #                        {next_pos:
    #                             {index_stat:
    #                                  round(pos_connections[pos][next_pos][index_stat] / index_stats[index_stat], 5) if index_stats[index_stat] > 0 else 0
    #                              for index_stat in index_stats}
    #                         for next_pos in all_pos}
    #                    for pos in all_pos}
    # save_to_json(pos_probability, "pos_probability.json")
    # print(pos_probability)
    # print(pos_connections)
    # print(index_stats)
    # print(all_index)
    # print(all_pos)


def answers(pos_probs_without_indexes, begin_probs, pos_translation):

    no_connections = set()
    pairs_with_probabilities = []
    NUMR_pairs = set()

    for pos in pos_probs_without_indexes:
        if pos == 'END':
            continue
        if pos == "NUMR":
            for next_pos in pos_probs_without_indexes[pos]:
                pair = (pos, next_pos, pos_probs_without_indexes[pos][next_pos])
                NUMR_pairs.add(pair)
        for next_pos in pos_probs_without_indexes[pos]:
            prob = pos_probs_without_indexes[pos][next_pos]
            if prob > 0.0:
                pairs_with_probabilities.append((pos, next_pos, prob))
            if pos_probs_without_indexes[pos][next_pos] == 0.0:
                pair = (pos, next_pos)
                if pair not in no_connections:
                    no_connections.add(pair)

    print("\nПары с числительными:")
    for pair in NUMR_pairs:
        print(f"{pos_translation.get(pair[0])} -> {pos_translation.get(pair[1])}. Вероятность: {pair[2]:.5f}")

    top_5_pairs = sorted(pairs_with_probabilities, key=lambda x: x[2], reverse=True)[:5]
    print("\nТоп-5 пар частей речи с максимальными вероятностями:")
    for pos, next_pos, prob in top_5_pairs:
        print(f"{pos_translation.get(pos)} -> {pos_translation.get(next_pos)}: {prob:.5f}")

    print("\nПары без связи:")
    for item in no_connections:
        print(f'Нет связи между {pos_translation.get(item[0])} и {pos_translation.get(item[1])}')

    print("\nТретья по счету часть речи, с которой чаще всего начинается предложение:")
    third_begin_pos, third_begin_prob = sorted(begin_probs.items(), key=lambda x: x[1], reverse=True)[2]
    print(f"{third_begin_pos}, вероятность: {third_begin_prob:.5f}")



if __name__ == "__main__":

    pos_tags = load_pos_tags_from_json("pos_tags.json")
    if pos_tags is None:
        print("POS-теги не найдены. Сначала выполните обработку текстов.")
        exit()

    pos_translation = {
        'NOUN': 'существительное',
        'ADJF': 'прилагательное (полное)',
        'ADJS': 'прилагательное (краткое)',
        'COMP': 'компаратив',
        'VERB': 'глагол (личная форма)',
        'INFN': 'глагол (инфинитив)',
        'PRTF': 'причастие (полное)',
        'PRTS': 'причастие (краткое)',
        'GRND': 'деепричастие',
        'NUMR': 'числительное',
        'ADVB': 'наречие',
        'NPRO': 'местоимение-существительное',
        'PRED': 'предикатив',
        'PREP': 'предлог',
        'CONJ': 'союз',
        'PRCL': 'частица',
        'INTJ': 'междометие',
        'UNKNOWN': 'неизвестно',
        'END': 'конец предложения'
    }


    begin_probs, end_probs = find_probability_of_beginning_ending(pos_tags)
    pos_probs_without_indexes = find_connections_and_probs(pos_tags)
    make_graph(pos_probs_without_indexes, begin_probs, end_probs)
    answers(pos_probs_without_indexes, begin_probs, pos_translation)





