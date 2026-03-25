<template>
  <footer class="footer">
    <div class="page-container">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">🎒 校园失物招领平台</div>
          <p class="footer-desc">帮助校园师生找回丢失物品，传递温暖与善意</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>快速入口</h4>
            <router-link to="/found">失物招领</router-link>
            <router-link to="/lost">寻物启事</router-link>
            <router-link to="/publish">发布信息</router-link>
          </div>
          <div class="footer-col">
            <h4>帮助中心</h4>
            <a href="#">使用指南</a>
            <a href="#">隐私政策</a>
            <a href="#">联系我们</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2024 校园失物招领平台 · 基于 Django + Vue 3 构建</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer { background: #1e293b; color: rgba(255,255,255,.7); padding: 48px 0 24px; margin-top: 80px; }
.footer-inner { display: flex; justify-content: space-between; gap: 48px; margin-bottom: 32px; }
.footer-brand { max-width: 280px; }
.footer-logo { font-size: 18px; font-weight: 700; color: white; margin-bottom: 12px; }
.footer-desc { font-size: 14px; line-height: 1.6; }
.footer-links { display: flex; gap: 48px; }
.footer-col { display: flex; flex-direction: column; gap: 10px; }
.footer-col h4 { font-size: 14px; font-weight: 600; color: white; margin-bottom: 4px; }
.footer-col a { font-size: 13px; color: rgba(255,255,255,.6); text-decoration: none; transition: color .15s; }
.footer-col a:hover { color: white; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,.1); padding-top: 20px; text-align: center; font-size: 13px; }
@media (max-width: 768px) { .footer-inner { flex-direction: column; } .footer-links { flex-direction: column; gap: 24px; } }
</style>
