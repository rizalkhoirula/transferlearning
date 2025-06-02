<template>
  <div class="food-container">
    <div class="upload-section">
      <input type="file" @change="onFileChange" accept="image/*" id="fileInput" ref="fileInput" :disabled="loading" />
      <label for="fileInput" class="file-input-label" :class="{ 'disabled': loading }">
        {{ selectedFile ? selectedFile.name : 'Choose an Image' }}
      </label>
      <button @click="uploadImage" :disabled="!selectedFile || loading" class="upload-button">
        Upload & Predict
      </button>
    </div>

    <div v-if="imagePreviewUrl" class="image-preview-container">
      <img :src="imagePreviewUrl" alt="Image Preview" class="image-preview" />
    </div>

    <div v-if="loading" class="loading-spinner-container">
      <div class="loading-spinner"></div>
      <p>Processing your delicious image...</p>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="recipeInfo && !loading" class="chat-message assistant-message">
      <div class="message-header">
        <span class="role-display">Recipe Bot</span>
        <span v-if="recipeTimestamp" class="timestamp">{{ recipeTimestamp }}</span>
      </div>
      <div class="message-content recipe-info">
        <h3>{{ recipeInfo.name }}</h3>
        <p><strong>Predicted Food:</strong> {{ recipeInfo.predicted_food }}</p>
      <h4>Ingredients:</h4>
      <ul>
        <li v-for="(ingredient, index) in recipeInfo.ingredients" :key="'ingredient-' + index">{{ ingredient }}</li>
      </ul>
      <h4>Steps:</h4>
      <ol>
        <li v-for="(step, index) in recipeInfo.steps" :key="'step-' + index">{{ step }}</li>
      </ol>
      <p><strong>Calories:</strong> {{ recipeInfo.calories }}</p>
      <h4>Nutrition:</h4>
      <div v-if="recipeInfo.nutrition">
        <p v-for="(value, key) in recipeInfo.nutrition" :key="key"><strong>{{ key }}:</strong> {{ value }}</p>
      </div>
       <div v-else>
        <p>Nutrition information not available.</p>
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
      recipeInfo: null,
      recipeTimestamp: null, // Added for timestamp
      loading: false,
      error: null,
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.imagePreviewUrl = URL.createObjectURL(file);
        this.recipeInfo = null;
        this.recipeTimestamp = null; // Clear timestamp
        this.error = null;
      } else {
        this.selectedFile = null;
        this.imagePreviewUrl = null;
        this.recipeTimestamp = null; // Clear timestamp
      }
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.error = null;
      // this.recipeInfo = null; // Optionally clear old recipe immediately
      // this.recipeTimestamp = null; 

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        // Replace with your actual API endpoint
        const response = await fetch("/predict_food_class/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ message: "Server error" }));
          throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        this.recipeInfo = this.formatRecipeText(data);
        if (this.recipeInfo) {
          this.recipeTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else {
          this.recipeTimestamp = null;
        }

      } catch (err) {
        this.error = `Error uploading image: ${err.message}`;
        console.error("Error uploading image:", err);
        this.recipeInfo = null; 
        this.recipeTimestamp = null; // Clear timestamp on error
      } finally {
        this.loading = false;
      }
    },
    formatRecipeText(data) {
      if (!data) {
        this.error = "No data received from server.";
        // Ensure timestamp is not set if data is invalid
        this.recipeTimestamp = null; 
        return null;
      }

      const llmInfo = data.llm_info || {};
      const recipe = llmInfo.recipe || {};

      // Basic check to see if we have something to display as a recipe
      if (!recipe.name && !(recipe.ingredients && recipe.ingredients.length > 0) && !llmInfo.calories) {
          this.error = "LLM did not return sufficient recipe information.";
          this.recipeTimestamp = null; 
          return null;
      }

      return {
        predicted_food: data.predicted_food || "Information not available.",
        name: recipe.name || "Recipe name not available.",
        ingredients: recipe.ingredients && recipe.ingredients.length > 0 ? recipe.ingredients : ["Ingredients not available."],
        steps: recipe.steps && recipe.steps.length > 0 ? recipe.steps : ["Steps not available."],
        calories: llmInfo.calories || "Calories information not available.",
        nutrition: llmInfo.nutrition ? this.formatNutrition(llmInfo.nutrition) : null,
      };
    },
    formatNutrition(nutritionData) {
        if (typeof nutritionData === 'string') {
            return { General: nutritionData };
        }
        if (typeof nutritionData === 'object' && nutritionData !== null) {
            const formatted = {};
            for (const key in nutritionData) {
                formatted[key.charAt(0).toUpperCase() + key.slice(1)] = nutritionData[key] || "Not available";
            }
            return formatted;
        }
        return { Information: "Not available" };
    }
  },
  watch: {
    selectedFile(newFile, oldFile) {
      if (oldFile && this.imagePreviewUrl && this.imagePreviewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(this.imagePreviewUrl);
      }
      // If a new file is selected (or deselected), clear previous recipe and timestamp
      if (newFile !== oldFile) {
          this.recipeInfo = null;
          this.recipeTimestamp = null;
      }
    }
  },
  beforeUnmount() {
    if (this.imagePreviewUrl && this.imagePreviewUrl.startsWith('blob:')) {
      URL.revokeObjectURL(this.imagePreviewUrl);
    }
  }
};
</script>

