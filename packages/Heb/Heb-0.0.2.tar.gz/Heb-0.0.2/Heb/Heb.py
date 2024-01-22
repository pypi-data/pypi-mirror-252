class Heb:
    def p1(self):
        print('''
class McCullochPittsNeuron: 
    def __init__(self, weights, threshold): 
        self.weights = weights 
        self.threshold = threshold 

    def activate(self, inputs): 
        weighted_sum = sum([inputs[i] * self.weights[i] for i in range(len(inputs))]) 
        return 1 if weighted_sum >= self.threshold else 0 

# AND Logic Function 
and_weights = [1, 1] 
and_threshold = 2 
and_neuron = McCullochPittsNeuron(and_weights, and_threshold) 

# OR Logic Function 
or_weights = [1, 1] 
or_threshold = 1 
or_neuron = McCullochPittsNeuron(or_weights, or_threshold) 

# Test AND logic function 
input_values_and = [(0, 0), (0, 1), (1, 0), (1, 1)] 
print("AND Logic Function:") 
for inputs in input_values_and: 
    output = and_neuron.activate(inputs) 
    print(f"Input: {inputs}, Output: {output}") 

# Test OR logic function 
input_values_or = [(0, 0), (0, 1), (1, 0), (1, 1)] 
print("\n OR Logic Function:") 
for inputs in input_values_or: 
    output = or_neuron.activate(inputs) 
    print(f"Input: {inputs}, Output: {output}")
    
        ''')
    def p2(self):
        print('''
class McCullochPittsNeuron:

    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold

    def activate(self, inputs):
        weighted_sum = sum([inputs[i] * self.weights[i] for i in range(len(inputs))])
        return 1 if weighted_sum >= self.threshold else 0

# AND1 Logic Function
and_weights1 = [1, -1]
and_threshold1 = 1
and_neuron1 = McCullochPittsNeuron(and_weights1, and_threshold1)

# AND2 Logic Function
and_weights2 = [-1, 1]
and_threshold2 = 1
and_neuron2 = McCullochPittsNeuron(and_weights2, and_threshold2)

# OR Logic Function
or_weights = [1, 1]
or_threshold = 1
or_neuron = McCullochPittsNeuron(or_weights, or_threshold)

# Test AND1 logic function
input_values_and1 = [(0, 0), (0, 1), (1, 0), (1, 1)]
print("AND Logic Function1:")
for inputs in input_values_and1:
    output = and_neuron1.activate(inputs)
    print(f"Input: {inputs}, Output: {output}")

# Test AND2 logic function
input_values_and2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
print("AND Logic Function2:")
for inputs in input_values_and2:
    output = and_neuron2.activate(inputs)
    print(f"Input: {inputs}, Output: {output}")

# Test OR logic function
input_values_xor = [(0, 0), (0, 1), (1, 0), (0, 0)]
print("\nOR Logic Function:")
for inputs in input_values_xor:
    output = or_neuron.activate(inputs)
    print(f"Input: {inputs}, Output: {output}")
------------------------------------------------------------------
              AND-NOT
class McCullochPittsNeuron: 

    def __init__(self, weights, threshold): 

        self.weights = weights 

        self.threshold = threshold 

 

    def activate(self, inputs): 

        activation = sum([inputs[i] * self.weights[i] for i in range(len(inputs))]) 

        return 1 if activation >= self.threshold else 0 

 

# ANDNOT logic function 

def andnot_logic_gate(inputs): 

    weights = [1, -1] 

    threshold = 1 

    neuron = McCullochPittsNeuron(weights, threshold) 

    return neuron.activate(inputs) 

 

 

# Test ANDNOT logic gate 

print("ANDNOT Logic Gate:") 

print("0 ANDNOT 0 =", andnot_logic_gate([0, 0])) 

print("0 ANDNOT 1 =", andnot_logic_gate([0, 1])) 

print("1 ANDNOT 0 =", andnot_logic_gate([1, 0])) 

print("1 ANDNOT 1 =", andnot_logic_gate([1, 1])) 
---------------------------------------------------
 XOR 
              
class McCullochPittsNeuron: 

    def __init__(self, weights, threshold): 

        self.weights = weights 

        self.threshold = threshold 

 

    def activate(self, inputs): 

        weighted_sum = sum([inputs[i] * self.weights[i]  

        for i in range(len(inputs))]) 

        return 1 if weighted_sum >= self.threshold else 0 

 

# AND1 Logic Function 

and_weights1 = [1, -1] 

and_threshold = 1 

and_neuron1 = McCullochPittsNeuron(and_weights1, and_threshold) 

 

# AND2 Logic Function 

and_weights2 = [-1, 1] 

and_threshold = 1 

and_neuron2 = McCullochPittsNeuron(and_weights2, and_threshold) 

 

# OR Logic Function 

or_weights = [1, 1] 

or_threshold = 1 

or_neuron = McCullochPittsNeuron(or_weights, or_threshold) 

 

# Test AND logic function 

input_values_and1 = [(0, 0), (0, 1), (1, 0), (1, 1)] 

print("AND Logic Function1:") 

for inputs in input_values_and1: 

    output = and_neuron1.activate(inputs) 

    print(f"Input: {inputs}, Output: {output}") 

     

# Test AND logic function 

input_values_and2 = [(0, 0), (0, 1), (1, 0), (1, 1)] 

print("AND Logic Function2:") 

for inputs in input_values_and2: 

    output = and_neuron2.activate(inputs) 

    print(f"Input: {inputs}, Output: {output}") 

     

# Test XOR logic function 

input_values_xor = [(0, 0), (0, 1), (1, 0), (0, 0)] 

print("\nOR Logic Function:") 

for inputs in input_values_xor: 

    output = or_neuron.activate(inputs) 

    print(f"Input: {inputs}, Output: {output}") 
''')
    def p4(self):
        print('''
import numpy as np
import matplotlib.pyplot as plt

class HebbianNetwork:
    def __init__(self, input_size):
        self.weights = np.zeros((input_size, input_size))

    def train(self, input_patterns):
        for pattern in input_patterns:
            self.weights += np.outer(pattern, pattern)

    def classify(self, input_pattern):
        output = np.dot(input_pattern, self.weights)
        return np.sign(output)

def plot_patterns(input_patterns, title):
    for pattern in input_patterns:
        plt.scatter(pattern[0], pattern[1], color='b')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.show()

def main():
    input_size = 2
    hebb_net = HebbianNetwork(input_size)

    # Define input patterns
    pattern1 = np.array([1, 1])
    pattern2 = np.array([1, -1])
    pattern3 = np.array([-1, 1])
    pattern4 = np.array([-1, -1])

    input_patterns = [pattern1, pattern2, pattern3, pattern4]

    # Train the Hebbian network
    hebb_net.train(input_patterns)

    # Classify new patterns
    test_pattern1 = np.array([0.5, 0.5])
    test_pattern2 = np.array([0.5, -0.5])
    test_pattern3 = np.array([-0.5, 0.5])
    test_pattern4 = np.array([-0.5, -0.5])

    result1 = hebb_net.classify(test_pattern1)
    result2 = hebb_net.classify(test_pattern2)
    result3 = hebb_net.classify(test_pattern3)
    result4 = hebb_net.classify(test_pattern4)

    print(f"Test Pattern 1 Result: {result1}")
    print(f"Test Pattern 2 Result: {result2}")
    print(f"Test Pattern 3 Result: {result3}")
    print(f"Test Pattern 4 Result: {result4}")

    # Plot input patterns and test patterns
    plot_patterns(input_patterns, 'Input Patterns')
    plot_patterns([test_pattern1, test_pattern2, test_pattern3, test_pattern4], 'Test Patterns')

if __name__ == "__main__":
    main()
''')
    def p5(self):
        print('''
        import numpy as np


class DiscreteFieldNetwork:
    def __init__(self,num_nueron):
        self.num_nueron=num_nueron
        self.weight=np.zeros((num_nueron,num_nueron))
    def train(self,patterns):
        pattern=np.array(patterns)
        outer_product=np.outer(pattern,pattern)
        np.fill_diagonal(outer_product,0)
        self.weight+=outer_product
    def energy(self,state):
        state=np.array(state)
        return 0.5*np.sign(np.dot(self.weight,state))
    def update_rule(self,state):
        new_state=np.sign(np.dot(self.weight,state))
        new_state[new_state>=0]=1
        new_state[new_state<0]=0
        return new_state
    def run(self,initial_state,max_iteration=100):
        current_state=np.array(initial_state)
        for _ in range(max_iteration):
            new_state=self.update_rule(current_state)
            if np.array_equal(new_state,current_state):
                break
        current_state=new_state
        return current_state

hopfield_network=DiscreteFieldNetwork(4)
training_pattern=[[1,1,1,-1]]
hopfield_network.train(training_pattern)
initial_state=[0,0,1,0]
result=hopfield_network.run(initial_state)
print(result)
print("energy:",hopfield_network.energy(result))

''')
    def p6(self):
        print('''
import numpy as np
import matplotlib.pyplot as plt

class KohonenSOM:
    def __init__(self, input_size, map_size):
        self.input_size = input_size
        self.map_size = map_size
        self.weights = np.random.rand(map_size[0], map_size[1], input_size)

    def update_weights(self, input_vector, winner, learning_rate, neighborhood_radius):
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                weight_vector = self.weights[i, j, :]
                distance = np.linalg.norm(np.array([i, j]) - np.array(winner))
                influence = np.exp(-(distance*2) / (2 * neighborhood_radius*2))
                self.weights[i, j, :] += learning_rate * influence * (input_vector - weight_vector)

    def train(self, data, epochs, initial_learning_rate=0.1, initial_radius=None):
        if initial_radius is None:
            initial_radius = max(self.map_size) / 2

        for epoch in range(epochs):
            learning_rate = initial_learning_rate * np.exp(-epoch / epochs)
            neighborhood_radius = initial_radius * np.exp(-epoch / epochs)

            for input_vector in data:
                winner = self.find_winner(input_vector)
                self.update_weights(input_vector, winner, learning_rate, neighborhood_radius)

    def find_winner(self, input_vector):
        min_distance = float('inf')
        winner = (0, 0)

        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                weight_vector = self.weights[i, j, :]
                distance = np.linalg.norm(input_vector - weight_vector)

                if distance < min_distance:
                    min_distance = distance
                    winner = (i, j)

        return winner

    def visualize(self, data):
        colors = ['r', 'g', 'b', 'y', 'c', 'm']

        for input_vector in data:
            winner = self.find_winner(input_vector)
            plt.scatter(winner[0], winner[1], color=colors[np.random.randint(len(colors))])

        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                plt.scatter(i, j, color='k', marker='x')

        plt.show()

# Example usage:
if __name__ == "__main__":
    # Generate some random 2D data points
    data = np.random.rand(100, 2)

    # Create a Kohonen SOM with input size 2 and a 10x10 map
    som = KohonenSOM(input_size=2, map_size=(10, 10))

    # Train the SOM for 100 epochs
    som.train(data, epochs=100)

    # Visualize the result
    som.visualize(data)''')