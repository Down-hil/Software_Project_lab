<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <el-icon :size="48" color="#409eff"><UserFilled /></el-icon>
        <h2>人事管理系统</h2>
        <p>请输入姓名和密码登录</p>
      </div>
      <el-form
        :model="loginForm"
        :rules="rules"
        ref="loginFormRef"
        label-position="top"
      >
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="loginForm.name"
            placeholder="请输入姓名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            {{ loading ? "登录中..." : "登 录" }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-tip">
        <el-alert
          title="提示：管理员账号 admin / 123456，员工账号可联系管理员创建"
          type="info"
          :closable="false"
          show-icon
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { UserFilled } from "@element-plus/icons-vue";
import { employeeApi } from "@/api";

const router = useRouter();
const loginFormRef = ref(null);
const loading = ref(false);

const loginForm = reactive({
  name: "",
  password: "",
});

const rules = {
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};

const handleLogin = async () => {
  const valid = await loginFormRef.value.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;
  try {
    const res = await employeeApi.login({
      name: loginForm.name,
      password: loginForm.password,
    });
    const user = res.data;
    // 存储用户信息到 sessionStorage
    sessionStorage.setItem("currentUser", JSON.stringify(user));
    ElMessage.success(`欢迎回来，${user.name}！`);

    // 根据角色跳转
    if (user.role === "admin") {
      router.push("/admin");
    } else {
      router.push("/employee");
    }
  } catch (error) {
    ElMessage.error(
      error.response?.data?.detail || "登录失败，请检查姓名和密码"
    );
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 420px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
.login-header {
  text-align: center;
  margin-bottom: 32px;
}
.login-header h2 {
  margin: 12px 0 4px;
  color: #303133;
  font-size: 24px;
}
.login-header p {
  color: #909399;
  font-size: 14px;
}
.login-tip {
  margin-top: 20px;
}
</style>