<style scoped>
.food-container {
  max-width: 700px; /* Slightly wider for chat layout */
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 12px;
  font-family: 'Roboto', 'Arial', sans-serif; /* Changed font */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background-color: #f9f9f9; /* Light gray background for the whole container */
}

.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 25px; /* Increased margin */
  padding: 20px;
  background-color: #fff; /* White background for upload section */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

input[type="file"] {
  display: none; 
}

.file-input-label {
  padding: 12px 25px;
  background-color: #5c67f2; /* Primary brand color */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 15px;
  text-align: center;
  display: inline-block;
  min-width: 220px; /* Slightly wider */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.file-input-label:hover {
  background-color: #4a54e0; /* Darker shade on hover */
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.file-input-label.disabled {
  background-color: #b0b0b0; /* Muted color when disabled */
  cursor: not-allowed;
  box-shadow: none;
}

.upload-button {
  padding: 12px 25px;
  background-color: #28a745; /* Green for upload action */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.upload-button:hover {
  background-color: #218838; /* Darker green on hover */
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.upload-button:disabled {
  background-color: #a3d9b1; /* Lighter, muted green when disabled */
  cursor: not-allowed;
  box-shadow: none;
}

.image-preview-container {
  margin-bottom: 25px;
  text-align: center;
}

.image-preview {
  max-width: 100%;
  max-height: 350px; /* Slightly larger preview */
  border-radius: 10px; /* More rounded corners */
  border: 2px solid #ddd; /* More prominent border */
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.loading-spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 25px;
  color: #454545; /* Darker text for loading */
  font-size: 1.1em; /* Slightly larger loading text */
}

.loading-spinner {
  border: 6px solid #e0e0e0; 
  border-top: 6px solid #5c67f2; /* Brand color for spinner */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px; /* Increased margin */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #b71c1c; /* Darker red for error text */
  background-color: #ffcdd2; /* Lighter red background */
  border: 1px solid #ef9a9a; /* Softer red border */
  padding: 12px 18px; /* More padding */
  border-radius: 8px;
  margin-bottom: 25px;
  text-align: center;
  font-weight: 500;
}

/* Chat Message Styling */
.chat-message {
  margin-top: 20px;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.07);
  position: relative;
  max-width: 95%;
}

.assistant-message {
  background-color: #e3f2fd; /* Light blue background for assistant */
  margin-left: auto; /* Align to right if we had user messages on left */
  margin-right: 10px; /* Or centered if it's the only message type */
  /* If we want a tail, it would be more complex CSS with pseudo-elements */
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.role-display {
  font-weight: bold;
  color: #0d47a1; /* Darker blue for role */
  font-size: 0.95em;
}

.timestamp {
  font-size: 0.8em;
  color: #555;
}

.message-content.recipe-info {
  padding: 0; /* Remove padding from original recipe-info if wrapped */
  background-color: transparent; /* Make it inherit chat bubble color */
  border: none; /* Remove original border */
  box-shadow: none; /* Remove original shadow */
  margin-top: 0;
}

.recipe-info h3, .recipe-info h4 {
  color: #1e3a56; /* Darker, more professional color for headings */
  margin-top: 10px;
  margin-bottom: 8px;
}
.recipe-info h3 {
  font-size: 1.4em; /* Slightly adjusted font size */
  border-bottom: 1px solid #bbdefb; /* Light blue underline for main title */
  padding-bottom: 5px;
}
.recipe-info h4 {
  font-size: 1.15em;
}

.recipe-info ul, .recipe-info ol {
  padding-left: 20px;
  list-style-position: outside; /* More standard list appearance */
  margin-bottom: 10px;
}
.recipe-info li {
  margin-bottom: 6px; /* Slightly tighter line spacing */
  line-height: 1.55;
  color: #333; /* Standard text color */
}

/* Responsive adjustments if needed */
@media (max-width: 600px) {
  .food-container {
    margin: 10px;
    padding: 15px;
  }
  .assistant-message {
    margin-right: 5px;
    margin-left: 5px; /* Center on small screens */
  }
}
</style>
