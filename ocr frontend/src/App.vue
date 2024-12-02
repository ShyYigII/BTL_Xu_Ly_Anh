<template>
  <h1>OCR kết hợp xử lý ảnh</h1>
  <input type="file" @change="onFileChange" accept="image/*" />
  <img v-if="image" :src="image" alt="Uploaded" class="preview" />

  <div v-if="image">
    <select v-model="method">
      <option value="original">Giữ nguyên ảnh gốc</option>
      <option value="otsu">Phân ngưỡng</option>
      <option value="distance_transform">Biến đổi khoảng cách</option>
      <option value="morphological_opening">Phép toán hình thái</option>
    </select>
    <button @click="processImage" :disabled="isLoading">
      Xử lý hình ảnh và OCR
    </button>
  </div>

  <div v-if="isLoading" class="loading-spinner"></div>

  <div v-if="processedImage">
    <h2>Hình ảnh sau khi được xử lý:</h2>
    <img :src="processedImage" alt="Processed" class="preview" />
  </div>

  <div v-if="ocrText">
    <h2>Kết quả OCR:</h2>
    <pre>{{ ocrText }}</pre>
  </div>

  <div v-if="processedImage">
    <a
      :href="processedImage"
      :download="'processed_image.jpg'"
      class="save-button"
    >
      Save Image
    </a>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      image: null,
      file: null,
      method: "original",
      processedImage: null,
      ocrText: null,
      isLoading: false, // Trạng thái loading
    };
  },

  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.file = file;
      this.image = URL.createObjectURL(file);
    },
    async processImage() {
      this.isLoading = true; // Bật trạng thái loading
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
      } finally {
        this.isLoading = false; // Tắt trạng thái loading
      }
    },
  },
};
</script>
<style>
.save-button {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #218838;
}

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

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:enabled {
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

.loading-spinner {
  display: block;
  margin: 20px auto;
  width: 40px;
  height: 40px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
