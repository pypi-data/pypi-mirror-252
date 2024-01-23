"""
Test basic functionality of classifiers.py
"""
import PIL.Image
import numpy as np
import torch

from aircraft_classifiers_jme45 import classifiers


def test_trivial_classifier(tmp_path):
    torch.manual_seed(0)

    # Instantiate a trivial classifier and save it
    trivial_classifier = classifiers.AircraftClassifier("trivial", "test", False)
    save_path = tmp_path / "test.pth"
    trivial_classifier.save_model(save_path)

    # Now load this classifier again.
    trivial_classifier_loaded = classifiers.AircraftClassifier(
        "trivial", "test", True, save_path
    )

    # Check that the linear layers are equal (the 2nd element in the Sequential).
    assert torch.equal(
        trivial_classifier.model.layers[1].weight,
        trivial_classifier_loaded.model.layers[1].weight,
    )


def test_predict():
    torch.manual_seed(0)

    # Instantiate a trivial classifier and save it
    trivial_classifier = classifiers.AircraftClassifier("trivial", "test", False)

    # Make a random image.
    np.random.seed(0)
    img = PIL.Image.fromarray(np.uint8(255 * np.random.rand(300, 300, 3)))

    # Now make a prediction.
    pred = trivial_classifier.predict(img, apply_crop=False)

    # Get the prediction probability for A380 and check it matches.
    pred_prob_A380_expected = 0.2670742869377136
    pred_prob_A380 = pred[0]["A380"]
    assert np.isclose(pred_prob_A380_expected, pred_prob_A380)
