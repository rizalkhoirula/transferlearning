<template>
  <div class="dashboard-container">
    <div class="main-content">
      <div class="header-section">
        <div class="header-content">
          <div class="header-icon">
            <i class="bi bi-cpu-fill"></i>
          </div>
          <div class="header-text">
            <h1 class="header-title">Chinese Food Recognition</h1>
            <p class="header-subtitle">
              An AI-Powered Culinary Exploration Dashboard
            </p>
          </div>
        </div>
      </div>

      <div class="info-card overview-card">
        <h2 class="card-title">
          <i class="bi bi-card-text"></i> Project Overview
        </h2>
        <p class="card-body">
          Welcome to the Chinese Food Recognition project dashboard. This
          platform leverages the power of artificial intelligence (AI) and
          computer vision to identify a wide variety of Chinese dishes from an
          image. By simply uploading a photo of a meal, our deep learning model
          will analyze and recognize the dish's name, then present relevant
          information such as recipes, ingredients, and nutritional data.
        </p>
        <p class="card-body">
          The goal is to bridge the gap between the visual enjoyment of cuisine
          and the knowledge behind it, making food exploration easier, more
          interactive, and informative for everyone.
        </p>
      </div>

      <div class="features-section">
        <h2 class="section-title">
          <i class="bi bi-star-fill"></i> Key Features
        </h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-bullseye"></i>
            </div>
            <div class="feature-text">
              <h3>High-Accuracy Recognition</h3>
              <p>
                The AI model is trained on thousands of images from hundreds of
                Chinese cuisine categories to ensure accurate identification.
              </p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-book-half"></i>
            </div>
            <div class="feature-text">
              <h3>Instant Recipe Generation</h3>
              <p>
                Once a food is recognized, the system automatically generates a
                complete recipe with detailed cooking steps.
              </p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-heart-pulse-fill"></i>
            </div>
            <div class="feature-text">
              <h3>Nutrition Information</h3>
              <p>
                Get estimated nutritional information, including calorie counts,
                to help you make healthier food choices.
              </p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-palette-fill"></i>
            </div>
            <div class="feature-text">
              <h3>Modern & Dynamic UI</h3>
              <p>
                The elegant and responsive interface is designed to provide a
                seamless and enjoyable user experience.
              </p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-camera-video-fill"></i>
            </div>
            <div class="feature-text">
              <h3>Real-Time Food Scanning</h3>
              <p>
                The system supports real-time scanning, providing instant
                identification and details as you capture food images.
              </p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="bi bi-chat-square-quote-fill"></i>
            </div>
            <div class="feature-text">
              <h3>Live Chat with AI</h3>
              <p>
                Have a question about a recipe or want cooking tips? Chat
                directly with our AI to get instant answers and culinary
                suggestions!
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="cta-section">
        <router-link to="/food" class="cta-button">
          <i class="bi bi-camera-fill"></i>
          Try the Food Scanner Now!
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardComponent",
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css");

.dashboard-container {
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
  width: calc(100% - 280px);
  box-sizing: border-box;
  padding: 32px;
  min-height: 100vh;
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
  flex-shrink: 0;
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

.info-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 40px;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-body {
  font-size: 16px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 16px;
}

.card-body:last-child {
  margin-bottom: 0;
}

.features-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.feature-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px) scale(1.02);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
}

.feature-icon {
  font-size: 32px;
  color: rgba(255, 255, 255, 0.8);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  padding: 16px;
}

.feature-text h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: rgba(255, 255, 255, 0.9);
}

.feature-text p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
}

.cta-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.cta-button {
  padding: 16px 32px;
  font-size: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 30px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  transition: background 0.3s ease;
}

.cta-button:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  box-shadow: 0 8px 32px rgba(118, 75, 162, 0.3);
}

.cta-button i {
  font-size: 24px;
}
</style>
