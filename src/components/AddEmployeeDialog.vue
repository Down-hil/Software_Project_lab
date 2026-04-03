<template>
  <el-dialog v-model="dialogVisible" title="新增员工" width="700px">
    <el-form :model="formData" label-width="100px" ref="formRef">
      <el-divider content-position="left">基本信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="formData.name" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="性别">
            <el-select v-model="formData.gender">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出生日期">
            <el-date-picker
              v-model="formData.birthday"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系电话">
            <el-input v-model="formData.phone" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="电子邮箱">
            <el-input v-model="formData.email" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">学历信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="8">
          <el-form-item label="学历">
            <el-input v-model="formData.education" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="毕业院校">
            <el-input v-model="formData.school" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="专业">
            <el-input v-model="formData.major" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">其他信息</el-divider>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="婚姻状况">
            <el-select v-model="formData.maritalStatus">
              <el-option label="未婚" value="未婚" />
              <el-option label="已婚" value="已婚" />
              <el-option label="离异" value="离异" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="职称">
            <el-input v-model="formData.jobTitle" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmAdd">确定添加</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, reactive } from "vue";
import { ElMessage } from "element-plus";
import { generateDefaultWage } from "@/utils/helpers";

const props = defineProps({
  modelValue: Boolean,
});
const emit = defineEmits(["update:modelValue", "add"]);

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const formData = reactive({
  name: "",
  gender: "男",
  birthday: "",
  phone: "",
  email: "",
  education: "",
  school: "",
  major: "",
  maritalStatus: "未婚",
  jobTitle: "",
});

const resetForm = () => {
  Object.assign(formData, {
    name: "",
    gender: "男",
    birthday: "",
    phone: "",
    email: "",
    education: "",
    school: "",
    major: "",
    maritalStatus: "未婚",
    jobTitle: "",
  });
};

const confirmAdd = () => {
  if (!formData.name) {
    ElMessage.warning("请输入员工姓名");
    return;
  }
  const newId = Date.now();
  const newEmployee = {
    id: newId,
    ...formData,
    status: "active",
    wageDetails: generateDefaultWage().map((item, idx) => ({
      ...item,
      id: Date.now() + idx,
    })),
  };
  emit("add", newEmployee);
  dialogVisible.value = false;
  resetForm();
  ElMessage.success(`员工 ${newEmployee.name} 添加成功`);
};
</script>
