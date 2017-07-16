import numpy as np


class RNN:
    def __init__(self, text, n_hidden_states=100, learning_rate=.0005, gamma=0.9, epsilon=1e-20,
                 sequence_length=25, sigma=0.01):
        # Obtain alphabet
        """
        :param text: Text to train on, as a string
        :param n_hidden_states: number of hidden units
        :param learning_rate: learning rate
        :param sequence_length: Length of the generated strings
        :param sigma: Standard deviation used in the initialization of the model parameters
        """
        self.text = text
        self.text_size = len(self.text)
        self.alphabet = np.unique(list(text))
        # Dimensionality of output/input layer
        self.alphabet_size = len(self.alphabet)
        # Dimensionality of the hidden layer
        self.hidden_units = n_hidden_states
        # Learning rate
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        # Length of input sequence
        self.sequence_length = sequence_length
        # Bias terms
        self.b = np.zeros([self.hidden_units, 1])
        self.c = np.zeros([self.alphabet_size, 1])
        # Weight matrices
        self.U = sigma * np.random.randn(self.hidden_units, self.alphabet_size)
        self.W = sigma * np.random.randn(self.hidden_units, self.hidden_units)
        self.V = sigma * np.random.randn(self.alphabet_size, self.hidden_units)
        # Mapping between indices and characters
        self.encoder = Encoder(self)

    def forward_pass(self, input_sequence, previous_state):
        """
        Predicts output sequence given an input sequence (matrix one-hot encoding)
        :param input_sequence: Input text sequence as a one-hot encoded matrix alphabet_size x seq_length
        :return: output_estimate: Next character probability matrix (alphabet_size x sequence_length),
                hidden_states: Hidden states (hidden_units x sequence_length)
        """
        # Initial zero state
        hidden_states, output_estimate = self._forward_pass(input_sequence[:, 0], previous_state)
        previous_state = hidden_states
        for i in range(1, input_sequence.shape[1]):
            previous_state, _output_estimate = self._forward_pass(input_sequence[:, i], previous_state)
            output_estimate = np.column_stack((output_estimate, _output_estimate))
            hidden_states = np.column_stack((hidden_states, previous_state))

        return hidden_states, output_estimate

    def _forward_pass(self, input_character, hidden_state):
        """
        Performs the forward pass on a one-hot encoded vector
        :param input_character: Input character as one-hot encoded vector, alphabet_size x 1
        :param hidden_state: Hidden state, n_hidden_units x 1
        :return: p: Output probabilities for the next character. p[k] is the probability of the k-th character being the
                next one (alphabet_size x 1); h: hidden state (m x 1); activity values (alphabet_size x 1)
        """
        a = self.W @ hidden_state + self.U.dot(input_character).reshape(-1, 1) + self.b
        hidden_state = np.tanh(a)
        o = self.V @ hidden_state + self.c  # self.V.dot(h)
        p = softmax(o)
        return hidden_state, p

    @staticmethod
    def compute_cost(output_estimate, output_sequence):
        """
        Computes cost between predicted and targeted output sequence
        :param output_estimate: Predicted sequence, as one-hot matrix (K x seq_length)
        :param output_sequence: Targeted sequence, as one-hot matrix (K x seq_length)
        :return: Cross-entropy loss
        """
        return -np.sum(np.log(np.sum(np.multiply(output_estimate, output_sequence), 0) + 1e-20))

    def compute_grad(self, param_names, input_sequence, hidden_states, output_estimate, output_sequence, previous_state):
        """
        Computes the gradient from the parameters listed in grad_names
        :param param_names: List of strings containing the name of the model parameters to find the gradient from
        :param input_sequence: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
        :param hidden_states: Activations in the hidden layer (hidden_units x sequence_length)
        :param output_estimate: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
        :param output_sequence: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)
        :return: Dictionary containing the gradient from the model parameters specified by grad_names
        """
        gradients = {}

        # Model parameters at the Output layer
        G = output_estimate - output_sequence

        if param_names.__contains__("V"):
            gradients["V"] = np.dot(G, hidden_states.T).clip(-5, 5)
        if param_names.__contains__("c"):
            gradients["c"] = G.sum(axis=1).reshape(-1, 1).clip(-5, 5)

        # Model parameters at the Hidden layer
        f = G[:, -1].dot(self.V).dot(np.diag(np.ones(self.hidden_units) - hidden_states[:, -1] ** 2))
        F = f
        for i in range(2, self.sequence_length + 1):
            f = (G[:, -i].dot(self.V) + f.dot(self.W)).dot(
                np.diag(np.ones(self.hidden_units) - hidden_states[:, -i] ** 2))
            F = np.column_stack((F, f))
        F = np.fliplr(F)

        if param_names.__contains__("W"):
            H_ = np.roll(hidden_states, 1)
            H_[:, :1] = previous_state.reshape(-1, 1)
            gradients["W"] = np.dot(F, H_.T).clip(-5, 5)
        if param_names.__contains__("U"):
            gradients["U"] = np.dot(F, input_sequence.T).clip(-5, 5)
        if param_names.__contains__("b"):
            gradients["b"] = F.sum(axis=1).reshape(-1, 1).clip(-5, 5)

        return gradients

    def backward_pass(self, input_sequence, hidden_states, output_estimate, output_sequence, previous_state):
        """
        Computes the gradient of all the model parameters
        :param input_sequence: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
        :param hidden_states: Activations in the hidden layer (hidden_units x sequence_length)
        :param output_estimate: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
        :param output_sequence: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)
        :param previous_state: Previous state, hidden units x 1
        :return:
        """
        param_names = ["W", "U", "b", "V", "c"]
        return self.compute_grad(param_names, input_sequence, hidden_states, output_estimate, output_sequence,
                                 previous_state)

    def adagrad_update(self, grads, m):
        """
        Ada-Grad update rule
        :param grads: Gradients of the model parameters
        :param m: 
        :return:
        """
        m["W"] = self.gamma*m["W"] + (1-self.gamma)*grads["W"]**2
        self.W -= self.learning_rate/(np.sqrt(m["W"] + self.epsilon))*grads["W"]
        m["U"] = self.gamma*m["U"] + (1-self.gamma)*grads["U"]**2
        self.U -= self.learning_rate/(np.sqrt(m["U"] + self.epsilon))*grads["U"]
        m["V"] = self.gamma*m["V"] + (1-self.gamma)*grads["V"]**2
        self.V -= self.learning_rate/(np.sqrt(m["V"] + self.epsilon))*grads["V"]
        m["b"] = self.gamma*m["b"] + (1-self.gamma)*grads["b"]**2
        self.b -= self.learning_rate/(np.sqrt(m["b"] + self.epsilon))*grads["b"]
        m["c"] = self.gamma*m["c"] + (1-self.gamma)*grads["c"]**2
        self.c -= self.learning_rate/(np.sqrt(m["c"] + self.epsilon))*grads["c"]

        return m

    def generate_sequence(self, epochs=100):
        """
        generates a sequence based on the sentences from a user
        :param epochs: number of epochs to train the model
        :return:
        """
        m = {"W": 0, "U": 0, "V": 0, "b": 0, "c": 0}
        smooth_loss = 0
        smooth_loss_history = []
        generated_sequences = {}
        for epoch in range(epochs):
            previous_state = np.zeros([self.hidden_units, 1])
            for idx in range(0, self.text_size-self.sequence_length-1, self.sequence_length):
                iteration = int(epoch*self.text_size/self.sequence_length + idx/self.sequence_length)
                # Load input and output sequences
                input_sequence, output_sequence = self.get_data(idx)

                # Forward pass: Obtain estimate and model intermediate values
                hidden_states, output_estimate = self.forward_pass(input_sequence, previous_state)

                if iteration % 500 == 0:
                    info = "iter = " + str(iteration) + ", smooth loss = " + str(smooth_loss)
                    print(info)

                    if (iteration+500) % 10000 == 0 or iteration == 0:
                        initial_char = input_sequence[:, 0]
                        print("-------")
                        generated_sequence = self.generate_output_string(initial_char, previous_state, 100)
                        print(generated_sequence)
                        generated_sequences[iteration] = generated_sequence
                        print("-------")
                    smooth_loss_history.append(smooth_loss)

                previous_state = hidden_states[:, -1].reshape(-1, 1)
                # Loss
                loss = self.compute_cost(output_estimate, output_sequence)
                smooth_loss = .999 * smooth_loss + .001 * loss
                # Backward pass: Obtain gradient of model parameters
                grads = self.backward_pass(input_sequence, hidden_states, output_estimate, output_sequence,
                                           previous_state)
                # Update model parameters
                m = self.adagrad_update(grads, m)

        print("-------")
        print("*** FINAL TEXT GENERATION ***")
        generated_sequence = self.generate_output_string(initial_char, previous_state, 1000)
        print(generated_sequence)
        generated_sequences[iteration] = generated_sequence
        print("-------")
        iters = list(range(0, 500*len(smooth_loss_history), 500))
        return smooth_loss_history, iters, generated_sequences

    def generate_output_string(self, input_character, previous_state, sequence_length):
        s = ""
        for i in range(sequence_length):
            previous_state, p = self._forward_pass(input_character, previous_state)
            input_character = self.sample_from_distrib(p)
            s += self.encoder.index_to_char(input_character)
            input_character = self.encoder.index_to_onehot(input_character)
        return s

    def get_data(self, idx):
        """
        Obtains the idx-th input and output sentences in one-hot-encoded matrices format
        :param idx: Index of the input-output pair to get
        :return: Two matrices, one for the input sentence and the other for the output sentence, both K x seq_length
        """
        if idx < len(self.text):
            X_char = self.text[idx:idx + self.sequence_length]
            Y_char = self.text[idx + 1:idx + self.sequence_length + 1]
            X = np.array([self.encoder.char_to_onehot(x) for x in X_char]).reshape(self.sequence_length,
                                                                                   self.alphabet_size).T
            Y = np.array([self.encoder.char_to_onehot(y) for y in Y_char]).reshape(self.sequence_length,
                                                                                   self.alphabet_size).T
            return X, Y
        else:
            print("Index not valid")
            return -1

    def sample_from_distrib(self, p):
        """
        Samples from probability distribution
        :param p: Probability distribution vector, p[k] denotes the probability of the k-th value
        :return: An integer {1, 2, ...,k} sampled from the p
        """
        p = p.T[0]
        k = np.random.choice(np.arange(self.alphabet_size), p=p)
        return k


