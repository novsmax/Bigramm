from graphviz import Digraph
from aot_6_loader import load_pos_tags_from_json, save_to_json


def find_probabilities(pos_tags):
    find_probability_of_beginning(pos_tags)
    find_probability_of_ending(pos_tags)

def find_probability_of_beginning(pos_tags):
    total_starts = 0
    pos_start_counts = {pos: 0 for pos in pos_translation.keys()}

    for tag in pos_tags.values():
        if tag['word_index'] == 0:
            total_starts += tag['count']
            pos = tag['pos']
            pos_start_counts[pos] += tag['count']
    print(total_starts)

    start_probabilities = {pos_translation.get(pos): round(count / total_starts, 5) for pos, count in pos_start_counts.items() if total_starts > 0}
    print(start_probabilities)
    return start_probabilities


def find_probability_of_ending(pos_tags):
    total_ends = 0
    pos_end_counts = {pos: 0 for pos in pos_translation.keys()}

    for tag in pos_tags.values():
        if tag['next_word_index'] == -1:
            total_ends += tag['count']
            pos = tag['pos']
            pos_end_counts[pos] += tag['count']
    print(total_ends)

    end_probabilities = {pos_translation.get(pos): round(count / total_ends, 5) for pos, count in pos_end_counts.items() if total_ends > 0}
    print(end_probabilities)
    return end_probabilities


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

    all_pos = set([tag['next_pos'] for tag in pos_tags.values()])
    all_index = set([tag['word_index'] for tag in pos_tags.values()])

    pos_connections = {pos: {next_pos: {index: 0 for index in all_index} for next_pos in all_pos} for pos in all_pos}
    for tag in pos_tags.values():
        pos = tag['pos']
        next_pos = tag['next_pos']
        index = tag['word_index']
        pos_connections[pos][next_pos][index] += tag['count']

    index_stats = {index: 0 for index in all_index}
    for tag in pos_tags.values():
        index = tag['word_index']
        index_stats[index] += tag['count']

    pos_probability = {pos:
                           {next_pos:
                                {index_stat:
                                     round(pos_connections[pos][next_pos][index_stat] / index_stats[index_stat], 5) if index_stats[index_stat] > 0 else 0
                                 for index_stat in index_stats}
                            for next_pos in all_pos}
                       for pos in all_pos}

    save_to_json(pos_connections, "pos_connections.json")
    save_to_json(pos_probability, "pos_probability.json")
    # print(pos_probability)
    # print(pos_connections)
    # print(index_stats)
    # print(all_index)
    # print(all_pos)



    dot = Digraph(comment='Граф переходов по частям речи', format='png')
    dot.node("Начало", label="Начало", shape="ellipse", style="filled", fillcolor="lightblue")
    dot.node("Конец", label="Конец", shape="ellipse", style="filled", fillcolor="lightblue")
    for pos in all_pos:
        dot.node(pos_translation.get(pos), pos_translation.get(pos))

    dot.render('pos_connections', view=True)