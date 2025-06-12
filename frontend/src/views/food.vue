<template>
  <div class="food-scanner-container">
    <div class="main-content">
      <div class="header-section">
        <div class="header-content">
          <div class="header-icon">
            <i class="bi bi-camera-fill"></i>
          </div>
          <div class="header-text">
            <h1 class="header-title">Food Scanner</h1>
            <p class="header-subtitle">
              AI-Powered Food Recognition & Recipe Discovery
            </p>
          </div>
        </div>
      </div>

      <div class="upload-section">
        <div class="upload-card">
          <div
            class="upload-zone"
            :class="{
              'drag-over': isDragOver,
              disabled: loading,
              'has-image': imagePreviewUrl,
            }"
            @dragover.prevent="handleDragOver"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input
              type="file"
              @change="onFileChange"
              accept="image/*"
              id="fileInput"
              ref="fileInput"
              :disabled="loading"
              style="display: none"
            />

            <div v-if="!imagePreviewUrl" class="upload-content">
              <div class="upload-icon">
                <i class="bi bi-cloud-upload"></i>
              </div>
              <h3 class="upload-title">Drop your food image here</h3>
              <p class="upload-subtitle">or click to browse from your device</p>
              <div class="upload-formats">
                <span class="format-tag">JPG</span>
                <span class="format-tag">PNG</span>
                <span class="format-tag">WEBP</span>
              </div>
            </div>

            <div v-if="imagePreviewUrl" class="image-preview-container">
              <img
                :src="imagePreviewUrl"
                alt="Food Preview"
                class="image-preview"
              />
              <button @click.stop="removeImage" class="btn-remove">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>

          <div class="action-buttons">
            <button
              @click="uploadImage"
              :disabled="!selectedFile || loading"
              class="btn-analyze"
            >
              <span v-if="loading">
                <div class="loading-spinner"></div>
                Analyzing...
              </span>
              <span v-else>
                <i class="bi bi-magic"></i>
                Analyze Food
              </span>
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading-section">
        <div class="loading-card">
          <div class="loading-animation">
            <div class="loading-circle"></div>
            <div class="loading-pulse"></div>
          </div>
          <h3 class="loading-title">AI is analyzing your image</h3>
          <p class="loading-subtitle">
            Identifying ingredients and finding recipes...
          </p>
        </div>
      </div>

      <div v-if="error" class="error-section">
        <div class="error-card">
          <div class="error-icon">
            <i class="bi bi-exclamation-triangle"></i>
          </div>
          <div class="error-content">
            <h4 class="error-title">Something went wrong</h4>
            <p class="error-message">{{ error }}</p>
          </div>
        </div>
      </div>

      <div v-if="predictedFood && !loading" class="results-section">
        <div class="result-card classification-card">
          <div class="result-header">
            <div class="result-avatar classification">
              <i class="bi bi-robot"></i>
            </div>
            <div class="result-info">
              <h4 class="result-title">AI Classification</h4>
              <span class="result-time">Just now</span>
            </div>
          </div>
          <div class="result-content">
            <div class="classification-result">
              <span class="classification-label">Identified as:</span>
              <span class="classification-value">
                {{ displayedPrediction }}
                <span v-if="isTypingPrediction" class="typing-cursor">|</span>
              </span>
            </div>
          </div>
        </div>

        <div v-if="foodInfo && foodInfo.recipe" class="result-card recipe-card">
          <div class="result-header">
            <div class="result-avatar recipe">
              <i class="bi bi-book"></i>
            </div>
            <div class="result-info">
              <h4 class="result-title">Recipe Guide</h4>
              <span class="result-time">{{ recipeTimestamp }}</span>
            </div>
          </div>

          <div class="result-content">
            <div v-if="displayedFoodName" class="food-name">
              <h2>
                {{ displayedFoodName
                }}<span v-if="isTypingFoodName" class="typing-cursor">|</span>
              </h2>
            </div>

            <div
              v-if="displayedIngredients.length > 0"
              class="ingredients-section"
            >
              <h3 class="section-title">
                <i class="bi bi-list-ul"></i>
                Ingredients
              </h3>
              <div class="ingredients-grid">
                <div
                  v-for="(ingredient, index) in displayedIngredients"
                  :key="'ingredient-' + index"
                  class="ingredient-item"
                >
                  <div class="ingredient-bullet"></div>
                  <span class="ingredient-text">
                    {{ ingredient }}
                    <span
                      v-if="
                        index === displayedIngredients.length - 1 &&
                        isTypingIngredients
                      "
                      class="typing-cursor"
                      >|</span
                    >
                  </span>
                </div>
              </div>
            </div>

            <div v-if="displayedSteps.length > 0" class="steps-section">
              <h3 class="section-title">
                <i class="bi bi-list-check"></i>
                Cooking Steps
              </h3>
              <div class="steps-list">
                <div
                  v-for="(step, index) in displayedSteps"
                  :key="'step-' + index"
                  class="step-item"
                >
                  <div class="step-number">{{ index + 1 }}</div>
                  <div class="step-content">
                    {{ step }}
                    <span
                      v-if="
                        index === displayedSteps.length - 1 && isTypingSteps
                      "
                      class="typing-cursor"
                      >|</span
                    >
                  </div>
                </div>
              </div>
            </div>

            <div class="nutrition-grid">
              <div v-if="displayedCalories" class="nutrition-card calories">
                <div class="nutrition-icon">
                  <i class="bi bi-fire"></i>
                </div>
                <div class="nutrition-info">
                  <span class="nutrition-label">Calories</span>
                  <span class="nutrition-value">
                    {{ displayedCalories }}
                    <span v-if="isTypingCalories" class="typing-cursor">|</span>
                  </span>
                </div>
              </div>

              <div v-if="displayedNutrition" class="nutrition-card health">
                <div class="nutrition-icon">
                  <i class="bi bi-heart-pulse"></i>
                </div>
                <div class="nutrition-info">
                  <span class="nutrition-label">Nutrition</span>
                  <span class="nutrition-value">
                    {{ displayedNutrition }}
                    <span v-if="isTypingNutrition" class="typing-cursor"
                      >|</span
                    >
                  </span>
                </div>
              </div>
            </div>

            <div
              v-if="getYouTubeLink(foodInfo) && displayedNutrition"
              class="tutorial-section"
            >
              <h3 class="section-title">
                <i class="bi bi-play-circle"></i>
                Video Tutorial
              </h3>
              <a
                :href="getYouTubeLink(foodInfo)"
                target="_blank"
                rel="noopener noreferrer"
                class="tutorial-btn"
              >
                <i class="bi bi-youtube"></i>
                Watch Cooking Tutorial
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      imagePreviewUrl: null,
      foodInfo: null,
      predictedFood: null,
      recipeTimestamp: null,
      loading: false,
      error: null,
      isDragOver: false,
      displayedPrediction: "",
      displayedFoodName: "",
      displayedIngredients: [],
      displayedSteps: [],
      displayedCalories: "",
      displayedNutrition: "",
      isTypingPrediction: false,
      isTypingFoodName: false,
      isTypingIngredients: false,
      isTypingSteps: false,
      isTypingCalories: false,
      isTypingNutrition: false,
      typingSpeed: 30,
    };
  },
  methods: {
    triggerFileInput() {
      if (!this.loading) {
        this.$refs.fileInput.click();
      }
    },

    handleDragOver(event) {
      if (!this.loading) {
        this.isDragOver = true;
      }
    },

    handleDragLeave(event) {
      this.isDragOver = false;
    },

    handleDrop(event) {
      this.isDragOver = false;
      if (this.loading) return;

      const files = event.dataTransfer.files;
      if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith("image/")) {
          this.processFile(file);
        }
      }
    },

    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.processFile(file);
      }
    },

    processFile(file) {
      if (this.imagePreviewUrl && this.imagePreviewUrl.startsWith("blob:")) {
        URL.revokeObjectURL(this.imagePreviewUrl);
      }
      this.selectedFile = file;
      this.imagePreviewUrl = URL.createObjectURL(file);
      this.resetDisplayedContent();
      this.error = null;
    },

    removeImage(event) {
      event.stopPropagation();
      if (this.imagePreviewUrl && this.imagePreviewUrl.startsWith("blob:")) {
        URL.revokeObjectURL(this.imagePreviewUrl);
      }
      this.selectedFile = null;
      this.imagePreviewUrl = null;
      this.resetDisplayedContent();
      this.error = null;
      this.$refs.fileInput.value = "";
    },

    resetDisplayedContent() {
      this.foodInfo = null;
      this.predictedFood = null;
      this.recipeTimestamp = null;
      this.displayedPrediction = "";
      this.displayedFoodName = "";
      this.displayedIngredients = [];
      this.displayedSteps = [];
      this.displayedCalories = "";
      this.displayedNutrition = "";
      this.isTypingPrediction = false;
      this.isTypingFoodName = false;
      this.isTypingIngredients = false;
      this.isTypingSteps = false;
      this.isTypingCalories = false;
      this.isTypingNutrition = false;
    },

    async typeText(text, callback, isTypingFlag) {
      this[isTypingFlag] = true;
      for (let i = 0; i <= text.length; i++) {
        callback(text.substring(0, i));
        await new Promise((resolve) => setTimeout(resolve, this.typingSpeed));
      }
      this[isTypingFlag] = false;
    },

    async typeArray(array, displayArray, callback, isTypingFlag) {
      this[isTypingFlag] = true;
      for (let i = 0; i < array.length; i++) {
        displayArray.push("");
        const currentItem = array[i];
        for (let j = 0; j <= currentItem.length; j++) {
          displayArray[i] = currentItem.substring(0, j);
          await new Promise((resolve) => setTimeout(resolve, this.typingSpeed));
        }
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
      this[isTypingFlag] = false;
    },

    async startTypingEffects() {
      if (this.predictedFood) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        await this.typeText(
          this.predictedFood,
          (text) => {
            this.displayedPrediction = text;
          },
          "isTypingPrediction"
        );
      }

      if (this.foodInfo && this.foodInfo.recipe) {
        await new Promise((resolve) => setTimeout(resolve, 800));
        await this.typeText(
          this.foodInfo.food_name,
          (text) => {
            this.displayedFoodName = text;
          },
          "isTypingFoodName"
        );

        await new Promise((resolve) => setTimeout(resolve, 500));
        await this.typeArray(
          this.foodInfo.recipe.ingredients,
          this.displayedIngredients,
          () => {},
          "isTypingIngredients"
        );

        await new Promise((resolve) => setTimeout(resolve, 500));
        await this.typeArray(
          this.foodInfo.recipe.steps,
          this.displayedSteps,
          () => {},
          "isTypingSteps"
        );

        await new Promise((resolve) => setTimeout(resolve, 500));
        await this.typeText(
          this.foodInfo.calories,
          (text) => {
            this.displayedCalories = text;
          },
          "isTypingCalories"
        );

        await new Promise((resolve) => setTimeout(resolve, 500));
        await this.typeText(
          this.foodInfo.nutrition,
          (text) => {
            this.displayedNutrition = text;
          },
          "isTypingNutrition"
        );
      }
    },

    getYouTubeLink(foodInfo) {
      if (!foodInfo) return null;
      return (
        foodInfo.youtube ||
        foodInfo.youtube_tutorial_link ||
        foodInfo.youtubeLink ||
        null
      );
    },

    async uploadImage() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.error = null;
      this.resetDisplayedContent();

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/predict_food_class/",
          {
            method: "POST",
            body: formData,
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(
            errorData.detail || `HTTP error! status: ${response.status}`
          );
        }

        let data = await response.json();

        if (typeof data === "string" && data.includes("food_name")) {
          const cleanedString = data.replace(/^```json\s*|\s*```$/g, "");
          try {
            data = JSON.parse(cleanedString);
          } catch (e) {
            throw new Error("Received malformed JSON string from the server.");
          }
        }

        this.predictedFood = data.predicted_food;
        this.foodInfo = data.llm_info;

        this.recipeTimestamp = new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });

        this.$nextTick(() => {
          this.startTypingEffects();
        });
      } catch (err) {
        this.error = `${err.message}. Please try again or check your connection.`;
        console.error("Error details:", err);
      } finally {
        this.loading = false;
      }
    },
  },
  beforeUnmount() {
    if (this.imagePreviewUrl && this.imagePreviewUrl.startsWith("blob:")) {
      URL.revokeObjectURL(this.imagePreviewUrl);
    }
  },
};
</script>

