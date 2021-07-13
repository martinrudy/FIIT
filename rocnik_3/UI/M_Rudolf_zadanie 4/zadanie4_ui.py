import matplotlib.pyplot as plt
import random
import math

MAX_ITERATION = 10
POINTS_NUMBER = 40000


class Centroid:
    distance = 1
    def __init__(self, x, y, labels):
        self.x = x
        self.y = y
        self.labels = labels

class Medoid:
    distance = 1
    def __init__(self, x, y, labels):
        self.x = x
        self.y = y
        self.labels = labels

def create_points():
    points = []
    while (len(points) < 20):
        x =  random.randint(-5000, 5000), random.randint(-5000, 5000)
        if(x in points):
            continue
        else:
            points.append(x)
    for _ in range (POINTS_NUMBER):
        offset_x =  random.randint(-100, 100)
        offset_y = random.randint(-100, 100)
        random_old = random.choice(points)
        x =  random_old[0] + offset_x
        y = random_old[1] + offset_y
        random_new = x, y
        points.append(random_new)
    return points


def stop_means(centroids):
    for centroid in centroids:
        if(centroid.distance == 1):
            return False

    return True


def getLabel(points, centroids):
    for point in points:
        distance = 0
        min_distance = 200000000
        min_centroid = None
        for centroid in centroids:
            a = point[0] - centroid.x
            b = point[1] - centroid.y
            distance = math.sqrt(a**2 + b**2)
            if(distance < min_distance):
                min_distance = distance 
                min_centroid = centroid
        if(min_distance > 500):
            min_centroid.distance = 1
        else:
            min_centroid.distance = 0
        min_centroid.labels.append(point)


def getCentroids(centroids):
    actualized = []
    sum = 0
    x = 0
    y = 0
    for centroid in centroids:
        sum = 0
        x = 0
        y = 0
        for point in centroid.labels:
            x += point[0]
            y += point[1]
            sum +=1
        if (sum == 0):
            return False
        else:
            actualized.append(Centroid(round(x / sum), round(y / sum), []))
    return actualized

def randomCentroids(points, k):
    centroids = []
    for _ in range(k):
        x, y = random.randint(-5000, 5000), random.randint(-5000, 5000)
        centroid = Centroid(x, y, [])
        centroids.append(centroid)
    return centroids

def clearLabels(centroids):
    for centroid in centroids:
        centroid.labels.clear()
def isEqual(old_centroids, centroids):
    old_x = []
    new_x = []
    old_y = []
    new_y = []
    for centroid in centroids:
        new_x.append(centroid.x)
        new_y.append(centroid.y)
    for old_centroid in old_centroids:
        old_x.append(old_centroid.x)
        old_y.append(old_centroid.y)
    if(old_x == new_x and old_y == new_y):
        return True
    else:
        return False


def k_means_centroid(points, k):
    centroids = randomCentroids(points, k)
    old_centroids = centroids

    while not stop_means(old_centroids):
        old_centroids = centroids
        getLabel(points, centroids)
        centroids = getCentroids(centroids)
        if(centroids == False):
            centroids = randomCentroids(points, k)
            continue
        if(isEqual(old_centroids, centroids)):
            break
    getLabel(points, centroids)
    return centroids


def getMedoidCost(medoids):
    cost = 0
    cost_sum = 0
    for medoid in medoids:
        cost = 0
        for point in medoid.labels:
            a = point[0] - medoid.x
            b = point[1] - medoid.y
            distance = math.sqrt(a**2 + b**2)
            cost += distance
        cost_sum += cost
    return cost_sum




def random_medoids(points, k):
    medoids = []
    iterator = 0
    while(iterator != k):
        pot_medoid = random.choice(points)
        if pot_medoid in medoids:
            continue
        else:
            medoids.append(Medoid(pot_medoid[0], pot_medoid[1], []))
            iterator += 1
    return medoids

def newMedoid(medoids, points):
    k = len(medoids)
    new_medoids = []
    while (len(new_medoids) != k):
        for medoid in medoids:
            new_medoids.append(Medoid(medoid.x, medoid.y, []))

    new_medoids.pop(random.randrange(len(medoids)))
    while (len(new_medoids) != k):
        pot_medoid = random.choice(points)
        if pot_medoid in new_medoids:
            continue
        else:
            new_medoids.append(Medoid(pot_medoid[0], pot_medoid[1], []))
    return new_medoids


