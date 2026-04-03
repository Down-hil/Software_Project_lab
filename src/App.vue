<template>
  <div class="hr-container">
    <div class="header">
      <h1>人事管理系统</h1>
      <el-button type="primary" @click="addDialogVisible = true">
        + 新增员工
      </el-button>
    </div>

    <div class="main-layout">
      <EmployeeList
        :employees="employees"
        v-model:statusFilter="statusFilter"
        v-model:searchKeyword="searchKeyword"
        @select="handleSelectEmployee"
        @edit="selectAndEdit"
        @status-change="handleStatusChange"
      />

      <div v-if="selectedEmployee" class="employee-detail">
        <EmployeeDetail
          :employee="selectedEmployee"
          @update:employee="updateSelectedEmployee"
          @save="saveEmployeeInfo"
        />
        <WageSection
          :employee="selectedEmployee"
          @update:employee="updateSelectedEmployee"
        />
      </div>
      <div v-else class="empty-detail">
        <el-empty description="请从左侧选择员工以查看详情和工资条" />
      </div>
    </div>

    <AddEmployeeDialog v-model="addDialogVisible" @add="addEmployee" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import EmployeeList from "./components/EmployeeList.vue";
import EmployeeDetail from "./components/EmployeeDetail.vue";
import WageSection from "./components/WageSection.vue";
import AddEmployeeDialog from "./components/AddEmployeeDialog.vue";
import { getStatusText } from "./utils/helpers";

// ---------- 模拟数据 ----------
const employees = ref([
  {
    id: 1,
    name: "张敏",
    gender: "女",
    birthday: "1990-05-12",
    phone: "13812345678",
    email: "zhangmin@company.com",
    education: "本科",
    school: "复旦大学",
    major: "计算机科学与技术",
    maritalStatus: "已婚",
    jobTitle: "高级工程师",
    status: "active",
    wageDetails: [
      { id: 101, name: "基本工资", type: "income", amount: 12000 },
      { id: 102, name: "项目奖金", type: "income", amount: 3500 },
      { id: 103, name: "全勤奖", type: "income", amount: 500 },
      { id: 104, name: "公积金扣款", type: "deduction", amount: 1500 },
      { id: 105, name: "迟到扣款", type: "deduction", amount: 200 },
    ],
  },
  {
    id: 2,
    name: "李强",
    gender: "男",
    birthday: "1985-08-23",
    phone: "13987654321",
    email: "liqiang@company.com",
    education: "硕士",
    school: "清华大学",
    major: "工商管理",
    maritalStatus: "已婚",
    jobTitle: "市场总监",
    status: "active",
    wageDetails: [
      { id: 201, name: "基本工资", type: "income", amount: 15000 },
      { id: 202, name: "季度奖金", type: "income", amount: 8000 },
      { id: 203, name: "交通补贴", type: "income", amount: 800 },
      { id: 204, name: "个人所得税", type: "deduction", amount: 2200 },
    ],
  },
  {
    id: 3,
    name: "王芳",
    gender: "女",
    birthday: "1992-11-02",
    phone: "15233445566",
    email: "wangfang@company.com",
    education: "本科",
    school: "浙江大学",
    major: "设计学",
    maritalStatus: "未婚",
    jobTitle: "UI设计师",
    status: "resigned",
    wageDetails: [
      { id: 301, name: "基本工资", type: "income", amount: 8000 },
      { id: 302, name: "绩效奖金", type: "income", amount: 2000 },
      { id: 303, name: "社保扣款", type: "deduction", amount: 800 },
      { id: 304, name: "餐补", type: "income", amount: 300 },
    ],
  },
]);

// 筛选与选中
const statusFilter = ref("active");
const searchKeyword = ref("");
const selectedEmployee = ref(null);
const addDialogVisible = ref(false);

// 事件处理
const handleSelectEmployee = (row) => {
  selectedEmployee.value = row;
};
const selectAndEdit = (row) => {
  selectedEmployee.value = row;
};

const updateSelectedEmployee = (updatedEmployee) => {
  const index = employees.value.findIndex(
    (emp) => emp.id === updatedEmployee.id
  );
  if (index !== -1) {
    employees.value[index] = updatedEmployee;
  }
  // 同步当前选中的员工对象
  if (selectedEmployee.value?.id === updatedEmployee.id) {
    selectedEmployee.value = updatedEmployee;
  }
};

const saveEmployeeInfo = () => {
  ElMessage.success("员工信息已更新");
};

const handleStatusChange = (row, command) => {
  row.status = command;
  const idx = employees.value.findIndex((emp) => emp.id === row.id);
  if (idx !== -1) employees.value[idx].status = command;
  ElMessage.success(`已将 ${row.name} 状态更改为 ${getStatusText(command)}`);
  if (
    statusFilter.value === "active" &&
    command !== "active" &&
    selectedEmployee.value?.id === row.id
  ) {
    selectedEmployee.value = null;
  }
};

const addEmployee = (newEmployee) => {
  employees.value.push(newEmployee);
  if (statusFilter.value === "active") {
    selectedEmployee.value = newEmployee;
  }
};
</script>

<style scoped>
.hr-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #f5f7fa;
  box-sizing: border-box;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.header h1 {
  margin: 0;
  font-size: 24px;
  color: #2c3e50;
}
.main-layout {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0;
  overflow: hidden;
}
.employee-detail {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 20px;
  overflow-y: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.empty-detail {
  flex: 1;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