<style scoped>

@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css");


.food-scanner-container {
  min-height: 100vh;
  background: linear-gradient(145deg, #0f0f23, #1a1a2e, #16213e);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  padding: 0;
  margin: 0;
  overflow-x: hidden;
}

.main-content {
  margin-left: 280px; 
  width: calc(
    100% - 280px
  ); 
  box-sizing: border-box; 

  padding: 32px;
  min-height: 100vh;
}

.header-section {
  margin-bottom: 40px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.header-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent; 
}

.header-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0 0;
  font-weight: 400;
}

.upload-section {
  margin-bottom: 40px;
}

.upload-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.upload-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.upload-zone {
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 48px 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.02);
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.upload-zone::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.upload-zone:hover::before {
  opacity: 1;
}

.upload-zone:hover {
  border-color: rgba(102, 126, 234, 0.6);
  transform: scale(1.02);
}

.upload-zone.drag-over {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  transform: scale(1.05);
}

.upload-zone.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-zone.has-image {
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.2);
  padding: 16px;
}

.upload-content {
  z-index: 1;
  position: relative;
}

.upload-icon {
  font-size: 64px;
  color: rgba(102, 126, 234, 0.8);
  margin-bottom: 24px;
  transition: transform 0.3s ease;
}

.upload-zone:hover .upload-icon {
  transform: scale(1.1);
}

