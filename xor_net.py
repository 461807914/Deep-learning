#!/usr/bin/env python
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def list_to_flat_array(labels):
    return np.array(labels).reshape(len(labels), -1)


def analyze_classifier(sess, i, w1, b1, w2, b2, XOR_X, XOR_T):
    print('\nEpoch %i' % i)
    print('Hypothesis %s' % sess.run(hypothesis,
                                     feed_dict={input_: XOR_X,
                                                target: XOR_T}))
    print('w1=%s' % sess.run(w1))
    print('b1=%s' % sess.run(b1))
    print('w2=%s' % sess.run(w2))
    print('b2=%s' % sess.run(b2))
    print('cost (ce)=%s' % sess.run(cross_entropy,
                                    feed_dict={input_: XOR_X,
                                               target: XOR_T}))
    # ���ӻ�����߽�
    xs = np.linspace(-5, 5)
    ys = np.linspace(-5, 5)
    pred_classes = []
    for x in xs:
        for y in ys:
            pred_class = sess.run(hypothesis,
                                  feed_dict={input_: [[x, y]]})
            pred_classes.append((x, y, pred_class.argmax()))
    xs_p, ys_p = [], []
    xs_n, ys_n = [], []
    for x, y, c in pred_classes:
        if c == 0:
            xs_n.append(x)
            ys_n.append(y)
        else:
            xs_p.append(x)
            ys_p.append(y)
    plt.plot(xs_p, ys_p, 'ro', xs_n, ys_n, 'bo')
    plt.show()


# ѵ������
XOR_X = [[0, 0], [0, 1], [1, 0], [1, 1]]  

XOR_Y = [0, 1, 1, 0]  # ÿ�����ݶ�Ӧ�Ľ��

assert len(XOR_X) == len(XOR_Y)  # ������ݺͱ�ǩ�Ƿ�һ��


enc = OneHotEncoder()
enc.fit(list_to_flat_array(XOR_Y))
XOR_T = enc.transform(list_to_flat_array(XOR_Y)).toarray()

'''
XOR_T���Ϊ
[[ 1.  0.]
 [ 0.  1.]
 [ 0.  1.]
 [ 1.  0.]]
 ��ʾ
 [0,1,1,0]��Ӧ��onehotencodingֵ

'''

# �ֳɼ���
nb_classes = 2

'''
placeholder������
��������
������״(�������д���Զ�����)
������

'''
input_ = tf.placeholder(tf.float32,
                        shape=[None, len(XOR_X[0])],
                        name="input")
target = tf.placeholder(tf.float32,
                        shape=[None, nb_classes],
                        name="output")
nb_hidden_nodes = 2
# enc = tf.one_hot([0, 1], 2)
# ��һ�㣬�������ݻ�ȡ����
w1 = tf.Variable(tf.random_uniform([2, nb_hidden_nodes], -1, 1, seed=0),
                 name="Weights1")

w2 = tf.Variable(tf.random_uniform([nb_hidden_nodes, nb_classes], -1, 1,
                                   seed=0),
                 name="Weights2")


b1 = tf.Variable(tf.zeros([nb_hidden_nodes]), name="Biases1")

b2 = tf.Variable(tf.zeros([nb_classes]), name="Biases2")

'''
matmul������˷�
inputΪ?��2�еľ���w1Ϊ2��2�еľ���
'''
activation2 = tf.sigmoid(tf.matmul(input_, w1) + b1)

#����һ��?��2�еľ����ʾÿ�������Ӧ�ĸ���

hypothesis = tf.nn.softmax(tf.matmul(activation2, w2) + b2)

#���㽻����

cross_entropy = -tf.reduce_sum(target * tf.log(hypothesis))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)

# Start training
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)


    for i in range(20001):
        #����ֵinput_�� [[0, 0], [0, 1], [1, 0], [1, 1]]
        #��ǩtarget��   [[ 1.  0.][ 0.  1.][ 0.  1.][ 1.  0.]]
        sess.run(train_step, feed_dict={input_: XOR_X, target: XOR_T})

        if i % 10000 == 0:
            analyze_classifier(sess, i, w1, b1, w2, b2, XOR_X, XOR_T)
