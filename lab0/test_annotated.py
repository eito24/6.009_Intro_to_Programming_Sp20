#!/usr/bin/env python3

import os
import lab_annotated
import pickle
import hashlib
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


class Lab0Test(unittest.TestCase):
    def compare_images(self, im1, im2):
        self.assertTrue(set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary')
        self.assertEqual(im1['height'], im2['height'], 'Heights must match')
        self.assertEqual(im1['width'], im2['width'], 'Widths must match')
        self.assertEqual(len(im1['pixels']), im1['height']*im1['width'], 'Incorrect number of pixels')
        self.assertTrue(all(isinstance(i, int) for i in im1['pixels']), 'Pixels must all be integers')
        self.assertTrue(all(0<=i<=255 for i in im1['pixels']), 'Pixels must all be in the range from [0, 255]')
        pix_incorrect = (None, None)
        for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
            if i != j:
                pix_incorrect = (ix, abs(i-j))
        self.assertTrue(pix_incorrect == (None, None), 'Pixels must match.  Incorrect value at location %s (differs from expected by %s)' % pix_incorrect)


class TestImage(Lab0Test):
    def test_load(self):
        result = lab_annotated.load_image('test_images/centered_pixel.png')
        expected = {
            'height': 11,
            'width': 11,
            'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }
        self.compare_images(result, expected)


class TestInverted(Lab0Test):
    #tests the inversion of the center white, others black image
    def test_inverted_1(self):
        im = lab_annotated.load_image('test_images/centered_pixel.png')
        result = lab_annotated.inverted(im)
        expected = {
            'height': 11,
            'width': 11,
            'pixels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                       255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        }
        self.compare_images(result, expected)

    def test_inverted_2(self):
        im={'height':1,'width':4,'pixels':[14, 66, 130, 206]}
        result = lab_annotated.inverted(im)
        expected = {'height':1,'width':4,'pixels':[241, 189, 125, 49]}
        self.compare_images(result, expected)
    def test_inverted_images(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
                im = lab_annotated.load_image(inpfile)
                oim = object_hash(im)
                result = lab_annotated.inverted(im)
                expected = lab_annotated.load_image(expfile)
                self.assertEqual(object_hash(im), oim, 'Be careful not to modify the original image!')
                self.compare_images(result, expected)


class TestFilters(Lab0Test):
    def test_blurred(self):
        for kernsize in (1, 3, 7):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
                    input_img = lab_annotated.load_image(inpfile)
                    input_hash = object_hash(input_img)
                    result = lab_annotated.blurred(input_img, kernsize)
                    expected = lab_annotated.load_image(expfile)
                    self.assertEqual(object_hash(input_img), input_hash, "Be careful not to modify the original image!")
                    self.compare_images(result, expected)

    def test_blurred_black_image(self):
        #blurring a black image returns a black image
        image={'height': 6,
                'width': 5,
                'pixels': [255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255]}
        expected = {'height': 6,
                    'width': 5,
                    'pixels': [255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255,
                            255, 255, 255, 255, 255]}
        #applying the blurred function twice still results in a black image
        result=lab_annotated.blurred(image,5)
        resulted=lab_annotated.blurred(result,3)
        self.compare_images(resulted,expected)

        #blurs the centered pixel image, blurs it so 255/9 applied to the middle 9 pixels, rounded down
    def test_blurred_centered_pixel_1(self):
        a=lab_annotated.load_image('test_images/centered_pixel.png')
        result=lab_annotated.blurred(a,3)
        expected={'height': 11,
                    'width': 11,
                    'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}        
        self.compare_images(result,expected)
        #blurs the centered pixel image, blurs it so 255/25 applied to the middle 25 pixels, rounded down
    def test_blurred_centered_pixel_2(self):
        a=lab_annotated.load_image('test_images/centered_pixel.png')
        result=lab_annotated.blurred(a,5)
        expected={'height': 11,
                    'width': 11,
                    'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                                0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                                0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                                0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                                0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.compare_images(result,expected)                                
        # REPLACE THIS with your 2nd test case from section 5.1

    def test_sharpened(self):
        for kernsize in (1, 3, 9):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
                    input_img = lab_annotated.load_image(inpfile)
                    input_hash = object_hash(input_img)
                    result = lab_annotated.sharpened(input_img, kernsize)
                    expected = lab_annotated.load_image(expfile)
                    self.assertEqual(object_hash(input_img), input_hash, "Be careful not to modify the original image!")
                    self.compare_images(result, expected)

    def test_edges(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
                input_img = lab_annotated.load_image(inpfile)
                input_hash = object_hash(input_img)
                result = lab_annotated.edges(input_img)
                expected = lab_annotated.load_image(expfile)
                self.assertEqual(object_hash(input_img), input_hash, "Be careful not to modify the original image!")
                self.compare_images(result, expected)

#edges are amplified thus turns all black
    def test_edges_centered_pixel(self):
        im = lab_annotated.load_image('test_images/centered_pixel.png')
        result = lab_annotated.edges(im)
        expected = {
            'height': 11,
            'width': 11,
            'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0,
                        0, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0,
                        0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.compare_images(result, expected)        

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
