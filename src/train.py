import tensorflow as tf
import numpy as np

# Not yet tested
def tf_train(X_train, y_train, batch_size=20):
    m = len(X_train)
    n = len(X_train[0])

    X = tf.placeholder(tf.float32, [m, n])
    y = tf.placeholder(tf.float32, [m, 1])

    W = tf.Variable(tf.random_normal([n, 1], stddev=0.1), name="weights")
    b = tf.Variable(tf.zeros([1], name="biases")) # Unused right now

    z = tf.matmul(X, W)

    # Removed to use built-in logistic regression loss function:
    # a = tf.sigmoid(z)
    # loss = tf.reduce_mean( -(y*tf.log(a) + (1-y)*tf.log(1-a)) )

    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=z, labels=y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # Train
    for epoch in range(1000):

        # Stochastic gradient descent; maybe try normal gradient descent?
        idx = np.random.choice(len(X_train), batch_size, replace=False)
        _,l = sess.run([train_step, loss], feed_dict={x: X_train[idx], y: y_train[idx]})
        if epoch % 100 == 0:
            print("loss: " + str(l))

    return sess.run(W)

def accuracy(X, y, weights):
    y_estimate = X.dot(weights)
    y_estimate[y >= 0.5] = 1
    y_estimate[y < 0.5] = 0

    return np.sum(y_estimate == y) / len(y)