class TestGradient:
    def __init__(self, text, n_hidden_states):
        self.rnn = RNN(text, n_hidden_states=n_hidden_states)
        self.n_hidden_states = n_hidden_states
        self.initial_state = np.zeros([self.n_hidden_states, 1])

    def run(self):
        """
        Executes the code, checking if the analytical gradient of rnn is well implemented
        :return: Relative L1 loss between analytical and numerical gradients
        """
        input_sequence, output_sequence = self.rnn.get_data(0)
        hidden_states, output_estimate = self.rnn.forward_pass(input_sequence, self.initial_state)
        grad_names = ["W", "U", "b", "V", "c"]
        e = self.gradient_check(grad_names, input_sequence, hidden_states, output_estimate, output_sequence,
                                self.initial_state)
        return e

    def gradient_check(self, param_names, input_sequence, hidden_states, output_estimate, output_sequence, init_state):
        """
        Computes the error between the numerical and analytical gradients
        :param param_names: List of strings containing the name of the model parameters to find the gradient from
        :param input_sequence: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
        :param hidden_states: Activations in the hidden layer (hidden_units x sequence_length)
        :param output_estimate: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
        :param output_sequence: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)
        :return: Relative L1 loss between numerical and analytical gradients
        """
        numerical_gradients = self.compute_grad_num(param_names, input_sequence, output_sequence, init_state)
        error = {}
        grads = self.rnn.compute_grad(param_names, input_sequence, hidden_states, output_estimate, output_sequence,
                                      init_state)
        for param_name in param_names:
            error[param_name] = self.error(grads[param_name], numerical_gradients[param_name])
        return error

    @staticmethod
    def error(a, b):
        """
        Computes the error between two vectors, using the relative l1 loss
        :param a: Array of size n
        :param b: Array of size n
        :return: Error (float)
        """
        return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))

    def compute_grad_num(self, param_names, input_sequence, output, init_state, h=1e-4):
        """
        Computes the gradient of a model parameter numerically
        :param param_names: List containing the model parameters' names to check
        :param input_sequence: Input sequence in one-hot format
        :param output: Output sequence in one-hot format
        :param h: Slope
        :return: Numerical gradients
        """
        grads = {}
        for param_name in param_names:
            if param_name is "W":
                grads[param_name] = self.compute_grad_num_matrix(self.rnn.W, input_sequence, output, init_state, h)
            elif param_name is "U":
                grads[param_name] = self.compute_grad_num_matrix(self.rnn.U, input_sequence, output, init_state, h)
            elif param_name is "V":
                grads[param_name] = self.compute_grad_num_matrix(self.rnn.V, input_sequence, output, init_state, h)
            elif param_name is "b":
                grads[param_name] = self.compute_grad_num_vector(self.rnn.b, input_sequence, output, init_state, h)
            elif param_name is "c":
                grads[param_name] = self.compute_grad_num_vector(self.rnn.c, input_sequence, output, init_state, h)

        return grads

    def compute_grad_num_vector(self, param, input_sequence, output, init_state, h):
        """
        Numerically obtains the gradient of a given model parameter (vector shape)
        :param param: Model parameter
        :param input_sequence: Input sequence, one-hot matrix format
        :param output: Output sequence in one-hot matrix format
        :param h: Increment to compute, numerically, the slope
        :return: Vector containing the partial derivatives (gradient) of the given model parameter
        """
        grad = np.zeros(param.shape)
        for i in range(len(param)):
            param[i] += h
            _, P_pos = self.rnn.forward_pass(input_sequence, init_state)
            c_pos = self.rnn.compute_cost(P_pos, output)
            param[i] -= 2 * h
            _, P_neg = self.rnn.forward_pass(input_sequence, init_state)
            c_neg = self.rnn.compute_cost(P_neg, output)
            param[i] += h
            grad[i] = (c_pos - c_neg) / (2 * h)
        return grad

    def compute_grad_num_matrix(self, param, input_sequence, output, init_state, h):
        """
        Numerically obtains the gradient of a given model parameter (matrix shape)
        :param param: Model parameter (matrix shape)
        :param input_sequence: Input sequence, one-hot matrix format
        :param output: Output sequence in one-hot matrix format
        :param h: Increment to compute, numerically, the slope
        :return: Matrix containing the partial derivatives (gradient) of the given model parameter
        """
        grad = np.zeros(param.shape)
        for i in range(param.shape[0]):
            for j in range(param.shape[1]):
                param[i, j] += h
                _, P_pos = self.rnn.forward_pass(input_sequence, init_state)
                c_pos = self.rnn.compute_cost(P_pos, output)
                param[i, j] -= 2 * h
                _, P_neg = self.rnn.forward_pass(input_sequence, init_state)
                c_neg = self.rnn.compute_cost(P_neg, output)
                param[i, j] += h
                grad[i, j] = (c_pos - c_neg) / (2 * h)
        return grad


