<template>
  <div class="hr-container">
    <div class="header">
      <h1>人事管理系统</h1>
      <div class="header-right">
        <span class="welcome-text">管理员：{{ userName }}</span>
        <el-button type="primary" @click="addDialogVisible = true">
          + 新增员工
        </el-button>
        <el-button type="danger" plain @click="handleLogout">
          退出登录
        </el-button>
      </div>
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
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { employeeApi } from "@/api";
import { getStatusText } from "@/utils/helpers";

import EmployeeList from "@/components/EmployeeList.vue";
import EmployeeDetail from "@/components/EmployeeDetail.vue";
import WageSection from "@/components/WageSection.vue";
import AddEmployeeDialog from "@/components/AddEmployeeDialog.vue";
import { watch } from "vue";

const router = useRouter();

const user = JSON.parse(sessionStorage.getItem("currentUser") || "{}");
const userName = computed(() => user.name || "");

// ---------- 数据 ----------
const employees = ref([]);

// 筛选与选中
const statusFilter = ref("active");
const searchKeyword = ref("");
const selectedEmployee = ref(null);
const addDialogVisible = ref(false);

const handleSelectEmployee = (row) => {
  selectedEmployee.value = row;
};

const selectAndEdit = (row) => {
  selectedEmployee.value = row;
};

const mapEmployeeData = (employee) => {
  return {
    ...employee,
    maritalStatus: employee.maritalStatus || employee.marital_status || "",
    jobTitle: employee.jobTitle || employee.job_title || "",
    wageDetails: employee.wageDetails || employee.wage_details || [],
  };
};

// 加载员工列表
const fetchEmployees = async () => {
  try {
    const params = {};
    if (statusFilter.value !== "all") params.status = statusFilter.value;
    if (searchKeyword.value) params.search = searchKeyword.value;
    const res = await employeeApi.getEmployees(params);
    employees.value = res.data.map(mapEmployeeData);
  } catch (error) {
    ElMessage.error("获取员工列表失败");
  }
};

watch([statusFilter, searchKeyword], () => {
  fetchEmployees();
});

onMounted(fetchEmployees);

// 新增员工
const addEmployee = async (newEmployee) => {
  try {
    const res = await employeeApi.createEmployee(newEmployee);
    employees.value.push(mapEmployeeData(res.data));
    if (statusFilter.value === "active" || statusFilter.value === "all") {
      selectedEmployee.value = res.data;
    }
    ElMessage.success(`员工 ${newEmployee.name} 添加成功`);
  } catch (error) {
    ElMessage.error("添加失败");
  }
};

// 更新员工
const updateSelectedEmployee = async (updatedEmployee) => {
  try {
    const res = await employeeApi.updateEmployee(
      updatedEmployee.id,
      updatedEmployee
    );
    const index = employees.value.findIndex(
      (emp) => emp.id === updatedEmployee.id
    );
    const mappedEmployee = mapEmployeeData(res.data);
    if (index !== -1) employees.value[index] = mappedEmployee;
    if (selectedEmployee.value?.id === updatedEmployee.id) {
      selectedEmployee.value = mappedEmployee;
    }
    ElMessage.success("员工信息已更新");
  } catch (error) {
    ElMessage.error("更新失败");
  }
};

// 更改状态
const handleStatusChange = async (row, command) => {
  try {
    await employeeApi.patchEmployeeStatus(row.id, command);
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
  } catch (error) {
    ElMessage.error("状态更新失败");
  }
};

// 退出登录
const handleLogout = () => {
  sessionStorage.removeItem("currentUser");
  router.push("/login");
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
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.welcome-text {
  color: #409eff;
  font-weight: 500;
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
