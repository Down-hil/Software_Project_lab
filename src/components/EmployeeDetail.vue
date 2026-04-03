<template>
  <div class="detail-section">
    <h3>员工信息编辑</h3>
    <el-form :model="localEmployee" label-width="90px" label-position="left">
      <el-divider content-position="left">基本信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="姓名">
            <el-input v-model="localEmployee.name" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="性别">
            <el-select v-model="localEmployee.gender">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出生日期">
            <el-date-picker
              v-model="localEmployee.birthday"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系电话">
            <el-input v-model="localEmployee.phone" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="电子邮箱">
            <el-input v-model="localEmployee.email" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">学历信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="8">
          <el-form-item label="学历">
            <el-input v-model="localEmployee.education" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="毕业院校">
            <el-input v-model="localEmployee.school" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="专业">
            <el-input v-model="localEmployee.major" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">其他信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="婚姻状况">
            <el-select v-model="localEmployee.maritalStatus">
              <el-option label="未婚" value="未婚" />
              <el-option label="已婚" value="已婚" />
              <el-option label="离异" value="离异" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="职称">
            <el-input v-model="localEmployee.jobTitle" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="在职状态">
            <el-select v-model="localEmployee.status">
              <el-option label="在职" value="active" />
              <el-option label="辞职" value="resigned" />
              <el-option label="转出" value="transfer" />
              <el-option label="退休" value="retired" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" @click="save"> 保存修改 </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  employee: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:employee", "save"]);

// 使用 reactive 创建本地副本，避免直接修改 prop
const localEmployee = reactive({ ...props.employee });

// 当外部传入的 employee 变化时，同步本地副本
watch(
  () => props.employee,
  (newVal) => {
    Object.assign(localEmployee, newVal);
  },
  { deep: true }
);

// 保存修改，将更新后的员工对象传递给父组件
const save = () => {
  emit("update:employee", { ...localEmployee });
  emit("save"); // 可选，用于提示保存成功
};
</script>

<style scoped>
.detail-section {
  margin-bottom: 28px;
}
.el-divider {
  margin: 16px 0;
}
</style>
