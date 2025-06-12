<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="logo-container">
        <div class="logo-icon">
          <i class="bi bi-shop"></i>
        </div>
        <div class="logo-text">
          <span class="brand-name">AI Tools</span>
          <span class="brand-subtitle">Studio</span>
        </div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li class="nav-item">
          <router-link to="/" class="nav-link" active-class="active">
            <div class="nav-icon">
              <i class="bi bi-house-door-fill"></i>
            </div>
            <span class="nav-text">Dashboard</span>
            <div class="nav-indicator"></div>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/food" class="nav-link" active-class="active">
            <div class="nav-icon">
              <i class="bi bi-camera-fill"></i>
            </div>
            <span class="nav-text">Food Scanner</span>
            <div class="nav-indicator"></div>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/live-chat" class="nav-link" active-class="active">
            <div class="nav-icon">
              <i class="bi bi-chat"></i>
            </div>
            <span class="nav-text">Live Chat</span>
            <div class="nav-indicator"></div>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/detail" class="nav-link" active-class="active">
            <div class="nav-icon">
              <i class="bi bi-card-list"></i>
            </div>
            <span class="nav-text">Details</span>
            <div class="nav-indicator"></div>
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <div class="version-info">
        <div class="status-dot"></div>
        <span class="version-text">v1.0.2</span>
      </div>
      <div class="author-info">
        <span class="author-name">Rizal 柯瑞安</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background: linear-gradient(145deg, #0f0f23, #1a1a2e, #16213e);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo-icon:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
}

.logo-icon i {
  font-size: 24px;
  color: white;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.brand-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 4px;
  padding: 0 16px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  gap: 14px;
}

.nav-link::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -1;
}

.nav-link:hover::before {
  width: 100%;
}

.nav-link:hover {
  color: white;
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: white;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.2),
    rgba(118, 75, 162, 0.2)
  );
  border: 1px solid rgba(102, 126, 234, 0.3);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.nav-link.active::before {
  width: 100%;
}

.nav-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover .nav-icon {
  transform: scale(1.1);
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  flex: 1;
}

.nav-indicator {
  width: 6px;
  height: 6px;
  background: transparent;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link.active .nav-indicator {
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.6);
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
}

.version-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.version-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.author-info {
  margin-top: 4px;
}

.author-name {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 400;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
