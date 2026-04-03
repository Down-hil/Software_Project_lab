<template>
  <div class="wage-section">
    <h3>工资条 - {{ employee.name }}</h3>
    <div class="wage-custom-tip">
      <el-button size="small" type="success" @click="addWageItem">
        + 自定义工资/奖金/扣款
      </el-button>
      <span style="font-size: 12px; color: #909399; margin-left: 8px">
        可添加奖金、扣款等项目，自定义金额
      </span>
    </div>
    <el-table :data="localWageDetails" style="width: 100%; margin-top: 12px">
      <el-table-column label="项目名称" width="180">
        <template #default="{ row }">
          <el-input v-model="row.name" size="small" />
        </template>
      </el-table-column>
      <el-table-column label="类型" width="100">
        <template #default="{ row }">
          <el-select v-model="row.type" size="small">
            <el-option label="收入" value="income" />
            <el-option label="扣款" value="deduction" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="金额(¥)" width="150">
        <template #default="{ row }">
          <el-input-number
            v-model="row.amount"
            :min="0"
            :step="100"
            size="small"
            controls-position="right"
            style="width: 140px"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="80">
        <template #default="{ $index }">
          <el-button link type="danger" @click="removeWageItem($index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="wage-summary">
      <div>
        总收入: <span class="income-total">¥{{ totalIncome }}</span>
      </div>
      <div>
        总扣款: <span class="deduction-total">¥{{ totalDeduction }}</span>
      </div>
      <div>
        实发金额: <strong>¥{{ netSalary }}</strong>
      </div>
    </div>
    <div class="wage-note">
      注：自定义工资项后自动保存，员工可在此查看个人工资条
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  employee: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:employee"]);

// 本地工资明细，避免直接修改 prop
const localWageDetails = ref([...props.employee.wageDetails]);

// 监听本地工资明细的变化，同步到父组件
watch(
  localWageDetails,
  (newDetails) => {
    const updatedEmployee = {
      ...props.employee,
      wageDetails: newDetails,
    };
    emit("update:employee", updatedEmployee);
  },
  { deep: true }
);

// 当外部 employee 变化时，同步本地明细
watch(
  () => props.employee,
  (newEmployee) => {
    localWageDetails.value = [...newEmployee.wageDetails];
  },
  { deep: true }
);

// 添加新工资项
const addWageItem = () => {
  localWageDetails.value.push({
    id: Date.now(),
    name: "新项目",
    type: "income",
    amount: 0,
  });
};

// 删除工资项
const removeWageItem = (index) => {
  localWageDetails.value.splice(index, 1);
};

// 汇总计算
const totalIncome = computed(() =>
  localWageDetails.value
    .filter((item) => item.type === "income")
    .reduce((sum, item) => sum + (item.amount || 0), 0)
);

const totalDeduction = computed(() =>
  localWageDetails.value
    .filter((item) => item.type === "deduction")
    .reduce((sum, item) => sum + (item.amount || 0), 0)
);

const netSalary = computed(() => totalIncome.value - totalDeduction.value);
</script>

<style scoped>
.wage-section {
  margin-bottom: 28px;
}
.wage-section h3 {
  margin-top: 0;
  border-left: 4px solid #409eff;
  padding-left: 12px;
}
.wage-custom-tip {
  display: flex;
  align-items: center;
  margin: 12px 0;
}
.wage-summary {
  background: #f0f9eb;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 16px;
  display: flex;
  gap: 24px;
  font-size: 16px;
}
.income-total {
  color: #67c23a;
  font-weight: bold;
}
.deduction-total {
  color: #f56c6c;
  font-weight: bold;
}
.wage-note {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
  text-align: right;
}
</style>
