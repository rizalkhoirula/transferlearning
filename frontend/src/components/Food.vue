<script setup>
import { ref } from "vue";

const selectedFile = ref(null);
const loading = ref(false);

const chatMessages = ref([]);

function onFileChange(event) {
  selectedFile.value = event.target.files[0];
}

async function uploadImage() {
  if (!selectedFile.value) return;
  loading.value = true;
  chatMessages.value = [];

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const res = await fetch("http://localhost:8000/predict_food_class/", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`Error: ${err.detail || "Unknown error"}`);
      loading.value = false;
      return;
    }

    const data = await res.json();

    const recipeInfo = data?.llm_info?.recipe;
    if (recipeInfo) {
      const recipeText = formatRecipeText(recipeInfo);
      addChatMessage("LLM", recipeText);
    } else {
      addChatMessage("LLM", "No recipe info available.");
    }
  } catch (e) {
    alert(`Failed to upload: ${e.message}`);
  } finally {
    loading.value = false;
  }
}

function formatRecipeText(llmInfo) {
  const recipe = llmInfo?.recipe;
  const nutrition = llmInfo?.nutrition;
  const calories = llmInfo?.calories;

  const name = recipe?.name ? `🍽️ Recipe: ${recipe.name}\n` : "";

  const ingredients = Array.isArray(recipe?.ingredients)
    ? `\n🧂 ingredients:\n- ${recipe.ingredients.join("\n- ")}\n`
    : "";

  const steps = Array.isArray(recipe?.steps)
    ? `\n👨‍🍳 Steps:\n${recipe.steps
        .map((step, i) => `${i + 1}. ${step}`)
        .join("\n")}\n`
    : "";

  const cal = calories ? `\n🔥 Calories: ${calories}\n` : "";

  const nutriDetails = nutrition
    ? `\n🧪 nutrition:\n- Protein: ${nutrition.protein}\n- Karbohidrat: ${nutrition.carbohydrates}\n- Lemak: ${nutrition.fat}\n- Serat: ${nutrition.fiber}\n- Vitamin: ${nutrition.vitamins}\n- Mineral: ${nutrition.minerals}`
    : "";

  const finalText = `${name}${ingredients}${steps}${cal}${nutriDetails}`.trim();

  return finalText || "Informasi resep tidak tersedia.";
}

function addChatMessage(role, text) {
  const message = {
    role,
    text,
    displayText: "",
  };
  chatMessages.value.push(message);
  typeText(message);
}

async function typeText(message) {
  const words = message.text.split(" ");
  for (let i = 0; i < words.length; i++) {
    if (message.displayText.length > 0) {
      message.displayText += " ";
    }
    message.displayText += words[i];
    await new Promise((r) => setTimeout(r, 20)); // optional: percepat animasi
  }
}
</script>
<template>
  <div class="container mx-auto p-4 max-w-md">
    <h1 class="text-2xl font-bold mb-4">Padang Food Classifier</h1>

    <!-- Upload Image -->
    <input type="file" accept="image/*" @change="onFileChange" class="mb-4" />
    <button
      :disabled="!selectedFile || loading"
      @click="uploadImage"
      class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
    >
      {{ loading ? "Processing..." : "Upload & Predict" }}
    </button>

    <!-- Chatbox -->
    <div
      v-if="chatMessages.length"
      class="mt-6 bg-gray-100 p-4 rounded shadow max-h-80 overflow-y-auto"
    >
      <div v-for="(msg, index) in chatMessages" :key="index" class="mb-3">
        <div class="font-semibold text-blue-700 mb-1">{{ msg.role }}</div>
        <div class="whitespace-pre-wrap text-gray-800">
          {{ msg.displayText }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
</style>
