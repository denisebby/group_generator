import random
from itertools import combinations
from collections import OrderedDict, defaultdict


def convert_from_str_to_fz(s):
    res = s.split("; ")[:-1]
    res2 = []
    for elem in res:
        res2.append(frozenset(elem.split(",")))
    return frozenset(res2)



def get_random_seeds(n, max_val, seed):
    random.seed(seed)
    return random.sample(range(max_val), n)
    
def get_pairs_so_far(val):
    
    pairs_so_far = defaultdict(int)
    

    for elem in list(val):
        for pair in combinations(elem, 2):
            pairs_so_far[frozenset(pair)] += 1
                
        
    return pairs_so_far

def assign_score(candidate, pairs_so_far):
    score = 0
    for elem in list(candidate):
        for pair in combinations(elem, 2):
            score += pairs_so_far[frozenset(pair)] 
    return score
    
def choose_group_splits(num_people):
    if num_people%4 == 0:
        return {"four": num_people//4, "three": 0}
    elif num_people%3 == 0:
        return {"four": 0, "three": num_people//3}
    else:
        split_strategy = {"four": 0, "three": 0}
        while num_people %3  != 0:
            num_people -= 4
            split_strategy["four"] += 1
        
        while num_people != 0:
            num_people -= 3
            split_strategy["three"] += 1
        
        return split_strategy
        
def generate_random_groups(people, pairs_so_far, n, seeds):
    num_people = len(people)
    split_strategy = choose_group_splits(num_people)
    
    sample_score_dict = dict()
    repeat_samples_dict = defaultdict(int)
    for i in range(n):
        random.seed(seeds[i])
        candidate_order = random.sample(people, num_people)
        
        g4 = candidate_order[0:split_strategy["four"]*4] 
        
        g4_2d = []
        i= 0
        while i < len(g4):
            g4_2d.append(frozenset(g4[i: i+4]))
            i+=4
        if split_strategy["three"] != 0:
            # get remaining part of list
            g3 = candidate_order[split_strategy["four"]*4:] 
            g3_2d = []
            i = 0
            while i < len(g3):
                g3_2d.append(frozenset(g3[i: i+3]))
                i+=3
        
        candidate = frozenset(g4_2d + g3_2d)
        sample_score_dict[candidate] = assign_score(candidate, pairs_so_far)
        repeat_samples_dict[candidate] += 1

    return sample_score_dict, repeat_samples_dict

def choose_best_sampled_group(sample_score_dict):
    min_score = min(sample_score_dict.values())
    for k, v in sample_score_dict.items():
        if v == min_score:
            return k


def main(seed):
    people = ["Bud", "Carly", "Cody", "Denis", "Eunice", "Jie", "Jonathan", "Kirtiraj", "Kyle B.", "Kyle C.", "Mohar", "Piyush", "Stan"]
    history = "Mohar,Jie,Cody,Denis; Bud,Stan,Jonathan; Carly,Kyle B.; Carly,Kyle C.; Stan,Eunice,Piyush;"
    s = convert_from_str_to_fz(history)

    pairs_so_far = get_pairs_so_far(s)

    num_samples = 1000
    seeds = get_random_seeds(n = num_samples, max_val = 10000, seed = seed)
    scores_dict, freq = generate_random_groups(people = people, pairs_so_far = pairs_so_far, n = num_samples, seeds = seeds)
    final_group = choose_best_sampled_group(sample_score_dict = scores_dict)

    return final_group




if __name__ == "__main__":
    main()

