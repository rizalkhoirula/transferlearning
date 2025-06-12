<template>
  <div class="predictions-container">
    <div class="main-content">
      <div class="header-section">
        <div class="header-content">
          <div class="header-icon">
            <i class="bi bi-graph-up-arrow"></i>
          </div>
          <div class="header-text">
            <h1 class="header-title">Model Performance & Accuracy</h1>
            <p class="header-subtitle">
              Detailed insights into the model's training and validation
              results.
            </p>
          </div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card accuracy-card">
          <div
            class="accuracy-chart"
            role="progressbar"
            aria-valuenow="87"
            aria-valuemin="0"
            aria-valuemax="100"
          >
            <div class="chart-inner">
              <div class="accuracy-value">87%</div>
            </div>
          </div>
          <div class="stat-label">Best Validation Accuracy</div>
          <p class="stat-description">
            The model's ability to correctly identify new, unseen food images.
          </p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <i class="bi bi-clock-history"></i>
          </div>
          <div class="stat-value">218m 29s</div>
          <div class="stat-label">Total Training Time</div>
          <p class="stat-description">
            Time taken for the model to learn from the entire dataset.
          </p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <i class="bi bi-shield-check"></i>
          </div>
          <div class="stat-value">Deployed & Active</div>
          <div class="stat-label">Current Status</div>
          <p class="stat-description">
            The model is currently live and serving predictions.
          </p>
        </div>
      </div>

      <div class="info-card">
        <h2 class="card-title">
          <i class="bi bi-lightbulb-fill"></i> Understanding The Accuracy Score
        </h2>
        <div class="card-body">
          <h3>What does 87% accuracy mean?</h3>
          <p>
            This score indicates that in our standardized tests, the model
            correctly identified the specific Chinese dish in approximately 9
            out of every 10 images it had never seen before. This is a crucial
            metric as it measures the model's generalization capability—its
            performance on real-world data, not just the data it was trained on.
          </p>

          <h3>Is this a good score?</h3>
          <p>
            Yes, for a complex computer vision task like food recognition, an
            accuracy of 87% is an excellent result. Food imagery presents unique
            challenges, including variations in lighting, camera angles, food
            presentation, and subtle differences between similar dishes. This
            score reflects a highly capable model that demonstrates strong
            performance in identifying various dishes.
          </p>

          <h3>Continuous Improvement</h3>
          <p>
            This accuracy score is a snapshot in time. Our goal is to
            continuously enhance the model's performance. Through ongoing
            training with more diverse data, refining the model architecture,
            and applying advanced data augmentation techniques, we aim to push
            this accuracy even higher in future versions.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PredictionsComponent",
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css");

.predictions-container {
  min-height: 100vh;
  background: linear-gradient(145deg, #0f0f23, #1a1a2e, #16213e);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: rgba(36, 39, 68, 0.5);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(36, 39, 68, 0.8);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  font-size: 48px;
  color: #a8b5ff;
  margin-bottom: 16px;
}
.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}
.stat-label {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 12px;
}
.stat-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.5;
  min-height: 42px;
}

.accuracy-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
}
.accuracy-chart {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  margin-bottom: 24px;
  display: grid;
  place-items: center;
  animation: fill-chart 2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
  background: conic-gradient(
    from 0deg,
    #667eea 0%,
    #764ba2 75.6%,
    rgba(255, 255, 255, 0.1) 75.6%,
    rgba(255, 255, 255, 0.1) 100%
  );
}

@keyframes fill-chart {
  from {
    background: conic-gradient(
      from 0deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.1) 100%
    );
  }
}

.chart-inner {
  width: 150px;
  height: 150px;
  background: #1a1a2e;
  border-radius: 50%;
  display: grid;
  place-items: center;
}
.accuracy-value {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #a8b5ff, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.info-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
}
.card-body h3 {
  font-size: 18px;
  font-weight: 600;
  color: #a8b5ff;
  margin-top: 16px;
  margin-bottom: 8px;
}
.card-body p {
  font-size: 16px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 16px;
}

@media (max-width: 1200px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 24px;
  }
}
@media (max-width: 768px) {
  .header-title {
    font-size: 28px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
