# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:15:11 2025

@author: Rohan
"""

import os
import re
import sys
import tarfile
import numpy as np
import tensorflow as tf
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3

# Global Variables
yaw = 0
counter = 1

# Paths for model and image
MODEL_PATH = '/tmp/inception_model'
IMAGE_PATH = ''

# TensorFlow app flags
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('model_directory', MODEL_PATH, "Directory for model files.")
tf.app.flags.DEFINE_string('image_path', IMAGE_PATH, "Path to input image.")
tf.app.flags.DEFINE_integer('top_predictions', 1, "Number of top predictions to display.")

# URL for the Inception model tarball
MODEL_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


class LabelLookup:
    def __init__(self, label_path=None, uid_path=None):
        if not label_path:
            label_path = os.path.join(FLAGS.model_directory, 'imagenet_2012_label_map.pbtxt')
        if not uid_path:
            uid_path = os.path.join(FLAGS.model_directory, 'imagenet_synset_to_human_labels.txt')
        self.label_map = self.load_labels(label_path, uid_path)

    def load_labels(self, label_path, uid_path):
        """Load human-readable labels."""
        if not tf.gfile.Exists(uid_path):
            tf.logging.fatal('File does not exist %s', uid_path)
        if not tf.gfile.Exists(label_path):
            tf.logging.fatal('File does not exist %s', label_path)

        # Load the label-to-human mapping
        uid_to_name = {}
        with tf.gfile.GFile(uid_path) as file:
            lines = file.readlines()
            for line in lines:
                items = re.findall(r'[n\d]+[ \S,]*', line)
                uid, human_name = items[0], items[2]
                uid_to_name[uid] = human_name

        # Mapping from node ID to human-readable string
        node_id_to_name = {}
        with tf.gfile.GFile(label_path) as file:
            lines = file.readlines()
            for line in lines:
                if 'target_class:' in line:
                    target_class = int(line.split(': ')[1])
                if 'target_class_string:' in line:
                    target_class_str = line.split(': ')[1].strip('"')
                    node_id_to_name[target_class] = uid_to_name.get(target_class_str)

        return node_id_to_name

    def id_to_string(self, node_id):
        return self.label_map.get(node_id, '')


def create_model_graph():
    """Load the trained model graph."""
    with tf.gfile.FastGFile(os.path.join(FLAGS.model_directory, 'classify_image_graph_def.pb'), 'rb') as file:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(file.read())
        tf.import_graph_def(graph_def, name='')


def perform_inference(image_file):
    """Run inference on the image."""
    if not tf.gfile.Exists(image_file):
        tf.logging.fatal('File does not exist %s', image_file)

    image_data = tf.gfile.FastGFile(image_file, 'rb').read()

    create_model_graph()

    with tf.Session() as session:
        softmax_tensor = session.graph.get_tensor_by_name('softmax:0')
        predictions = session.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Lookup labels for predictions
        label_lookup = LabelLookup()
        top_k = predictions.argsort()[-FLAGS.top_predictions:][::-1]

        for node_id in top_k:
            label = label_lookup.id_to_string(node_id)
            score = predictions[node_id]
            print(f'{label} (score = {score:.5f})')

            # Save predictions to a CSV file
            with open("Predictions.csv", "a") as file:
                file.write(f"\t{label}")


def download_and_extract_model():
    """Download and extract the model."""
    destination = FLAGS.model_directory
    if not os.path.exists(destination):
        os.makedirs(destination)
    file_name = MODEL_URL.split('/')[-1]
    file_path = os.path.join(destination, file_name)
    
    if not os.path.exists(file_path):
        def _progress(count, block_size, total_size):
            sys.stdout.write(f'\r>> Downloading {file_name} {float(count * block_size) / total_size * 100.0:.1f}%')
            sys.stdout.flush()

        urllib.request.urlretrieve(MODEL_URL, file_path, _progress)
        print()
        statinfo = os.stat(file_path)
        print(f'Successfully downloaded {file_name} {statinfo.st_size} bytes.')

    tarfile.open(file_path, 'r:gz').extractall(destination)


def position_callback(msg):
    """Callback function for position data."""
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rospy.loginfo(f'X: {x}, Y: {y}')


def orientation_callback(msg):
    """Callback function for orientation data."""
    global yaw, counter
    yaw = msg.z
    if counter == 1:
        with open("Predictions.csv", "a") as file:
            file.write(f"\n{yaw:.5f}")
        counter = 2


def main():
    """Main function."""
    global yaw, counter
    counter = 1
    rospy.init_node('image_classification', anonymous=True)
    rospy.Subscriber("/rpy_angles", Vector3, orientation_callback)

    download_and_extract_model()

    # Use default image file if not provided
    image_file = FLAGS.image_path if FLAGS.image_path else os.path.join(FLAGS.model_directory, 'cropped_panda.jpg')
    perform_inference(image_file)


if __name__ == '__main__':
    tf.app.run()