class Encoder:
    """
    This class implements several parsers
    """
    def __init__(self, rnn):
        self.rnn = rnn
        self.char_to_ind, self.ind_to_char = set_mappings(self.rnn.alphabet)

    def index_to_char(self, ind):
        """
        Converts an indexed to its corresponding character
        :param ind: integer index
        :return: character
        """
        return self.ind_to_char[ind]

    def char_to_index(self, char):
        """
        Converts a character to its corresponding index
        :param char: character
        :return: integer index
        """
        return self.char_to_ind[char]

    def index_to_onehot(self, ind):
        """
        Converts an index to its corresponding one-hot vector
        :param ind: integer index
        :return: onehot vector
        """
        v = np.zeros([self.rnn.alphabet_size, 1])
        v[ind] = 1
        return v

    @staticmethod
    def onehot_to_index(onehot):
        """
        Converts a one-hot vector to its corresponding index
        :param onehot: onehot vector
        :return: integer index
        """
        return onehot.argmax()

    def char_to_onehot(self, char):
        """
        Converts a character to its corresponding one-hot evector
        :param char:
        :return:
        """
        ind = self.char_to_ind[char]
        return self.index_to_onehot(ind)

    def onehot_to_char(self, onehot):
        """
        Converts a one-hot vector to its corresponding chracter
        :param onehot:
        :return:
        """
        ind = self.onehot_to_index(onehot)
        return self.ind_to_char[ind]


def softmax(x):
    """
    Applies softmax to an input vector
    :param x: Input vector
    :return: Vector with the softmax values of x
    """
    s = sum(np.exp(x))
    return np.exp(x) / s


def set_mappings(alphabet):
    """
    Given an alphabet it obtains the mapping between characters and indices
    :param alphabet: List of characters
    :return: Two dictionaries, mapping indices (int) to characters (chars) and viceversa
    """
    char_to_ind = {}
    ind_to_char = {}
    idx = 0

    for char in alphabet:
        char_to_ind[char] = idx
        ind_to_char[idx] = char
        idx += 1

    return char_to_ind, ind_to_char


def read_data(filename="Globet.txt"):
    # Read the text file and extract all the characters that it contains
    """
    Reads the data from a given file
    :param filename: Name of the file containing the text to read
    :return: Read text as a list of characters
    """
    with open(filename) as f:
        book_text = f.read()
    return list(book_text)
