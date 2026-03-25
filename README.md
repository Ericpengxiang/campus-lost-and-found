# 校园失物招领与寻物匹配系统

基于 **Django + Python** 后端 + **Vue 3** 前端的校园失物招领平台。

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | Django 4.x + Django REST Framework |
| 身份认证 | JWT（djangorestframework-simplejwt） |
| 数据库 | SQLite（开发）/ MySQL（生产） |
| 前端框架 | Vue 3 (Composition API) + Vite |
| UI 组件库 | Element Plus |
| 状态管理 | Pinia |
| 路由 | Vue Router 4 |
| HTTP 客户端 | Axios |
| 智能匹配 | LLM API（内置 Forge API） |

---

## 项目结构

```
campus_laf/
├── manage.py
├── backend/              # Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                # 用户模块
│   ├── models.py         # 自定义 User 模型
│   ├── serializers.py
│   ├── views.py          # 注册、登录、个人信息、管理员用户管理
│   └── urls.py
├── items/                # 物品模块（失物招领 + 寻物启事）
│   ├── models.py         # Item、ItemImage、Message 模型
│   ├── serializers.py
│   ├── views.py          # 物品 CRUD、图片上传、留言、管理员内容管理
│   └── urls.py
├── matches/              # 匹配模块
│   ├── models.py         # Match 模型
│   ├── serializers.py
│   ├── views.py          # 智能匹配触发、匹配列表
│   └── urls.py
└── frontend/             # Vue 3 前端
    ├── src/
    │   ├── views/        # 页面组件
    │   │   ├── HomeView.vue          # 首页
    │   │   ├── ItemListView.vue      # 失物招领/寻物启事列表
    │   │   ├── ItemDetailView.vue    # 物品详情
    │   │   ├── PublishView.vue       # 发布表单
    │   │   ├── SearchView.vue        # 搜索页
    │   │   ├── LoginView.vue         # 登录
    │   │   ├── RegisterView.vue      # 注册
    │   │   ├── ProfileView.vue       # 个人中心
    │   │   └── AdminView.vue         # 管理员后台
    │   ├── components/
    │   │   ├── AppNavbar.vue         # 导航栏
    │   │   ├── AppFooter.vue         # 页脚
    │   │   └── ItemCard.vue          # 物品卡片
    │   ├── stores/auth.js            # Pinia 认证状态
    │   ├── router/index.js           # Vue Router 路由配置
    │   ├── api/index.js              # Axios API 封装
    │   └── assets/main.css           # 全局样式
    ├── package.json
    └── vite.config.js
```

---

## 功能模块

### 用户模块
- 注册（用户名、密码、邮箱、身份类型、院系）
- 登录 / 登出（JWT Token）
- 个人中心（查看/编辑个人信息、头像上传）
- 我的发布（失物招领 + 寻物启事列表、编辑、删除）
- 我的匹配（查看匹配记录）

### 失物招领模块
- 发布捡到的物品（标题、分类、拾取时间、拾取地点、详细描述、图片、联系方式）
- 物品列表（分页、分类筛选、关键词搜索）
- 物品详情（图片轮播、发布者信息、留言区）
- 编辑 / 删除（仅发布者）
- 状态管理（进行中 / 已匹配 / 已关闭）

### 寻物启事模块
- 发布丢失的物品（标题、分类、丢失时间、丢失地点、详细描述、图片、联系方式）
- 物品列表（分页、分类筛选、关键词搜索）
- 物品详情（图片轮播、发布者信息、留言区）
- 编辑 / 删除（仅发布者）

### 智能匹配模块
- 在物品详情页触发 AI 智能匹配
- LLM 分析物品描述、分类、地点、时间等信息
- 返回匹配候选列表（含匹配度分数和匹配理由）
- 支持确认匹配 / 拒绝匹配

### 管理员后台
- 数据概览（注册用户数、失物招领数、寻物启事数、成功匹配数、分类统计、状态分布）
- 内容管理（查看所有物品、按类型/状态/关键词筛选、修改状态、删除）
- 用户管理（查看所有用户、搜索、禁用/启用账号）
- 匹配记录（查看所有匹配记录及状态）

---

## 快速启动

### 后端

```bash
# 1. 安装依赖
pip install django djangorestframework djangorestframework-simplejwt \
            django-cors-headers Pillow

# 2. 数据库迁移
cd campus_laf
python manage.py migrate

# 3. 创建超级管理员
python manage.py createsuperuser

# 4. 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 前端

```bash
cd campus_laf/frontend

# 1. 安装依赖
pnpm install   # 或 npm install

# 2. 启动开发服务器（代理到后端 8000 端口）
pnpm dev

# 3. 生产构建
pnpm build
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端（开发） | http://localhost:5173 |
| 后端 API | http://localhost:8000/api/ |
| Django 管理后台 | http://localhost:8000/admin/ |

---

## API 接口一览

### 用户接口 `/api/users/`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/register/` | 注册 |
| POST | `/login/` | 登录（返回 JWT） |
| POST | `/token/refresh/` | 刷新 Token |
| GET/PATCH | `/me/` | 获取/更新个人信息 |
| GET | `/me/unread/` | 未读消息数 |
| GET | `/admin/list/` | 管理员：用户列表 |
| PATCH/DELETE | `/admin/<id>/` | 管理员：用户操作 |

### 物品接口 `/api/items/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 物品列表（支持 type/category/status/keyword 筛选） |
| POST | `/create/` | 发布物品 |
| GET | `/<id>/` | 物品详情 |
| PATCH | `/<id>/edit/` | 编辑物品 |
| DELETE | `/<id>/delete/` | 删除物品 |
| GET | `/<id>/messages/` | 获取留言 |
| POST | `/<id>/messages/` | 发布留言 |
| GET | `/admin/stats/` | 管理员：统计数据 |

### 匹配接口 `/api/matches/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/item/<item_id>/` | 获取物品的匹配结果 |
| POST | `/run/<item_id>/` | 触发 AI 智能匹配 |
| POST | `/<match_id>/confirm/` | 确认匹配 |
| POST | `/<match_id>/reject/` | 拒绝匹配 |
| GET | `/admin/list/` | 管理员：所有匹配记录 |

---

## 物品分类

| 分类 | 说明 |
|------|------|
| `id_card` | 证件（学生证、身份证、校园卡等） |
| `electronics` | 电子产品（手机、电脑、耳机等） |
| `books` | 书籍文具（教材、笔记本、文具等） |
| `keys` | 钥匙 |
| `wallet` | 钱包 |
| `clothing` | 衣物 |
| `other` | 其他 |

---

## 默认管理员账号

```
用户名：admin
密码：admin123456
```

> 生产环境请务必修改默认密码。