def k_means_medoid(points, k):
    medoids = random_medoids(points, k)
    old_medoids = medoids
    old_cost = 0
    new_cost = 0
    same = 0


    while not stop_means(old_medoids):
        old_medoids = medoids
        getLabel(points, medoids)
        old_cost = getMedoidCost(medoids)
        medoids = newMedoid(medoids, points)
        getLabel(points, medoids)
        new_cost = getMedoidCost(medoids)
        if (old_cost - new_cost < 0):
            medoids = old_medoids
        if(isEqual(old_medoids, medoids)):
            same += 1
        else:
            same = 0
        if(same == 3):
            break
    return medoids

def isLabel(pairs, point, min_point):
    if(len(pairs) > 0):
        for pair in pairs:
            if (min_point in pair.labels):
                pair.labels.append(point)
                return True
            elif(point in pair.labels):
                pair.labels.append(min_point)
                return True
    return False

def find_closest(points):
    min_distance = 200000
    distance = 0
    array = points.copy()
    pairs = []
    labels = []
    for point in points:
        actual = array.pop(0)
        labels = []
        for pair in array:
            a = point[0] - pair[0]
            b = point[1] - pair[1]
            distance = math.sqrt(a**2 + b**2)
            if(distance < min_distance):
                min_distance = distance
                min_point = pair
        array.append(actual)
        if(isLabel(pairs, point, min_point)):
            continue
        else:
            labels.append(point)
            labels.append(min_point)
            pairs.append(Centroid(point[0], point[1], labels))
    return pairs
    

def agglomerative(points):
    clusters = find_closest(points)

    
    return clusters




def divisive(dataset, k):
    points = dataset.copy()
    clusters = k_means_centroid(points, 1)
    new_clusters = []
    while(1):
        for cluster in clusters:
            if(len(new_clusters) > 0):
                new_clusters.pop(0)
            pot_clusters = k_means_centroid(cluster.labels, 2)
            for pot_cluster in pot_clusters:
                new_clusters.append(pot_cluster)
            if(len(new_clusters) == k):
                break
        clusters = new_clusters.copy()
        if(len(clusters) == k):
            break
    return clusters










def print_k_means_centroid(k):
    points  = create_points()
    centroids = k_means_centroid(points, k)
    centroid_x = []
    centroid_y = []
    for centroid in centroids:
        point_x = []
        point_y = []
        centroid_x.append(centroid.x)
        centroid_y.append(centroid.y)
        for point in centroid.labels:
            a = point[0]
            b = point[1]
            point_x.append(a)
            point_y.append(b)
        plt.scatter(point_x, point_y)
    plt.scatter(centroid_x, centroid_y, marker='x', s=100, color='red')
    plt.show()

def print_k_means_medoid(k):
    points  = create_points()
    centroids = k_means_medoid(points, k)
    centroid_x = []
    centroid_y = []
    for centroid in centroids:
        point_x = []
        point_y = []
        centroid_x.append(centroid.x)
        centroid_y.append(centroid.y)
        for point in centroid.labels:
            a = point[0]
            b = point[1]
            point_x.append(a)
            point_y.append(b)
        plt.scatter(point_x, point_y)
    plt.scatter(centroid_x, centroid_y, marker='x', s=100, color='red')
    plt.show()

def print_divisive(k):
    points  = create_points()
    centroids = divisive(points, k)
    for centroid in centroids:
        point_x = []
        point_y = []
        for point in centroid.labels:
            a = point[0]
            b = point[1]
            point_x.append(a)
            point_y.append(b)
        plt.scatter(point_x, point_y)
    plt.show()

def print_agglomerative():
    points  = create_points()
    centroids = agglomerative(points)
    for centroid in centroids:
        point_x = []
        point_y = []
        for point in centroid.labels:
            a = point[0]
            b = point[1]
            point_x.append(a)
            point_y.append(b)
        plt.scatter(point_x, point_y)
    plt.show()

print_k_means_centroid(10)
#print_k_means_medoid(10)
#print_divisive(3)
#print_agglomerative()

