# growingnn

Framework that implements an algorithm allowing a neural network to grow while training

## Usage

### Simple query

```python
x_train, x_test, y_train, y_test, labels = data_reader.read_mnist_data(mnist_path, 0.9)
gnn.trainer.train(
    x_train = x_train, 
    y_train = y_train, 
    x_test = x_test,
    y_test = y_test,
    labels = labels,
    input_paths = 1,
    path = "./result", 
    model_name = "GNN_model",
    epochs = 10, 
    generations = 10,
    input_size = 28 * 28, 
    hidden_size = 28 * 28, 
    output_size = 10, 
    input_shape = (28, 28, 1), 
    kernel_size = 3, 
    depth = 2
)
```
This code trains a simple network on the MNIST dataset


# Credits

Szymon Świderski
Agnieszka Jastrzębska

# Disclosure

This is the first beta version of this package. I am not liable for the accuracy of this program’s output nor actions performed based upon it.