<template>
  <div class="employee-container">
    <div class="employee-header">
      <h1>工资条查询</h1>
      <div class="header-right">
        <span class="welcome-text">员工：{{ userName }}</span>
        <el-button type="danger" plain @click="handleLogout">
          退出登录
        </el-button>
      </div>
    </div>

    <div class="wage-content" v-if="employee">
      <div class="employee-info-card">
        <el-descriptions title="个人信息" :column="2" border>
          <el-descriptions-item label="姓名">
            {{ employee.name }}
          </el-descriptions-item>
          <el-descriptions-item label="性别">
            {{ employee.gender || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="职称">
            {{ jobTitle }}
          </el-descriptions-item>
          <el-descriptions-item label="学历">
            {{ employee.education || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ employee.phone || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="电子邮箱">
            {{ employee.email || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="婚姻状况">
            {{ maritalStatus }}
          </el-descriptions-item>
          <el-descriptions-item label="在职状态">
            {{ statusText }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <div class="wage-section">
        <h3>工资条明细</h3>
        <el-table
          :data="wageDetails"
          style="width: 100%; margin-top: 12px"
          stripe
        >
          <el-table-column prop="name" label="项目名称" width="200" />
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <el-tag
                :type="row.type === 'income' ? 'success' : 'danger'"
                size="small"
              >
                {{ row.type === "income" ? "收入" : "扣款" }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="金额(¥)" width="150">
            <template #default="{ row }">
              <span
                :class="
                  row.type === 'income' ? 'income-text' : 'deduction-text'
                "
              >
                ¥{{ row.amount.toLocaleString() }}
              </span>
            </template>
          </el-table-column>
        </el-table>

        <div class="wage-summary">
          <div class="summary-item">
            <span class="summary-label">总收入</span>
            <span class="income-total">
              ¥{{ totalIncome.toLocaleString() }}
            </span>
          </div>
          <div class="summary-item">
            <span class="summary-label">总扣款</span>
            <span class="deduction-total">
              ¥{{ totalDeduction.toLocaleString() }}
            </span>
          </div>
          <div class="summary-item summary-net">
            <span class="summary-label">实发金额</span>
            <strong class="net-amount">
              ¥{{ netSalary.toLocaleString() }}
            </strong>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { employeeApi } from "@/api";

const router = useRouter();
const user = JSON.parse(sessionStorage.getItem("currentUser") || "{}");
const userName = computed(() => user.name || "");

const employee = ref(null);
const loading = ref(true);

// 兼容字段名
const jobTitle = computed(
  () => employee.value?.jobTitle || employee.value?.job_title || "-"
);
const maritalStatus = computed(
  () => employee.value?.maritalStatus || employee.value?.marital_status || "-"
);

const statusText = computed(() => {
  const map = {
    active: "在职",
    resigned: "辞职",
    transfer: "转出",
    retired: "退休",
  };
  return map[employee.value?.status] || employee.value?.status || "-";
});

const wageDetails = computed(() => {
  return employee.value?.wageDetails || employee.value?.wage_details || [];
});

const totalIncome = computed(() =>
  wageDetails.value
    .filter((item) => item.type === "income")
    .reduce((sum, item) => sum + (item.amount || 0), 0)
);

const totalDeduction = computed(() =>
  wageDetails.value
    .filter((item) => item.type === "deduction")
    .reduce((sum, item) => sum + (item.amount || 0), 0)
);

const netSalary = computed(() => totalIncome.value - totalDeduction.value);

const fetchMyWage = async () => {
  try {
    const res = await employeeApi.getMyWage(user.id);
    employee.value = res.data;
  } catch (error) {
    ElMessage.error("获取工资信息失败");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchMyWage);

const handleLogout = () => {
  sessionStorage.removeItem("currentUser");
  router.push("/login");
};
</script>

<style scoped>
.employee-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #f5f7fa;
  box-sizing: border-box;
  overflow-y: auto;
}
.employee-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.employee-header h1 {
  margin: 0;
  font-size: 24px;
  color: #2c3e50;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.welcome-text {
  color: #409eff;
  font-weight: 500;
}
.wage-content {
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}
.employee-info-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.wage-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.wage-section h3 {
  margin: 0 0 8px;
  border-left: 4px solid #409eff;
  padding-left: 12px;
}
.wage-summary {
  background: #f0f9eb;
  padding: 16px 24px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  gap: 32px;
}
.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.summary-label {
  font-size: 13px;
  color: #909399;
}
.income-total {
  color: #67c23a;
  font-weight: bold;
  font-size: 18px;
}
.deduction-total {
  color: #f56c6c;
  font-weight: bold;
  font-size: 18px;
}
.summary-net {
  margin-left: auto;
}
.net-amount {
  font-size: 22px;
  color: #409eff;
}
.income-text {
  color: #67c23a;
  font-weight: 500;
}
.deduction-text {
  color: #f56c6c;
  font-weight: 500;
}
.loading-container {
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
  background: white;
  border-radius: 12px;
  padding: 24px;
}
</style>
