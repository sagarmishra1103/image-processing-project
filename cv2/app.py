import streamlit as st
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)

    def display_image(self, image=None):
        if image is None:
            image = self.image
        if image is not None:
            st.image(image, channels="BGR")
        else:
            st.warning("Please upload an image first.")

    def morphological_operations(self, operation, kernel_size):
        if self.image is not None:
            if operation == "Erosion":
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                self.image = cv2.erode(self.image, kernel, iterations=1)
            elif operation == "Dilation":
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                self.image = cv2.dilate(self.image, kernel, iterations=1)
            elif operation == "Opening":
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
            elif operation == "Closing":
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
        else:
            st.warning("Please upload an image first.")

    def gray_level_scaling(self, min_intensity, max_intensity):
        if self.image is not None:
            self.image = cv2.convertScaleAbs(self.image, alpha=(max_intensity - min_intensity) / 255, beta=min_intensity)
        else:
            st.warning("Please upload an image first.")

    def histogram_equalization(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            enhanced_image = cv2.equalizeHist(gray_image)
            self.image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)
        else:
            st.warning("Please upload an image first.")

    def gamma_correction(self, gamma):
        if self.image is not None:
            gamma_corrected = np.array(255 * (self.image / 255) ** gamma, dtype='uint8')
            self.image = gamma_corrected
        else:
            st.warning("Please upload an image first.")

    def contrast_stretching(self):
        if self.image is not None:
            # Convert to grayscale
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # Perform contrast stretching
            min_val = np.min(gray_image)
            max_val = np.max(gray_image)
            stretched_image = 255 * ((gray_image - min_val) / (max_val - min_val))
            self.image = cv2.cvtColor(stretched_image.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        else:
            st.warning("Please upload an image first.")

    def sharpening(self):
        if self.image is not None:
            # Convert to grayscale
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # Apply Laplacian filter for edge detection
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            # Add the Laplacian image to the original image to sharpen it
            sharpened_image = cv2.convertScaleAbs(gray_image - laplacian)
            self.image = cv2.cvtColor(sharpened_image, cv2.COLOR_GRAY2BGR)
        else:
            st.warning("Please upload an image first.")

    def calculate_intensity(self):
        if self.image is not None:
            intensity = cv2.mean(self.image)[0]
            return intensity, self.image
        else:
            st.warning("Please upload an image first.")
            return None, None

def main():
    processor = ImageProcessor()

    st.sidebar.title("Welcome to the Image Processing Application!")
    st.sidebar.write("Please select an option from the sidebar.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        processor.load_image(image_path)
        st.success("Image uploaded successfully!")

    st.empty()

    st.sidebar.subheader("Image Processing Operations")
    operation = st.sidebar.selectbox("Select Operation", ("Home","Morphological Operations", "Gray Level Scaling", "Image Enhancement", "Calculate Image Intensity"))

    if operation == "Home":
        st.title("Home Page")
        st.write("Welcome to the Image Processing Application!")
        st.write("Please select an option from the sidebar.")
        st.button ("upload an Image")
    
    if operation == "Image Enhancement":
        st.sidebar.subheader("Image Enhancement Techniques")
        enhancement_technique = st.sidebar.selectbox("Select Enhancement Technique", ("Histogram Equalization", "Gamma Correction", "Contrast Stretching", "Sharpening"))
        if enhancement_technique == "Histogram Equalization":
            st.sidebar.subheader("Histogram Equalization")
            if st.sidebar.button("Apply"):
                st.empty()
                processor.histogram_equalization()
                processor.display_image()
        elif enhancement_technique == "Gamma Correction":
            st.sidebar.subheader("Gamma Correction")
            gamma_value = st.sidebar.slider("Gamma Value", 0.1, 10.0, 1.0, 0.1)
            if st.sidebar.button("Apply"):
                st.empty()
                processor.gamma_correction(gamma_value)
                processor.display_image()
        elif enhancement_technique == "Contrast Stretching":
            st.sidebar.subheader("Contrast Stretching")
            if st.sidebar.button("Apply"):
                st.empty()
                processor.contrast_stretching()
                processor.display_image()
        elif enhancement_technique == "Sharpening":
            st.sidebar.subheader("Sharpening")
            if st.sidebar.button("Apply"):
                st.empty()
                processor.sharpening()
                processor.display_image()


    elif operation == "Morphological Operations":
        st.sidebar.subheader("Morphological Operations")
        morph_operation = st.sidebar.selectbox("Select Morphological Operation", ("Erosion", "Dilation", "Opening", "Closing"))
        kernel_size = st.sidebar.slider("Kernel Size", 1, 10, 3)
        if st.sidebar.button("Apply"):
            st.empty()
            processor.morphological_operations(morph_operation, kernel_size)
            intensity, image = processor.calculate_intensity()
            if intensity is not None:
                st.write(f"Average Intensity of the Image: {intensity}")
                processor.display_image(image)

    elif operation == "Gray Level Scaling":
        st.sidebar.subheader("Gray Level Scaling")
        min_intensity = st.sidebar.slider("Minimum Intensity", 0, 255, 0)
        max_intensity = st.sidebar.slider("Maximum Intensity", 0, 255, 255)
        if st.sidebar.button("Apply"):
            st.empty()
            processor.gray_level_scaling(min_intensity, max_intensity)
            intensity, image = processor.calculate_intensity()
            if intensity is not None:
                st.write(f"Average Intensity of the Image: {intensity}")
                processor.display_image(image)

    elif operation == "Calculate Image Intensity":
        st.sidebar.subheader("Calculate Image Intensity")
        if st.sidebar.button("Calculate"):
            st.empty()
            intensity, image = processor.calculate_intensity()
            if intensity is not None:
                st.write(f"Average Intensity of the Image: {intensity}")
                processor.display_image(image)

if __name__ == "__main__":
    main()
