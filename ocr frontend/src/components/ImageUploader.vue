<template>
  <div id="app">
    <h1>Image Processing Application</h1>
    <input type="file" @change="onFileChange" accept="image/*" />
    <img v-if="image" :src="image" alt="Uploaded" class="preview" />

    <div v-if="image">
      <select v-model="method">
        <option value="otsu">Otsu Thresholding</option>
        <option value="distance_transform">Distance Transform</option>
        <option value="morphological_opening">Morphological Opening</option>
      </select>
      <button @click="processImage">Process Image</button>
    </div>

    <div v-if="processedImage">
      <h2>Processed Image:</h2>
      <img :src="processedImage" alt="Processed" class="preview" />
    </div>

    <div v-if="ocrText">
      <h2>OCR Result:</h2>
      <p>{{ ocrText }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      image: null,
      file: null,
      method: "otsu",
      processedImage: null,
      ocrText: null,
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.file = file;
      this.image = URL.createObjectURL(file);
    },
    async processImage() {
      const formData = new FormData();
      formData.append("image", this.file);
      formData.append("method", this.method);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/process",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        const { processed_image, ocr_text } = response.data;
        this.processedImage = `data:image/jpeg;base64,${btoa(processed_image)}`;
        this.ocrText = ocr_text;
      } catch (error) {
        console.error(error);
        alert("Failed to process image.");
      }
    },
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f9;
}

#app {
  max-width: 800px;
  padding: 20px;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

input[type="file"] {
  display: block;
  margin: 0 auto 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

select {
  display: block;
  margin: 10px auto 20px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

button {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

img {
  max-width: 100%;
  margin: 20px 0;
  display: block;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

p {
  text-align: center;
  font-size: 18px;
  color: #333;
}
</style>
