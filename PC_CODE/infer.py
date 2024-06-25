import onnxruntime
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch
import os
import csv

# Load the ONNX model
onnx_model_path = 'efficientnet-b0_imgsz128.onnx'
ort_session = onnxruntime.InferenceSession(onnx_model_path)

def inference(image_path):
    # Load and preprocess the input image
    #image_path = 'bombo.jpg'
    img = Image.open(image_path).convert('RGB')
    img = img.resize((128, 128))  # Resize to 128x128
    img = transforms.ToTensor()(img)
    img = img.numpy()
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Run inference
    ort_inputs = {ort_session.get_inputs()[0].name: img}
    ort_outs = ort_session.run(None, ort_inputs)

    # Process the output
    # The output depends on the specific task the model was trained for (e.g., classification, object detection, etc.)
    # You'll need to check the model's documentation or inspect the outputs to understand how to interpret them.

    probs = torch.softmax(torch.tensor(ort_outs[0][0]), dim=0)  # probabilities
    #print(probs*100)

    class_labels = [
        "ant",
        "bee",
        "bee_apis",
        "bee_bombus",
        "beetle",
        "beetle_cocci",
        "beetle_oedem",
        "bug",
        "bug_grapho",
        "fly",
        "fly_empi",
        "fly_sarco",
        "fly_small",
        "hfly_episyr",
        "hfly_eristal",
        "hfly_eupeo",
        "hfly_myathr",
        "hfly_sphaero",
        "hfly_syrphus",
        "lepi",
        "none_background",
        "none_bird",
        "none_dirt",
        "none_shadow",
        "other",
        "scorpionfly",
        "wasp"
    ]


    #print(class_labels)
    max_index = ort_outs[0].argmax()

    # Retrieve the corresponding class label from the class labels list
    detected_class = class_labels[max_index]

    # Print the detected class and its confidence score
    print(f"Detected class: {detected_class}, Confidence score: {probs[max_index]}")

    return detected_class

