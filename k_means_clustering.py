import sys
import copy
import random

def read_file(filename):
    in_file = open(filename)
    elements = []
    first = True
    for line in in_file:
        if first:
            first = False
            continue
        line = line.strip()
        numbers = line.split("\t")
        for index, each_number in enumerate(numbers):
            if each_number == "-NA" or each_number == "NA":
                each_number = 0
            try:
                if not each_number:
                    each_number = 0
                numbers[index] = float(each_number)
            except:
                import pdb; pdb.set_trace()
        elements.append(numbers)
    in_file.close()
    return elements

def clustering(elements, k):
    k_clusters = {}
    k_means = {}
    to_be_picked = copy.copy(elements)
    for ii in range(0, k):
        chosen_element = random.choice(to_be_picked)
        to_be_picked.remove(chosen_element)
        index = elements.index(chosen_element)
        k_clusters.setdefault(index, [])
        k_means.setdefault(index, chosen_element)

    #Iterate
    for index, each_element in enumerate(elements):
        if index in k_clusters:
            continue
        smallest_distance, smallest_index = 100000000, -1
        for mean_index, each_mean in k_means.iteritems():
            distance = calculate_distance(each_element, each_mean)
            if distance < smallest_distance:
                smallest_distance = distance
                smallest_index = mean_index
        k_clusters[smallest_index].append(index)
        k_means[smallest_index] = calculate_mean(smallest_index, elements, k_clusters)
    print_list = []
    flag = True
    for each_index, cluster in k_clusters.iteritems():
        print_list.append("%s %s %s" % (each_index, len(cluster), k_clusters.keys()))
        flag = flag and len(cluster) > 40
    if flag:
        for each_print in print_list:
            print each_print
        print

def calculate_distance(a, b):
    sum_diff = 0
    for index, each_number in enumerate(a):
        sum_diff = sum_diff + (each_number - b[index])**2
    return sum_diff

def calculate_mean(index, elements, k_clusters):
    parent = elements[index]
    mean = copy.copy(parent)
    children = k_clusters[index]
    if not children:
        return mean
    for each_index in children:
        candidate = elements[each_index]
        for each_number_index, each_number in enumerate(mean):
            mean[each_number_index] = mean[each_number_index] + candidate[each_number_index]
    for each_number_index, each_number in enumerate(mean):
        mean[each_number_index] = mean[each_number_index] / len(children)
    return mean

if __name__ == "__main__":
    elements = read_file(sys.argv[1])
    for ii in range(1, 100):
        if not ii % 10:
             print "Processed %s" % ii
        clustering(elements, 4)