.upload-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
  color: white;
}

.upload-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 24px;
}

.upload-formats {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.format-tag {
  background: rgba(102, 126, 234, 0.2);
  color: rgba(102, 126, 234, 1);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid rgba(102, 126, 234, 0.3);
}


.image-preview-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.image-preview {
  max-width: 100%;
  max-height: 300px;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.btn-remove {
  position: absolute;
  top: -12px;
  right: -12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #ef4444;
  border: 2px solid white;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 18px;
  z-index: 10;
}

.btn-remove:hover {
  background: #dc2626;
  transform: scale(1.1);
}


.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.btn-analyze {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
}

.btn-analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}


.loading-section {
  margin-bottom: 40px;
}

.loading-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 48px 32px;
  text-align: center;
}

.loading-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 32px;
}

.loading-circle {
  width: 80px;
  height: 80px;
  border: 3px solid rgba(102, 126, 234, 0.3);
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  background: rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.5;
  }
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
  color: white;
}

.loading-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
}


.error-section {
  margin-bottom: 40px;
}

.error-card {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.error-icon {
  width: 48px;
  height: 48px;
  background: rgba(239, 68, 68, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #ef4444;
  flex-shrink: 0;
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #f87171;
}

.error-message {
  font-size: 14px;
  color: rgba(239, 68, 68, 0.8);
  margin: 0;
}


.results-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s ease;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.result-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  flex-shrink: 0;
}

.result-avatar.classification {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.result-avatar.recipe {
  background: linear-gradient(135deg, #10b981, #059669);
}

.result-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.result-time {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

/* --- Classification & Recipe Content --- */
.classification-result {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.classification-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.classification-value {
  font-size: 24px;
  font-weight: 700;
  color: #8b9dff;
  min-height: 36px;
}

.food-name h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: white;
  background: linear-gradient(135deg, #a8b5ff, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent; 
  min-height: 48px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 24px;
  margin-top: 32px;
}

.typing-cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
  font-weight: 700;
  color: #667eea;
  margin-left: 2px;
}

@keyframes blink {
  from,
  to {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

.ingredients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.ingredient-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
  min-height: 48px;
}

.ingredient-bullet {
  width: 8px;
  height: 8px;
  background-color: #667eea;
  border-radius: 50%;
  margin-top: 7px;
  flex-shrink: 0;
}

.ingredient-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  line-height: 1.5;
}


.steps-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 20px;
  min-height: 60px;
}
.step-item:last-child {
  border-bottom: none;
}

.step-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #a8b5ff;
  flex-shrink: 0;
}

.step-content {
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.6;
  margin-top: 6px;
}

.nutrition-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 32px;
}

.nutrition-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.nutrition-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.nutrition-card.calories .nutrition-icon {
  background: rgba(255, 159, 64, 0.2);
  color: #ff9f40;
}
.nutrition-card.health .nutrition-icon {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.nutrition-info {
  display: flex;
  flex-direction: column;
}

.nutrition-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
}

.nutrition-value {
  font-size: 18px;
  font-weight: 600;
  color: white;
  min-height: 27px;
}

.tutorial-section {
  margin-top: 32px;
}

.tutorial-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px 24px;
  background-color: #ff0000;
  color: white;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.tutorial-btn i {
  font-size: 20px;
}
.tutorial-btn:hover {
  background-color: #cc0000;
  transform: translateY(-2px);
}

@media (max-width: 1200px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 24px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .header-title {
    font-size: 28px;
  }
  .food-name h2 {
    font-size: 26px;
  }
  .nutrition-grid {
    grid-template-columns: 1fr;
  }
  .upload-card,
  .result-card,
  .loading-card {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 16px;
  }
  .upload-title {
    font-size: 20px;
  }
  .ingredients-grid {
    grid-template-columns: 1fr;
  }
}
</style>
