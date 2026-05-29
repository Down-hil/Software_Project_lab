import { createRouter, createWebHashHistory } from "vue-router";
import Login from "@/views/userLogin.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import EmployeeDashboard from "@/views/EmployeeDashboard.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/employee",
    name: "EmployeeDashboard",
    component: EmployeeDashboard,
    meta: { requiresAuth: true, role: "employee" },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 路由守卫：检查登录状态和角色
router.beforeEach((to, from, next) => {
  const user = sessionStorage.getItem("currentUser");
  const userData = user ? JSON.parse(user) : null;

  if (to.meta.requiresAuth) {
    if (!userData) {
      // 未登录，跳转登录页
      next("/login");
    } else if (to.meta.role && to.meta.role !== userData.role) {
      // 角色不匹配，跳转到对应页面
      if (userData.role === "admin") {
        next("/admin");
      } else {
        next("/employee");
      }
    } else {
      next();
    }
  } else {
    // 已登录用户访问登录页则跳转到对应主页
    if (userData && to.path === "/login") {
      if (userData.role === "admin") {
        next("/admin");
      } else {
        next("/employee");
      }
    } else {
      next();
    }
  }
});

export default router;
